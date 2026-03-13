# """
# Data Reader Module
# Developer 1 - Responsible for loading raw CSV data into memory.

# Reads the raw car rental CSV and returns records as a list of dictionaries.
# """

# import csv
# import os


# def load_csv(file_path):
#     """
#     Load a CSV file and return records as a list of dictionaries.

#     Args:
#         file_path: Path to the CSV file.

#     Returns:
#         list[dict]: List of row dictionaries.

#     Raises:
#         FileNotFoundError: If the CSV file does not exist.
#     """
#     if not os.path.exists(file_path):
#         raise FileNotFoundError(f"Raw data file not found: {file_path}")

#     records = []
#     with open(file_path, "r", encoding="utf-8") as f:
#         reader = csv.DictReader(f)
#         for row in reader:
#             records.append(dict(row))

#     return records


# def save_csv(records, file_path, fieldnames=None):
#     """
#     Save a list of dictionaries to a CSV file.

#     Args:
#         records: List of row dictionaries.
#         file_path: Output CSV path.
#         fieldnames: Column names. If None, inferred from first record.
#     """
#     if not records:
#         # Write empty file with headers if fieldnames provided
#         os.makedirs(os.path.dirname(file_path), exist_ok=True)
#         if fieldnames:
#             with open(file_path, "w", newline="", encoding="utf-8") as f:
#                 writer = csv.DictWriter(f, fieldnames=fieldnames)
#                 writer.writeheader()
#         return

#     if fieldnames is None:
#         fieldnames = list(records[0].keys())

#     os.makedirs(os.path.dirname(file_path), exist_ok=True)
#     with open(file_path, "w", newline="", encoding="utf-8") as f:
#         writer = csv.DictWriter(f, fieldnames=fieldnames)
#         writer.writeheader()
#         writer.writerows(records)


# if __name__ == "__main__":
#     data = load_csv("../../data/raw/car_rental_raw.csv")
#     print(f"Loaded {len(data)} records.")
#     if data:
#         print(f"Columns: {list(data[0].keys())}")






"""
Data Reader Module
Developer 1 - Responsible for loading raw CSV data into memory.

Reads the raw car rental CSV and returns records as a list of dictionaries.
"""

import csv
import os


def load_csv(file_path):
    """
    Load a CSV file and return records as a list of dictionaries.

    Args:
        file_path: Path to the CSV file.

    Returns:
        list[dict]: List of row dictionaries.

    Raises:
        FileNotFoundError: If the CSV file does not exist.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Raw data file not found: {file_path}")

    records = []

    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            records.append(dict(row))

    return records


def save_csv(records, file_path, fieldnames=None):
    """
    Save a list of dictionaries to a CSV file.

    Args:
        records: List of row dictionaries.
        file_path: Output CSV path.
        fieldnames: Column names. If None, inferred from first record.
    """

    # If no records exist
    if not records:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        if fieldnames:
            with open(file_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(
                    f,
                    fieldnames=fieldnames,
                    extrasaction="ignore"   # ignore extra fields
                )
                writer.writeheader()
        return

    # Infer fieldnames if not provided
    if fieldnames is None:
        fieldnames = list(records[0].keys())

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w", newline="", encoding="utf-8") as f:

        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames,
            extrasaction="ignore"   # ⭐ THIS FIXES YOUR ERROR
        )

        writer.writeheader()
        writer.writerows(records)


if __name__ == "__main__":
    data = load_csv("../../data/raw/car_rental_raw.csv")

    print(f"Loaded {len(data)} records.")

    if data:
        print(f"Columns: {list(data[0].keys())}")