"""
Diagnosis subgraph for health assessment and insulin resistance risk calculation
"""

import json
import re
import pandas as pd
from typing import Dict, Any, List
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END

from models.state_models import DiagnosisGraphState
from models.pydantic_models import ExtractedInfo, LoggingOutput, StateFixerOutput, DiagnosisOutput
from config.llm_config import LLMConfig
from config.settings import Settings
from utils.data_processing import normalize_units, predict_metr_ir, calculate_ir_risk

class DiagnosisSubgraph:
    """Handles complete health assessment workflow"""
    
    def __init__(self, pipeline=None, collection=None):
        """Initialize with ML components"""
        self.llm_clients = LLMConfig.create_llm_clients()
        self.pipeline = pipeline
        self.collection = collection
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the diagnosis subgraph"""
        builder = StateGraph(DiagnosisGraphState)
        
        # Add all nodes
        builder.add_node("info_extractor", self._info_extractor_node)
        builder.add_node("state_fixer", self._state_fixer_node)
        builder.add_node("orchestrator", self._orchestrator_node)
        builder.add_node("metr_ir", self._metr_ir_node)
        builder.add_node("symptom_scoring", self._symptom_scoring_node)
        builder.add_node("diagnosis", self._diagnosis_node)
        
        # Define edges
        builder.add_edge(START, "info_extractor")
        builder.add_edge("info_extractor", "state_fixer")
        builder.add_edge("state_fixer", "orchestrator")
        builder.add_edge("metr_ir", "orchestrator")
        builder.add_edge("symptom_scoring", "orchestrator")
        builder.add_edge("diagnosis", "orchestrator")
        
        # Conditional routing from orchestrator
        builder.add_conditional_edges(
            "orchestrator",
            self._orchestrator_router,
            {
                "state_fixer": "state_fixer",
                "symptom_scoring": "symptom_scoring",
                "metr_ir": "metr_ir",
                "diagnosis": "diagnosis",
                END: END,
            },
        )
        
        return builder.compile()
    
    def _info_extractor_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Extract medical information from user input"""
        user_input = state.get("input", "")
        print(user_input)
        existing_vars = state.get("vars", {})
        existing_symptoms = state.get("symptoms", [])

        # Build a context-aware prompt showing current state
        vars_status = []
        for key in ["age", "weight", "height", "waist", "gender"]:
            val = existing_vars.get(key)
            if val is not None:
                vars_status.append(f"{key}: {val} (already captured)")
            else:
                vars_status.append(f"{key}: null (needed)")

        extract_prompt = f"""Extract medical info from user message. Output ONLY valid JSON.

Current state:
{chr(10).join(vars_status)}

Existing symptoms: {existing_symptoms}

User message: "{user_input}"

CRITICAL RULES:
1. If user just greets (hello, hi, hey), return existing state unchanged
2. Do NOT ask for variables already captured (not null)
3. Extract ONLY what user explicitly mentions
4. Do NOT extract body descriptors as symptoms:
   ❌ "stubborn waist", "substantial weight", "big belly" → these are NOT symptoms
   ✅ "constant fatigue", "persistent thirst", "blurry vision" → these ARE symptoms

SYMPTOM EXAMPLES (3-6 words each):
✓ "tired every afternoon"
✓ "constantly thirsty despite drinking"
✓ "frequent urination at night"
✓ "blurry vision recently"
✓ "wounds heal very slowly"
✓ "tingling in both feet"
✓ "extreme hunger after meals"

UNIT CONVERSIONS:
- Weight: pounds → kg (1 lb = 0.453592 kg)
  Example: "280 lbs" → 127.0 kg
- Height: feet/inches → meters
  Example: "5'8\"" → 1.73 m, "5'6\"" → 1.68 m
- Waist: inches → cm (1 inch = 2.54 cm)
  Example: "48 inches" → 121.92 cm

EXTRACTION RULES:
- If user provides DIFFERENT value for existing variable, use the NEW value
- Extract embedded numbers: "I'm 72" → age: 72
- Keep existing values if not mentioned
- Set to null ONLY if never mentioned before
- Do NOT infer or estimate values

JSON format (no markdown, no extra text):
{{
  "vars": {{
    "age": {existing_vars.get('age', 'null')},
    "weight": {existing_vars.get('weight', 'null')},
    "height": {existing_vars.get('height', 'null')},
    "waist": {existing_vars.get('waist', 'null')},
    "gender": {json.dumps(existing_vars.get('gender')) if existing_vars.get('gender') else 'null'}
  }},
  "symptoms": []
}}"""

        try:
            # Try structured output first
            extracted = self.llm_clients["extractor"].with_structured_output(ExtractedInfo).invoke(extract_prompt)

            # Merge vars: new non-null values overwrite existing
            new_vars = existing_vars.copy()
            for k, v in extracted.vars.items():
                if v not in (None, "", "null", "None"):
                    new_vars[k] = v

            # Filter out non-symptom descriptors
            filtered_symptoms = []
            invalid_patterns = [
                r'\b(stubborn|substantial|big|large|small|thin)\s+(waist|weight|belly|size)\b',
                r'\b(weight|waist|height|size|body)\b(?!\s+loss|\s+gain)',
            ]

            for symptom in extracted.symptoms:
                if isinstance(symptom, str) and symptom.strip():
                    # Check if it's a body descriptor
                    is_descriptor = any(
                        re.search(pattern, symptom.lower())
                        for pattern in invalid_patterns
                    )
                    if not is_descriptor:
                        filtered_symptoms.append(symptom.strip())

            # Deduplicate symptoms (case-insensitive)
            seen = {s.lower() for s in existing_symptoms}
            new_symptoms = existing_symptoms.copy()

            for symptom in filtered_symptoms:
                if symptom.lower() not in seen:
                    new_symptoms.append(symptom)
                    seen.add(symptom.lower())

            return {
                "vars": new_vars,
                "symptoms": new_symptoms
            }

        except Exception as e:
            print(f"Info extractor error: {e}")
            # On error, return existing state unchanged
            return {
                "vars": existing_vars,
                "symptoms": existing_symptoms
            }
    
    def _create_logging_entry(self, prompt: str, previous_logs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Create logging entry for conversation tracking"""
        # Count how many times this type was asked before
        type_map = {"missing_vars": "demographics", "missing_symptoms": "symptoms"}
        log_type = type_map.get(prompt, prompt)

        times_asked = sum(1 for log in previous_logs if log.get("type") == log_type)

        log_prompt = f"""
Generate a logging entry for tracking conversation flow.

Context: {prompt}
Previous logs: {previous_logs}

Return JSON only:
{{
  "type": "{log_type}",
  "times_asked": {times_asked + 1}
}}
"""

        try:
            out = self.llm_clients["logger"].with_structured_output(LoggingOutput).invoke(log_prompt)
            updated = previous_logs.copy()
            updated.append({"type": out.type, "times_asked": out.times_asked})
            return updated
        except:
            # Fallback: manual logging
            updated = previous_logs.copy()
            updated.append({"type": log_type, "times_asked": times_asked + 1})
            return updated
    
    def _state_fixer_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize variable names and units"""
        vars_dict = state.get("vars", {})

        fix_prompt = f"""
You normalize variable names and values for medical data.

Input variables:
{vars_dict}

Canonical schema:
- age: number (years)
- weight: number (kg only)
- height: number (meters only)
- waist: number (cm only)
- gender: "Male" or "Female"

Rules:
1. Rename keys only if meaning is clear
2. Keep values as-is (unit conversion handled separately)
3. Drop variables with invalid types or impossible values
4. Do NOT infer or invent values
5. Return JSON only

Output format:
{{
  "vars": {{
    "age": number or null,
    "weight": number or null,
    "height": number or null,
    "waist": number or null,
    "gender": "Male" or "Female" or null
  }}
}}
"""

        try:
            output = self.llm_clients["state_fixer"].with_structured_output(StateFixerOutput).invoke(fix_prompt)
            return {
                "vars": normalize_units(output.vars)
            }
        except:
            # Fallback: just normalize units
            return {
                "vars": normalize_units(vars_dict)
            }
    
    def _metr_ir_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate METS-IR score"""
        vars = state.get("vars", {})
        
        # Check if all required variables are present
        required_keys = ["age", "gender", "weight", "height", "waist"]
        for key in required_keys:
            if key not in vars or vars[key] is None:
                return {"metr_ir": None}
        
        try:
            X = pd.DataFrame({
                "Age": [vars["age"]],
                "Gender": [vars["gender"]],
                "BMI": [vars["weight"] / vars["height"]**2],
                "Waist_cm": [vars["waist"]],
            })

            result = predict_metr_ir(X, self.pipeline)
            return {"metr_ir": result["METS_IR"]}
        except Exception as e:
            print(f"METS-IR calculation error: {e}")
            return {"metr_ir": None}
    
    def _symptom_scoring_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Score symptoms for insulin resistance risk"""
        symptoms = state.get("symptoms", []) or []
        result = calculate_ir_risk(symptoms, self.collection)
        return {"symptom_scores": {"score": result}}
    
    def _orchestrator_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Orchestrate workflow and prevent redundant questions"""
        vars_dict = state.get("vars", {})
        ir_symptoms = state.get("symptoms", []) or []
        scores = state.get("symptom_scores", None)
        metr_ir_val = state.get("metr_ir", None)
        logs = state.get("logging", [])

        # Check which vars have actual values (not just keys)
        vars_with_values = {k for k, v in vars_dict.items() if v is not None}
        missing_vars = Settings.REQUIRED_VARS - vars_with_values

        # 1) Missing variables - but only ask once or twice
        demographics_asked = sum(
            1 for log in logs
            if log.get("type") == "demographics"
        )

        if missing_vars and not metr_ir_val and demographics_asked < 2:
            msg = f"Please provide the following health details: {', '.join(sorted(missing_vars))}."
            return {
                "orchestrator_response": {"output": msg, "type": "question", "confidence": 80},
                "logging": self._create_logging_entry("missing_vars", logs),
                "ready": False,
                "router_next": END
            }

        # 2) Missing symptoms - but only ask once or twice
        symptoms_asked = sum(
            1 for log in logs
            if log.get("type") == "symptoms"
        )

        if len(ir_symptoms) < 3 and symptoms_asked < 2:
            msg = "Could you list any symptoms you have noticed? e.g., fatigue, thirst..."
            return {
                "orchestrator_response": {"output": msg, "type": "question", "confidence": 80},
                "logging": self._create_logging_entry("missing_symptoms", logs),
                "ready": False,
                "router_next": END
            }

        # 3) METR-IR missing
        if metr_ir_val is None and not missing_vars:
            return {
                "orchestrator_response": {"output": "Running metabolic risk model…", "type": "info", "confidence": 90},
                "ready": False,
                "router_next": "metr_ir",
            }

        # 4) Symptom scores missing
        if scores is None and len(ir_symptoms) >= 1:
            return {
                "orchestrator_response": {"output": "Analyzing symptom relevance…", "type": "info", "confidence": 90},
                "ready": False,
                "router_next": "symptom_scoring",
            }

        # 5) Final diagnosis
        if not state.get("final_output"):
            return {"router_next": "diagnosis", "ready": True}

        return {"router_next": END}
    
    def _orchestrator_router(self, state: Dict[str, Any]) -> str:
        """Route based on orchestrator decision"""
        router_next = state.get("router_next")
        if router_next:
            return router_next
        return END
    
    def _get_mets_ir_interpretation(self, value: float) -> str:
        """Get METS-IR interpretation"""
        prompt = f"""
You are a medical laboratory data interpreter.

Interpret the METS-IR value below using fixed thresholds:

Thresholds:
- Low Risk: METS-IR < 35
- Moderate Risk: 35 ≤ METS-IR ≤ 50
- High Risk: METS-IR > 50

METS-IR value: {value}

Write a concise, professional explanation that includes:
1. Status: Low / Moderate / High
2. Interpretation of insulin sensitivity and cardiometabolic risk
3. Recommendation to discuss with a physician
4. Disclaimer: this is a screening tool only, not a diagnosis

Rules:
- Do NOT infer or include symptoms
- Do NOT give treatment advice
- Professional and supportive tone
- Return JSON only, no markdown

Output format:
{{
  "response": "text"
}}
"""
        try:
            result = self.llm_clients["mets_ir_explainer"].invoke(prompt)
            return json.loads(result.content)['response']
        except:
            # Fallback interpretation
            if value < Settings.METS_IR_LOW_THRESHOLD:
                return "Low insulin resistance risk. Metabolic profile appears healthy."
            elif value <= Settings.METS_IR_HIGH_THRESHOLD:
                return "Moderate insulin resistance risk. Consider lifestyle modifications and consult your physician."
            else:
                return "High insulin resistance risk. Please discuss with your healthcare provider for further evaluation."
    
    def _diagnosis_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Generate final diagnosis combining METS-IR and symptoms"""
        scores = state.get("symptom_scores", {}) or {}
        metr_ir_val = state.get("metr_ir", None)
        vars = state.get("vars", {})
        ir_symptoms = state.get("symptoms", []) or []

        prompt = f"""
You are a medical interpretation agent specialized in insulin resistance risk screening.

Important context:
- The METS-IR value is a regression-based risk model output, not a lab measurement
- It is derived from: age, gender, BMI, and waist circumference
- It represents an estimated insulin resistance risk score

Input data:
- semantic_score: {scores.get('score', 0)} (symptom relevance to IR, range 0-1)
- mets_ir_value: {metr_ir_val} (model-derived risk score)
- demographics: {vars}
- symptoms: {ir_symptoms}

Task: Provide an assessment of insulin resistance risk for screening and triage.

Rules:
1. METS-IR score is the primary driver of risk classification
2. Symptoms may adjust risk UP by at most one level if:
   - semantic_score ≥ 0.5, AND
   - at least 3 symptoms are clinically consistent with IR
3. Symptoms CANNOT reduce risk below METS-IR indication
4. If METS-IR appears atypical, note this as model behavior (extrapolation)
5. Do NOT interpret METS-IR as a blood test or lab value
6. Respond professionally and clearly
7. Return JSON only, no markdown

Output format:
{{
  "risk_level": "Low | Moderate | High",
  "dominant_factor": "mets_ir_result | semantic_score | balanced",
  "interpretation": "1-2 sentences explaining risk using METS-IR, symptoms, and demographics",
  "note": "optional comment if METS-IR reflects model extrapolation or extreme inputs"
}}
"""

        try:
            result = self.llm_clients["risk_fusion"].invoke(prompt)
            return {"final_output": json.loads(result.content)}
        except Exception as e:
            print(f"Diagnosis error: {e}")
            # Fallback diagnosis
            if metr_ir_val is None:
                risk = "Unknown"
                interpretation = "Unable to calculate risk due to missing data."
            else:
                risk = "High" if metr_ir_val > Settings.METS_IR_HIGH_THRESHOLD else (
                    "Moderate" if metr_ir_val >= Settings.METS_IR_LOW_THRESHOLD else "Low"
                )
                interpretation = f"Based on METS-IR score of {metr_ir_val:.1f}, insulin resistance risk is {risk.lower()}."
            
            return {
                "final_output": {
                    "risk_level": risk,
                    "dominant_factor": "mets_ir_result",
                    "interpretation": interpretation,
                    "note": ""
                }
            }
    
    def invoke(self, state: DiagnosisGraphState) -> DiagnosisGraphState:
        """Invoke the diagnosis subgraph"""
        return self.graph.invoke(state)