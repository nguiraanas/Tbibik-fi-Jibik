"""
Data processing utilities for health metrics and ML models
"""

import math
import pandas as pd
from collections import defaultdict
from typing import Dict, Any, List, Union

def normalize_units(vars_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize units with automatic detection and conversion
    
    Args:
        vars_dict: Dictionary of health variables with potentially mixed units
        
    Returns:
        Dictionary with normalized units (kg, meters, cm)
    """
    normalized = vars_dict.copy()

    # Height: if > 3, assume cm and convert to meters
    if "height" in normalized and normalized["height"] is not None:
        if normalized["height"] > 3:
            normalized["height"] = normalized["height"] / 100

    # Waist: if < 80, likely inches, convert to cm
    if "waist" in normalized and normalized["waist"] is not None:
        if normalized["waist"] < 80:
            normalized["waist"] = normalized["waist"] * 2.54

    # Weight: if > 200, likely lbs, convert to kg
    if "weight" in normalized and normalized["weight"] is not None:
        if normalized["weight"] > 200:
            normalized["weight"] = normalized["weight"] * 0.453592

    return normalized

def predict_metr_ir(features: Union[Dict[str, Any], pd.DataFrame], pipeline) -> Dict[str, float]:
    """
    Predict METS-IR using sklearn pipeline
    
    Args:
        features: Health features as dict or DataFrame
        pipeline: Trained sklearn pipeline
        
    Returns:
        Dictionary with METS_IR prediction
        
    Raises:
        ValueError: If pipeline not loaded or invalid features
    """
    if pipeline is None:
        raise ValueError("Pipeline not loaded")
        
    if isinstance(features, dict):
        X = pd.DataFrame([features])
    elif isinstance(features, pd.DataFrame):
        X = features.copy()
    else:
        raise ValueError("features must be dict or DataFrame")

    if "Gender" in X.columns and X["Gender"].dtype == "object":
        X["Gender"] = X["Gender"].map({"Male": 1, "Female": 0})

    mets_ir_pred = pipeline.predict(X)[0]
    return {"METS_IR": float(mets_ir_pred)}

def sigmoid(x: float, steepness: float = 2) -> float:
    """
    Sigmoid function with adjustable steepness
    
    Args:
        x: Input value
        steepness: Controls the steepness of the sigmoid curve
        
    Returns:
        Sigmoid output between 0 and 1
    """
    return 1 / (1 + math.exp(-steepness * x))

def calculate_ir_risk(
    user_symptoms: List[str], 
    collection=None,
    top_k: int = 3, 
    similarity_threshold: float = 0.45
) -> float:
    """
    Calculate insulin resistance risk from symptoms using semantic similarity
    
    Args:
        user_symptoms: List of user-reported symptoms
        collection: ChromaDB collection for symptom matching
        top_k: Number of top matches to consider
        similarity_threshold: Minimum similarity threshold
        
    Returns:
        Risk score between 0 and 1
    """
    if not user_symptoms or collection is None:
        return 0.0

    # Track best match per symptom
    symptom_matches = defaultdict(lambda: {"similarity": 0, "relevance": 0, "type": None})
    matched_concepts = set()

    try:
        for symptom in user_symptoms:
            res = collection.query(
                query_texts=[symptom],
                n_results=top_k
            )

            best_match = None
            best_score = 0

            for meta, dist in zip(res["metadatas"][0], res["distances"][0]):
                if meta["type"] not in ("symptom", "biomarker"):
                    continue

                similarity = 1 - dist

                if similarity < similarity_threshold:
                    continue

                ir_relevance = meta.get("ir_relevance", 0.5)
                weighted_score = similarity * ir_relevance

                if weighted_score > best_score:
                    best_score = weighted_score
                    best_match = {
                        "similarity": similarity,
                        "relevance": ir_relevance,
                        "type": meta["type"],
                        "concept_id": meta["concept_id"],
                        "weighted_score": weighted_score
                    }

            if best_match:
                symptom_matches[symptom] = best_match
                matched_concepts.add(best_match["concept_id"])

        if not symptom_matches:
            return 0.0

        # Extract key metrics
        weighted_scores = [m["weighted_score"] for m in symptom_matches.values()]
        avg_weighted = sum(weighted_scores) / len(weighted_scores)
        max_weighted = max(weighted_scores)

        biomarker_count = sum(1 for m in symptom_matches.values() if m["type"] == "biomarker")
        symptom_count = sum(1 for m in symptom_matches.values() if m["type"] == "symptom")
        high_relevance_count = sum(1 for m in symptom_matches.values() if m["relevance"] >= 0.8)

        num_matches = len(symptom_matches)
        num_concepts = len(matched_concepts)

        # SPECIAL CASE 1: Single low-relevance symptom
        if num_matches == 1 and max_weighted < 0.5:
            return min(0.25, sigmoid(max_weighted * 0.6 - 0.3, steepness=3))

        # SPECIAL CASE 2: Multiple high-relevance biomarkers (severe cases)
        if biomarker_count >= 2 and high_relevance_count >= 2:
            base = avg_weighted * 1.5
            diversity_boost = num_concepts * 0.08
            return min(0.98, sigmoid(base + diversity_boost - 0.2, steepness=4))

        # GENERAL CASE: Standard calculation
        if num_matches == 1:
            avg_weighted *= 0.65
        elif num_matches == 2:
            avg_weighted *= 0.85

        # Diversity score with diminishing returns
        diversity = 1 - math.exp(-num_concepts / 2.5)

        # Biomarker boost
        if biomarker_count >= 3:
            biomarker_mult = 1.6
        elif biomarker_count == 2:
            biomarker_mult = 1.4
        elif biomarker_count == 1:
            biomarker_mult = 1.15
        else:
            biomarker_mult = 1.0

        # Multiple symptom boost
        if symptom_count >= 4:
            symptom_boost = 1.2
        elif symptom_count >= 3:
            symptom_boost = 1.1
        else:
            symptom_boost = 1.0

        # Combine all factors
        raw_score = avg_weighted * diversity * biomarker_mult * symptom_boost

        return sigmoid(raw_score - 0.38, steepness=4.2)
    
    except Exception as e:
        print(f"Symptom scoring error: {e}")
        return 0.0