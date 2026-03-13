"""
Car Rental Data Cleaning & Transformation Pipeline
===================================================

Entry point for the entire project.
Run with: python main.py

This script:
1. Creates required directories
2. Generates the raw messy dataset (~2000 records)
3. Cleans and normalizes the data
4. Validates records and separates rejects
5. Removes duplicates and detects fraud
6. Computes analytics and KPIs
7. Saves all outputs to data/output/
"""

import os
import sys

# Ensure the project root is in the Python path
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.pipeline.pipeline_runner import run_pipeline


def main():
    """Run the complete car rental data pipeline."""
    # Ensure directories exist
    dirs = [
        os.path.join(PROJECT_ROOT, "data", "raw"),
        os.path.join(PROJECT_ROOT, "data", "output"),
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

    # Run the pipeline
    result = run_pipeline(project_root=PROJECT_ROOT)
    return result


if __name__ == "__main__":
    main()
