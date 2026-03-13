"""
Dataset Generator Wrapper
-------------------------

This module preserves the original pipeline interface so that
existing code calling `generate_dataset()` continues to work.

Internally it calls the advanced generator which produces
multiple raw datasets and merges them into car_rental_raw.csv.
"""

import os
from src.ingestion.generator import generate_all


def generate_dataset(output_path, num_records=2000, seed=42):
    """
    Wrapper used by the pipeline.

    Args:
        output_path (str): Output CSV path expected by pipeline
        num_records (int): number of records (not used internally)
        seed (int): random seed (handled in generator)

    Returns:
        int: number of records generated
    """

    # generator creates all datasets and merged raw dataset
    count = generate_all()

    # ensure folder exists (pipeline safety)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    return count


if __name__ == "__main__":
    path = "../../data/raw/car_rental_raw.csv"
    count = generate_dataset(path)
    print(f"Generated {count} records")