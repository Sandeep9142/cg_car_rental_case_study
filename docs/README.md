# Car Rental Data Cleaning & Transformation Case Study

## Overview
A multi-city car rental company collects data from multiple systems (reservation, telematics, maintenance, payments, feedback). This project implements a complete data engineering pipeline that:

1. **Generates** a realistic messy dataset (~2000 records)
2. **Cleans** and normalizes all data fields
3. **Validates** records against business rules
4. **Deduplicates** reservations and detects fraud
5. **Transforms** data into analytics-ready KPIs
6. **Provides** SQL analytics for advanced querying

## Project Structure
```
car_rental_project/
├── main.py                          # Entry point - run this
├── data/
│   ├── raw/car_rental_raw.csv       # Generated messy dataset
│   └── output/
│       ├── cleaned_reservations.csv # Clean, enriched records
│       ├── rejected_reservations.csv# Invalid records with reasons
│       └── metrics_report.csv       # KPI metrics per reservation
├── src/
│   ├── ingestion/
│   │   ├── dataset_generator.py     # Developer 1: Data generation
│   │   └── reader.py               # Developer 1: CSV I/O
│   ├── cleaning/
│   │   └── cleaner.py              # Developer 2: Data cleaning
│   ├── validation/
│   │   └── validator.py            # Developer 3: Validation rules
│   ├── processing/
│   │   └── deduplicator.py         # Developer 4: Dedup & fraud
│   ├── analytics/
│   │   └── transformer.py          # Developer 5: KPI computation
│   └── pipeline/
│       └── pipeline_runner.py       # Pipeline orchestration
├── sql/
│   ├── schema.sql                   # Developer 6: DB schema
│   ├── inserts.sql                  # Developer 6: Sample data
│   └── solutions.sql               # Developer 6: Analytics queries
└── docs/
    ├── README.md                    # This file
    ├── architecture.md              # System architecture
    └── evaluation_questions.md      # Q&A for evaluators
```

## How to Run
```bash
cd car_rental_project
python main.py
```

No external dependencies required — uses only Python standard library.

## Pipeline Stages

| Stage | Description |
|-------|-------------|
| 1. Generate | Creates ~2080 records with intentional data issues |
| 2. Load | Reads raw CSV into memory |
| 3. Clean | Normalizes Vehicle IDs, timestamps, odometers, fuel, rates, cities, payments |
| 4. Validate | Checks timestamps, odometers, fuel ranges, payment methods |
| 5. Deduplicate | Removes duplicates by Reservation_ID, computes fraud risk scores |
| 6. Transform | Computes distance, duration, revenue, cost/km, fleet utilization |
| 7. Output | Saves cleaned, rejected, and metrics CSVs |

## Data Quality Issues Handled
- **Vehicle_ID**: Extra spaces, case inconsistencies
- **Timestamps**: Multiple formats, invalid minutes (e.g., 10:75)
- **Odometer**: Text units ("45,000 km"), commas
- **Fuel Level**: Mixed percent/fraction ("50%" vs "0.5")
- **Rate**: Currency symbols ("₹1,500/day")
- **City**: Abbreviations ("blr" → "Bengaluru")
- **Payment**: Case variations ("upi" → "UPI")
- **Duplicates**: Same Reservation_ID appearing multiple times
- **Mileage**: Odo_End < Odo_Start (rollback)

## Team Structure
- **Developer 1**: Dataset generation & ingestion
- **Developer 2**: Data cleaning module
- **Developer 3**: Data validation module
- **Developer 4**: Deduplication & fraud detection
- **Developer 5**: Analytics & KPI transformation
- **Developer 6**: SQL analytics
