import os
import sys
import time
import pandas as pd

# Add project root to path for imports
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.ingestion.dataset_generator import generate_dataset
from src.ingestion.reader import load_csv, save_csv
from src.cleaning.cleaner import clean_all
from src.validation.validator import validate_all
from src.processing.deduplicator import deduplicate_and_flag
from src.analytics.transformer import transform_all
from src.analytics.analytics_engine import AnalyticalEngine


CLEANED_FIELDS = [
    "Reservation_ID", "Vehicle_ID",
    "Vehicle_Class", "Booking_TS",
    "Pickup_TS", "Return_TS",

    "Pickup_Lat", "Pickup_Lon",
    "Drop_Lat", "Drop_Lon",

    "Odo_Start", "Odo_End", "Fuel_Level", "Rate", "City", "Payment",
    "Fraud_Risk_Score", "Fraud_Risk_Level",
    "Distance_km", "Rental_Hours", "Revenue", "Cost_per_km",

    "Utilization",
    "RevPAC",
    "Idle_Time",
    "Fuel_Efficiency",
    "Damage_Rate",
    "Maintenance_Due",
    "Overstay_Minutes",
    "Pickup_Delay",
    "Driver_License",
    "Driver_Score",
    "Fleet_Health_Score",
    "Churn_Risk",
]

REJECTED_FIELDS = [
    "Reservation_ID", "Vehicle_ID", "Pickup_TS", "Return_TS",
    "Odo_Start", "Odo_End", "Fuel_Level", "Rate", "City", "Payment",
    "Rejection_Reasons",
]

METRICS_FIELDS = [
    "Reservation_ID", "Vehicle_ID", "City", "Distance_km",
    "Rental_Hours", "Revenue", "Cost_per_km",
    "Fraud_Risk_Score", "Fraud_Risk_Level",
]


def run_pipeline(project_root=None):

    if project_root is None:
        project_root = PROJECT_ROOT

    raw_path = os.path.join(project_root, "data", "raw", "car_rental_raw.csv")
    cleaned_path = os.path.join(project_root, "data", "output", "cleaned_reservations.csv")
    rejected_path = os.path.join(project_root, "data", "output", "rejected_reservations.csv")
    metrics_path = os.path.join(project_root, "data", "output", "metrics_report.csv")
    analytics_path = os.path.join(project_root, "data", "output", "analytics_output.csv")

    for path in [cleaned_path, rejected_path, metrics_path, analytics_path]:
        os.makedirs(os.path.dirname(path), exist_ok=True)

    print("\n" + "=" * 60)
    print("🚗 CAR RENTAL DATA ENGINEERING PIPELINE")
    print("=" * 60 + "\n")

    pipeline_start = time.time()

    # ── Stage 1: Generate dataset ──
    stage_start = time.time()
    print("▶ Stage 1/7: Generating raw dataset...")
    total_generated = generate_dataset(raw_path)
    print(f"       Generated {total_generated} records → {raw_path}")
    print(f"       Completed in {time.time() - stage_start:.2f} seconds\n")

    # ── Stage 2: Load raw data ──
    stage_start = time.time()
    print("▶ Stage 2/7: Loading raw data...")
    raw_records = load_csv(raw_path)
    print(f"       Loaded {len(raw_records)} records")
    print(f"       Completed in {time.time() - stage_start:.2f} seconds\n")

    # ── Stage 3: Clean data ──
    stage_start = time.time()
    print("▶ Stage 3/7: Cleaning data...")
    cleaned_records = clean_all(raw_records)
    print(f"       Cleaned {len(cleaned_records)} records")
    print(f"       Completed in {time.time() - stage_start:.2f} seconds\n")

    # ── Stage 4: Validate records ──
    stage_start = time.time()
    print("▶ Stage 4/7: Validating records...")
    valid_records, rejected_records = validate_all(cleaned_records)
    print(f"       Valid: {len(valid_records)} | Rejected: {len(rejected_records)}")
    print(f"       Completed in {time.time() - stage_start:.2f} seconds\n")

    # ── Stage 5: Deduplicate and detect fraud ──
    stage_start = time.time()
    print("▶ Stage 5/7: Deduplicating and detecting fraud...")
    processed_records, num_duplicates = deduplicate_and_flag(valid_records)
    print(f"       Duplicates removed: {num_duplicates}")
    print(f"       Records after dedup: {len(processed_records)}")
    print(f"       Completed in {time.time() - stage_start:.2f} seconds\n")

    # ── Stage 6: Compute analytics ──
    stage_start = time.time()
    print("▶ Stage 6/7: Computing analytics and KPIs...")
    enriched_records, summary = transform_all(processed_records)
    print(f"       Metrics computed for {len(enriched_records)} records")
    print(f"       Completed in {time.time() - stage_start:.2f} seconds\n")

    # ── Stage 6.1: Advanced analytics ──
    stage_start = time.time()
    print("▶ Running advanced analytics scenarios...")

    df = pd.DataFrame(enriched_records)

    engine = AnalyticalEngine(df)

    analytics_df = engine.run_all()

    print("       Damage incidence per 100 rentals:", engine.damage_incidence_rate())

    analytics_df.to_csv(analytics_path, index=False)

    enriched_records = analytics_df.to_dict(orient="records")

    print(f"       Advanced analytics completed → {len(analytics_df)} records")
    print(f"       Saved analytics output → {analytics_path}")
    print(f"       Completed in {time.time() - stage_start:.2f} seconds\n")

    # ── Stage 7: Save outputs ──
    stage_start = time.time()
    print("▶ Stage 7/7: Saving output files...")

    save_csv(enriched_records, cleaned_path, fieldnames=CLEANED_FIELDS)
    print(f"       Cleaned data → {cleaned_path}")

    save_csv(rejected_records, rejected_path, fieldnames=REJECTED_FIELDS)
    print(f"       Rejected data → {rejected_path}")

    metrics_data = [
        {k: rec.get(k, "") for k in METRICS_FIELDS}
        for rec in enriched_records
    ]

    save_csv(metrics_data, metrics_path, fieldnames=METRICS_FIELDS)
    print(f"       Metrics report → {metrics_path}")

    print(f"       Completed in {time.time() - stage_start:.2f} seconds\n")

    total_time = time.time() - pipeline_start

    print("=" * 60)
    print("📊 PIPELINE SUMMARY")
    print("=" * 60)

    print(f"Total records generated:     {total_generated}")
    print(f"Invalid records removed:     {len(rejected_records)}")
    print(f"Duplicates removed:          {num_duplicates}")
    print(f"Clean records:               {len(enriched_records)}")

    print(f"\nTotal distance (km):         {summary['total_distance_km']:,}")
    print(f"Total revenue:               {summary['total_revenue']:,}")
    print(f"Avg rental duration (hrs):   {summary['avg_rental_hours']}")
    print(f"Avg distance (km):           {summary['avg_distance_km']}")
    print(f"Avg cost per km:             {summary['avg_cost_per_km']}")

    print("\nRevenue by City:")
    for city, rev in summary["revenue_by_city"].items():
        print(f"  {city:<15} {rev:>10,}")

    print("\nTop 10 Vehicles by Utilization (hours):")
    for vid, hours in summary["top_vehicles_by_utilization"]:
        print(f"  {vid:<12} {hours:>10.1f} hrs")

    print("\nFraud Risk Distribution:")
    for level, count in summary["fraud_risk_distribution"].items():
        print(f"  {level:<10} {count:>6}")

    print("\nOutput Files:")
    print(f"  Cleaned Data   → {cleaned_path}")
    print(f"  Rejected Data  → {rejected_path}")
    print(f"  Metrics Report → {metrics_path}")
    print(f"  Analytics Data → {analytics_path}")

    print("\nTotal Pipeline Runtime: {:.2f} seconds".format(total_time))

    print("\n" + "=" * 60)
    print("✅ Pipeline completed successfully!")
    print("=" * 60)

    return {
        "total_generated": total_generated,
        "invalid_removed": len(rejected_records),
        "duplicates_removed": num_duplicates,
        "clean_records": len(enriched_records),
        "summary": summary,
    }