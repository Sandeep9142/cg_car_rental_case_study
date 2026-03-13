# Evaluation Questions & Answers

## Q1: How does the cleaning pipeline work?

The cleaning pipeline processes each record through a series of field-level transformation functions:

1. **Vehicle_ID**: `strip()` removes leading/trailing whitespace, `upper()` standardizes case. Example: `"  car-12  "` → `"CAR-12"`.

2. **Timestamps**: First, invalid minutes are detected using regex (e.g., `10:75`). The fix uses carry-over arithmetic: `75 minutes = 1 hour + 15 minutes`, so `10:75` becomes `11:15`. Then the corrected string is parsed against 5 known formats (`YYYY/MM/DD HH:MM`, `YYYY-MM-DD HH:MM`, `DD-MM-YYYY HH:MM`, etc.) and output in the canonical format `YYYY-MM-DD HH:MM`.

3. **Odometer**: Regex removes "km"/"KM" suffixes, then commas are stripped, and the result is cast to integer. Example: `"45,000 km"` → `45000`.

4. **Fuel Level**: If `%` is present, the numeric part is divided by 100. Otherwise, the value is parsed as-is. Example: `"50%"` → `0.50`, `"0.5"` → `0.50`.

5. **Rate**: The `₹` symbol, `/day` suffix, and commas are removed, then cast to integer. Example: `"₹1,500/day"` → `1500`.

6. **City**: A lowercase lookup dictionary maps variants to canonical names. Example: `"blr"` → `"Bengaluru"`, `"bangalore"` → `"Bengaluru"`.

7. **Payment**: Converted to uppercase and checked against the allowed set {UPI, CARD, CASH, WALLET}.

Each function is pure (no side effects), making them independently testable.

---

## Q2: How are duplicates detected?

Duplicates are detected using the `Reservation_ID` field as the unique key. The deduplicator iterates through all records, maintaining a `set` of seen IDs. The first occurrence of each ID is kept; subsequent occurrences are counted as duplicates and discarded.

This approach is O(n) in time complexity with O(n) space for the set.

---

## Q3: How is fraud detected?

Fraud detection uses a scoring system with three risk factors:

1. **Short rental with large distance** (+3 points): A rental under 4 hours covering more than 500 km is flagged as suspicious — this indicates possible odometer tampering.

2. **Overlapping bookings** (+2 points): If the same vehicle has two bookings where the time ranges overlap (A.start < B.end AND B.start < A.end), both bookings are flagged. This could indicate double-booking fraud.

3. **Odometer rollback** (+3 points): When bookings for the same vehicle are sorted chronologically, if a later booking's Odo_Start is less than the previous booking's Odo_End, it indicates the odometer was rolled back.

The total score maps to risk levels: 0 = None, 1-2 = Low, 3-4 = Medium, 5+ = High.

---

## Q4: How is fleet utilization calculated?

Fleet utilization is computed as the **total rental hours per vehicle** across all completed rentals:

```
Rental_Hours = (Return_TS - Pickup_TS) in hours
Fleet_Utilization[Vehicle_ID] = SUM(Rental_Hours) for all rentals of that vehicle
```

This gives a direct measure of how much each vehicle is being used. Higher values indicate vehicles that are in high demand and generating more revenue.

---

## Q5: How can the pipeline scale for millions of records?

To scale the current pipeline for millions of records, the following changes would be needed:

1. **Streaming/Chunked Processing**: Instead of loading all records into memory, process the CSV in chunks (e.g., 10,000 rows at a time) using a generator pattern.

2. **Replace dict-based records with pandas DataFrames**: Pandas vectorized operations are 10-100x faster than row-by-row Python dict processing.

3. **Parallel Processing**: Use `multiprocessing` or `concurrent.futures` to parallelize the cleaning stage across CPU cores, since each record's cleaning is independent.

4. **Database Backend**: For deduplication and fraud detection (which require cross-record comparisons), use a database (SQLite for moderate scale, PostgreSQL for large scale) with proper indexing.

5. **Apache Spark/Dask**: For truly massive datasets (billions of records), use distributed computing frameworks that handle partitioning and shuffling automatically.

6. **Incremental Processing**: Instead of regenerating the entire dataset, process only new/changed records using a watermark or change data capture (CDC) pattern.

---

## Q6: What validation rules are applied?

Five validation rules are applied in order:

1. **Required fields**: Reservation_ID, Vehicle_ID, Pickup_TS, Return_TS, Odo_Start, Odo_End, Rate, City must not be null or empty.
2. **Timestamp order**: Return_TS must be strictly after Pickup_TS.
3. **Odometer consistency**: Odo_End must be ≥ Odo_Start.
4. **Fuel range**: Fuel_Level must be between 0.0 and 1.0 inclusive.
5. **Payment validity**: Payment must be one of UPI, CARD, CASH, WALLET.

Records failing any rule are written to `rejected_reservations.csv` with a `Rejection_Reasons` column listing all failures.

---

## Q7: What KPIs are computed?

**Per-record metrics:**
- `Distance_km` = Odo_End − Odo_Start
- `Rental_Hours` = (Return_TS − Pickup_TS) in hours
- `Revenue` = Daily Rate (from the Rate field)
- `Cost_per_km` = Revenue / Distance_km

**Aggregate metrics:**
- Total distance across all rentals
- Total revenue
- Average rental duration (hours)
- Average distance per rental (km)
- Average cost per km
- Fleet utilization: total rental hours per vehicle
- Revenue by city
- Vehicle usage frequency (number of rentals per vehicle)
- Fraud risk distribution (count per risk level)

---

## Q8: What SQL concepts are demonstrated?

The SQL solutions demonstrate:
- **JOINs**: INNER JOIN, LEFT JOIN across multiple tables
- **Aggregations**: COUNT, SUM, AVG, MIN, MAX with GROUP BY
- **Window Functions**: RANK(), LAG(), SUM() OVER (PARTITION BY ... ORDER BY ...)
- **CTEs**: WITH clauses for monthly revenue trends, maintenance vs revenue analysis, customer loyalty segmentation
- **CASE expressions**: Customer segmentation logic
- **COALESCE**: Handling NULL values in aggregations
- **Subqueries**: Nested queries for complex analytics

---

## Q9: Why use Python standard library only?

Using only the standard library ensures:
- **Zero setup**: No `pip install`, no virtual environment needed
- **Portability**: Runs on any system with Python 3.6+
- **Simplicity**: Easy to understand for team members of varying skill levels
- **Focus on fundamentals**: Demonstrates core data engineering concepts without framework abstractions

For production, pandas/polars would be preferred for performance.

---

## Q10: How is the project organized for a 6-person team?

Each developer owns a distinct module with clear interfaces:
- **Dev 1** (Ingestion): Owns data generation and CSV I/O — the entry/exit points
- **Dev 2** (Cleaning): Owns all field-level transformation logic
- **Dev 3** (Validation): Owns business rule enforcement
- **Dev 4** (Processing): Owns deduplication and fraud detection
- **Dev 5** (Analytics): Owns KPI computation and aggregation
- **Dev 6** (SQL): Owns the relational schema and analytical queries

Modules communicate via simple data structures (list of dicts), so each developer can work independently. The pipeline runner orchestrates the modules in sequence.
