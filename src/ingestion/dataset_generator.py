import os
from src.ingestion.generator import generate_all


def generate_dataset(output_path, num_records=2000, seed=42):
    count = generate_all()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    return count


if __name__ == "__main__":
    path = "../../data/raw/car_rental_raw.csv"
    count = generate_dataset(path)
    print(f"Generated {count} records")