# System Architecture

## High-Level Architecture

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   RAW DATA   │───▶│   CLEANING   │───▶│  VALIDATION  │
│  Generation  │    │   Module     │    │   Module     │
│ (Dev 1)      │    │ (Dev 2)      │    │ (Dev 3)      │
└──────────────┘    └──────────────┘    └──────┬───────┘
                                               │
                                    ┌──────────┴──────────┐
                                    ▼                     ▼
                              ┌───────────┐        ┌───────────┐
                              │  VALID    │        │ REJECTED  │
                              │  Records  │        │ Records   │
                              └─────┬─────┘        └───────────┘
                                    │                     │
                                    ▼                     ▼
                              ┌───────────┐        rejected_
                              │ DEDUP &   │        reservations.csv
                              │ FRAUD     │
                              │ (Dev 4)   │
                              └─────┬─────┘
                                    │
                                    ▼
                              ┌───────────┐
                              │ ANALYTICS │
                              │ & KPIs    │
                              │ (Dev 5)   │
                              └─────┬─────┘
                                    │
                          ┌─────────┼─────────┐
                          ▼         ▼         ▼
                    cleaned_   metrics_    Terminal
                    reserv..   report.csv  Summary
```

## Module Responsibilities

### Developer 1: Ingestion (`src/ingestion/`)
- **dataset_generator.py**: Generates ~2000 realistic records with intentional data quality issues. Uses configurable random seed for reproducibility. Produces messy Vehicle IDs, mixed timestamp formats, odometer values with units, fuel in percent/fraction, rates with currency symbols, city abbreviations, payment case variations, duplicate records, and negative mileage cases.
- **reader.py**: Generic CSV reader/writer using Python's `csv.DictReader`. Handles file I/O, directory creation, and encoding.

### Developer 2: Cleaning (`src/cleaning/`)
- **cleaner.py**: Field-level cleaning functions:
  - `clean_vehicle_id()`: Trims whitespace, converts to uppercase
  - `clean_timestamp()`: Fixes invalid minutes (carry-over arithmetic), tries multiple parse formats, outputs `YYYY-MM-DD HH:MM`
  - `clean_odometer()`: Strips units ("km"), removes commas, converts to integer
  - `clean_fuel_level()`: Converts percent to fraction (50% → 0.50)
  - `clean_rate()`: Removes ₹, /day, commas; converts to integer
  - `clean_city()`: Maps abbreviations to canonical names using lookup dict
  - `clean_payment()`: Normalizes to uppercase, validates against allowed set

### Developer 3: Validation (`src/validation/`)
- **validator.py**: Rule-based validation:
  - Return timestamp must be after pickup timestamp
  - Odo_End must be ≥ Odo_Start
  - Fuel level must be in [0, 1]
  - Payment must be one of: UPI, CARD, CASH, WALLET
  - Required fields must not be null
  - Invalid records are tagged with rejection reasons

### Developer 4: Processing (`src/processing/`)
- **deduplicator.py**: Deduplication and fraud detection:
  - Removes duplicates by Reservation_ID (keeps first)
  - Detects overlapping bookings for the same vehicle
  - Detects odometer rollback across sequential bookings
  - Computes fraud risk score (0-8) based on: short rental + long distance (+3), overlapping booking (+2), odometer rollback (+3)
  - Assigns risk levels: None, Low, Medium, High

### Developer 5: Analytics (`src/analytics/`)
- **transformer.py**: KPI computation:
  - Per-record: Distance_km, Rental_Hours, Revenue, Cost_per_km
  - Aggregate: Fleet utilization by vehicle, revenue by city, average duration, vehicle usage frequency, fraud risk distribution

### Developer 6: SQL Analytics (`sql/`)
- **schema.sql**: 6-table relational schema (CUSTOMERS, VEHICLES, RESERVATIONS, PAYMENTS, MAINTENANCE, LOCATIONS)
- **inserts.sql**: 10+ sample records per table
- **solutions.sql**: 12 advanced queries using JOINs, GROUP BY, window functions (RANK, LAG, SUM OVER), CTEs, and CASE expressions

## Data Flow
1. Raw CSV (2080 records, messy) → Cleaning → 2080 cleaned records
2. Cleaned → Validation → Valid + Rejected split
3. Valid → Deduplication → ~1920 unique records with fraud scores
4. Unique → Analytics → Enriched records with KPIs
5. Output: 3 CSV files + terminal summary

## Design Decisions
- **No external dependencies**: Uses only Python standard library (csv, datetime, re, os, sys, random, collections)
- **Dictionary-based records**: Simple and portable without requiring pandas/numpy
- **Modular pipeline**: Each stage is independently testable and replaceable
- **Deterministic output**: Random seed ensures reproducible dataset generation
