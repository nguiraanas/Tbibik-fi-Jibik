# Nutrition and Health Analysis Notebooks

This repository contains a comprehensive collection of Jupyter notebooks focused on nutrition analysis, health assessment, and AI-powered nutrition guidance. The project combines computer vision, machine learning, and natural language processing to create tools for nutritional fact extraction, health risk assessment, and intelligent nutrition counseling.

##  Table of Contents

- [Overview](#overview)
- [Notebooks](#notebooks)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)

##  Overview

This project encompasses several interconnected components for nutrition and health analysis:

1. **Computer Vision for Nutrition Facts**: Automated extraction of nutritional information from product images
2. **Health Risk Assessment**: Machine learning models for insulin resistance and metabolic syndrome evaluation
3. **Semantic Health Analysis**: Natural language processing for symptom analysis and health scoring
4. **AI Nutrition Agent**: Intelligent conversational agent for personalized nutrition guidance
5. **Calorie Estimation**: Image-based calorie estimation from food photos

##  Notebooks

### 1. CaloriesFromImageModel.ipynb
**Purpose**: Develops a computer vision model to estimate calories from food images using advanced image recognition techniques.

**Key Features**:
- Image preprocessing and augmentation
- Deep learning model training for calorie estimation
- Integration with nutrition databases
- Real-time calorie prediction from photos

### 2. IR-Symptoms-Semantic-Scoring.ipynb
**Purpose**: Creates a semantic scoring system for insulin resistance symptoms using natural language processing and machine learning.

**Key Features**:
- Symptom text analysis and classification
- Semantic similarity scoring for health symptoms
- Insulin resistance risk assessment
- Medical terminology processing and standardization
- Integration with SNOMED CT medical codes

### 3. METS-IR-Model.ipynb
**Purpose**: Implements machine learning models for Metabolic Syndrome and Insulin Resistance (METS-IR) prediction and analysis.

**Key Features**:
- Statistical analysis of nutrition datasets
- Metabolic syndrome risk factor identification
- Predictive modeling for insulin resistance
- Data visualization and exploratory analysis
- Correlation analysis between dietary patterns and health outcomes

### 4. NutritionAgentDev.ipynb
**Purpose**: Develops an intelligent conversational AI agent for personalized nutrition guidance and health assessment.

**Key Features**:
- Multi-agent architecture using LangGraph
- Semantic message decomposition and routing
- Memory-aware conversation management
- Personalized nutrition recommendations
- Health risk assessment integration
- Real-time chat interface with medical knowledge

### 5. Nutrition-Fact-Extraction/NutritionalFactTable_TO_JSON.ipynb
**Purpose**: Extracts and converts nutritional fact tables from images into structured JSON format.

**Key Features**:
- OCR (Optical Character Recognition) for nutrition labels
- Structured data extraction from unstructured text
- JSON schema validation for nutrition facts
- Integration with Hugging Face models for text processing
- Automated nutrition label parsing

### 6. Nutrition-Fact-Extraction/Yolo_Product_Fact_Table_Detection.ipynb
**Purpose**: Uses YOLO (You Only Look Once) object detection to identify and locate nutrition fact tables in product images.

**Key Features**:
- YOLO model training for nutrition label detection
- Bounding box prediction for fact tables
- Image preprocessing and augmentation
- Real-time detection capabilities
- Integration with Ultralytics framework

##  Features

### Computer Vision Capabilities
- **Nutrition Label Detection**: Automatically locate nutrition fact tables in product images
- **OCR Integration**: Extract text from nutrition labels with high accuracy
- **Calorie Estimation**: Estimate calories from food photos using deep learning
- **Image Preprocessing**: Advanced image enhancement and normalization

### Health Assessment Tools
- **Insulin Resistance Scoring**: ML-based risk assessment for insulin resistance
- **Symptom Analysis**: Semantic analysis of health symptoms and conditions
- **Metabolic Syndrome Prediction**: Predictive models for metabolic health risks
- **Personalized Health Insights**: Tailored recommendations based on individual profiles

### AI-Powered Nutrition Guidance
- **Conversational Agent**: Natural language interface for nutrition queries
- **Memory Management**: Context-aware conversations with session persistence
- **Multi-Modal Analysis**: Integration of text, image, and structured data
- **Real-Time Recommendations**: Instant nutrition advice and meal suggestions

### Data Processing & Analysis
- **Structured Data Extraction**: Convert unstructured nutrition data to JSON
- **Statistical Analysis**: Comprehensive analysis of nutrition datasets
- **Visualization Tools**: Interactive charts and graphs for data insights
- **Database Integration**: ChromaDB for vector storage and similarity search

##  Installation

### Note
Every notebook was developed using Google Colab and a L4 GPU which is the recommended for the replication 

### Prerequisites
- Python 3.8+
- Jupyter Notebook or JupyterLab
- CUDA-compatible GPU (recommended for deep learning models)
- Ollama (for local LLM inference)

### Required Libraries
```bash
# Core dependencies
pip install jupyter pandas numpy matplotlib seaborn scikit-learn

# Computer Vision
pip install opencv-python ultralytics torch torchvision

# Natural Language Processing
pip install transformers sentence-transformers langchain langgraph

# OCR and Image Processing
pip install pytesseract pillow qwen-vl-utils

# Database and Vector Storage
pip install chromadb

# Additional ML libraries
pip install xgboost lightgbm optuna

# Visualization
pip install plotly bokeh
```

### Ollama Setup (for NutritionAgent)
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull required models
ollama pull gemma3:4b
ollama pull embeddinggemma:latest
```

##  Usage

### Running Individual Notebooks

1. **Calorie Estimation**:
   ```bash
   jupyter notebook CaloriesFromImageModel.ipynb
   ```

2. **Health Risk Assessment**:
   ```bash
   jupyter notebook METS-IR-Model.ipynb
   ```

3. **Symptom Analysis**:
   ```bash
   jupyter notebook IR-Symptoms-Semantic-Scoring.ipynb
   ```

4. **Nutrition Agent Development**:
   ```bash
   jupyter notebook NutritionAgentDev.ipynb
   ```

5. **Nutrition Fact Extraction**:
   ```bash
   jupyter notebook Nutrition-Fact-Extraction/NutritionalFactTable_TO_JSON.ipynb
   jupyter notebook Nutrition-Fact-Extraction/Yolo_Product_Fact_Table_Detection.ipynb
   ```

##  Project Structure

```
├── CaloriesFromImageModel.ipynb           # Calorie estimation from images
├── IR-Symptoms-Semantic-Scoring.ipynb    # Symptom analysis and scoring
├── METS-IR-Model.ipynb                   # Metabolic syndrome prediction
├── NutritionAgentDev.ipynb               # AI nutrition agent development
├── Nutrition-Fact-Extraction/           # Nutrition label processing
│   ├── NutritionalFactTable_TO_JSON.ipynb
│   └── Yolo_Product_Fact_Table_Detection.ipynb
├── NutritionAgent/                       # Production-ready agent code
│   ├── config/                          # Configuration files
│   ├── core/                           # Core agent functionality
│   ├── models/                         # Data models and schemas
│   ├── subgraphs/                      # Agent subcomponents
│   ├── utils/                          # Utility functions
│   └── interfaces/                     # User interfaces
└── README.md                            # This file
```

##  Technologies Used

### Machine Learning & AI
- **PyTorch**: Deep learning framework for computer vision models
- **Transformers**: Hugging Face library for NLP models
- **Ultralytics YOLO**: Object detection for nutrition labels
- **Sentence Transformers**: Semantic similarity and embeddings
- **LangChain/LangGraph**: AI agent orchestration and workflow management

### Data Processing
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **OpenCV**: Computer vision and image processing
- **Tesseract OCR**: Optical character recognition

### Databases & Storage
- **ChromaDB**: Vector database for semantic search
- **SQLite**: Local data storage
- **JSON**: Structured data format

### Visualization
- **Matplotlib/Seaborn**: Statistical plotting
- **Plotly**: Interactive visualizations
- **Jupyter Widgets**: Interactive notebook components

### Web & APIs
- **Ollama**: Local LLM inference server
- **Hugging Face Hub**: Model repository and APIs
- **FastAPI**: Web API framework (for deployment)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

##  Disclaimer

**Important**: This software is for educational and research purposes only. It is not intended to diagnose, treat, cure, or prevent any disease. The nutrition and health assessments provided are not a substitute for professional medical advice. Always consult with qualified healthcare professionals for medical advice, diagnosis, and treatment.



*Last updated: December 2024*

**Note that this is an AI Generated Readme.md following a set of oriented prompt**