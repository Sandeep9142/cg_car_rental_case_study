import csv
import os


def load_csv(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Raw data file not found: {file_path}")

    records = []

    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            records.append(dict(row))

    return records


def save_csv(records, file_path, fieldnames=None):
    if not records:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        if fieldnames:
            with open(file_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(
                    f,
                    fieldnames=fieldnames,
                    extrasaction="ignore"   
                )
                writer.writeheader()
        return

    if fieldnames is None:
        fieldnames = list(records[0].keys())

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w", newline="", encoding="utf-8") as f:

        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames,
            extrasaction="ignore"   
        )

        writer.writeheader()
        writer.writerows(records)


if __name__ == "__main__":
    data = load_csv("../../data/raw/car_rental_raw.csv")

    print(f"Loaded {len(data)} records.")

    if data:
        print(f"Columns: {list(data[0].keys())}")