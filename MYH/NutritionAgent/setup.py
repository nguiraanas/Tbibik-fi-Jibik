"""
Setup script for NutritionAgent package
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="nutrition-agent",
    version="1.0.0",
    author="Nutrition Agent Team",
    author_email="contact@nutritionagent.com",
    description="AI-powered insulin resistance health assessment and nutrition guidance system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nutritionagent/nutrition-agent",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Healthcare Industry",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "langchain-ollama>=0.1.0",
        "langchain-core>=0.3.0",
        "langgraph>=0.2.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "joblib>=1.3.0",
        "chromadb>=0.4.0",
        "pydantic>=2.0.0",
        "typing-extensions>=4.8.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "nutrition-agent=NutritionAgent.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "NutritionAgent": ["config/*.json", "data/*.pkl"],
    },
)