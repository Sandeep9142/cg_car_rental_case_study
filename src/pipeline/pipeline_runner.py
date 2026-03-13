"""
Pipeline Runner Module
Orchestrates the full data cleaning and transformation pipeline.

Pipeline stages:
1. Generate raw dataset
2. Load raw data
3. Clean records
4. Validate records (split valid / rejected)
5. Deduplicate and detect fraud
6. Compute analytics and KPIs
7. Save outputs
8. Print summary
"""

import os
import sys

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


# Output field order for cleaned reservations
CLEANED_FIELDS = [
    "Reservation_ID", "Vehicle_ID", "Pickup_TS", "Return_TS",
    "Odo_Start", "Odo_End", "Fuel_Level", "Rate", "City", "Payment",
    "Fraud_Risk_Score", "Fraud_Risk_Level",
    "Distance_km", "Rental_Hours", "Revenue", "Cost_per_km",

     # Advanced analytics fields
    "Utilization",
    "RevPAC",
    "Idle_Time",
    "Fuel_Efficiency",
    "Damage_Rate",
    "Maintenance_Due",
    "Overstay_Minutes",
    "Pickup_Delay",
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
    """
    Execute the full data pipeline.

    Args:
        project_root: Root directory of the project.
                      Defaults to two levels up from this file.

    Returns:
        dict: Summary statistics from the pipeline run.
    """
    if project_root is None:
        project_root = PROJECT_ROOT

    raw_path = os.path.join(project_root, "data", "raw", "car_rental_raw.csv")
    cleaned_path = os.path.join(project_root, "data", "output", "cleaned_reservations.csv")
    rejected_path = os.path.join(project_root, "data", "output", "rejected_reservations.csv")
    metrics_path = os.path.join(project_root, "data", "output", "metrics_report.csv")

    # Ensure output directories exist
    for path in [cleaned_path, rejected_path, metrics_path]:
        os.makedirs(os.path.dirname(path), exist_ok=True)

    # ── Stage 1: Generate dataset ──
    print("=" * 60)
    print("  CAR RENTAL DATA CLEANING & TRANSFORMATION PIPELINE")
    print("=" * 60)
    print()

    print("[1/7] Generating raw dataset...")
    total_generated = generate_dataset(raw_path)
    print(f"       Generated {total_generated} records → {raw_path}")

    # ── Stage 2: Load raw data ──
    print("[2/7] Loading raw data...")
    raw_records = load_csv(raw_path)
    print(f"       Loaded {len(raw_records)} records")

    # ── Stage 3: Clean data ──
    print("[3/7] Cleaning data...")
    cleaned_records = clean_all(raw_records)
    print(f"       Cleaned {len(cleaned_records)} records")

    # ── Stage 4: Validate records ──
    print("[4/7] Validating records...")
    valid_records, rejected_records = validate_all(cleaned_records)
    print(f"       Valid: {len(valid_records)} | Rejected: {len(rejected_records)}")

    # ── Stage 5: Deduplicate and detect fraud ──
    print("[5/7] Deduplicating and detecting fraud...")
    processed_records, num_duplicates = deduplicate_and_flag(valid_records)
    print(f"       Duplicates removed: {num_duplicates}")
    print(f"       Records after dedup: {len(processed_records)}")

    # ── Stage 6: Compute analytics ──
    print("[6/7] Computing analytics and KPIs...")
    enriched_records, summary = transform_all(processed_records)
    print(f"       Metrics computed for {len(enriched_records)} records")

    # ── Stage 6.1: Advanced analytics scenarios ──
    print("       Running advanced analytics scenarios...")

    
    import pandas as pd

    df = pd.DataFrame(enriched_records)

    engine = AnalyticalEngine(df)

    analytics_df = engine.run_all()

    # Save analytics output
    analytics_df.to_csv("data/output/analytics_output.csv", index=False)

    # Convert updated dataframe back to records
    enriched_records = analytics_df.to_dict(orient="records")

    print("Advanced analytics completed")

    # ── Stage 7: Save outputs ──
    print("[7/7] Saving output files...")
    save_csv(enriched_records, cleaned_path, fieldnames=CLEANED_FIELDS)
    print(f"       Cleaned data → {cleaned_path}")

    save_csv(rejected_records, rejected_path, fieldnames=REJECTED_FIELDS)
    print(f"       Rejected data → {rejected_path}")

    # Save metrics report (subset of fields)
    metrics_data = []
    for rec in enriched_records:
        metrics_data.append({k: rec.get(k, "") for k in METRICS_FIELDS})
    save_csv(metrics_data, metrics_path, fieldnames=METRICS_FIELDS)
    print(f"       Metrics report → {metrics_path}")

    # ── Summary ──
    print()
    print("=" * 60)
    print("  PIPELINE SUMMARY")
    print("=" * 60)
    print(f"  Total records generated:    {total_generated}")
    print(f"  Invalid records removed:    {len(rejected_records)}")
    print(f"  Duplicates removed:         {num_duplicates}")
    print(f"  Clean records:              {len(enriched_records)}")
    print(f"  Total distance (km):        {summary['total_distance_km']:,}")
    print(f"  Total revenue:              {summary['total_revenue']:,}")
    print(f"  Avg rental duration (hrs):  {summary['avg_rental_hours']}")
    print(f"  Avg distance (km):          {summary['avg_distance_km']}")
    print(f"  Avg cost per km:            {summary['avg_cost_per_km']}")
    print()

    print("  Revenue by City:")
    for city, rev in summary["revenue_by_city"].items():
        print(f"    {city:<15} {rev:>10,}")
    print()

    print("  Top 10 Vehicles by Utilization (hours):")
    for vid, hours in summary["top_vehicles_by_utilization"]:
        print(f"    {vid:<12} {hours:>10.1f} hrs")
    print()

    print("  Fraud Risk Distribution:")
    for level, count in summary["fraud_risk_distribution"].items():
        print(f"    {level:<10} {count:>6}")
    print()
    print("=" * 60)
    print("  Pipeline completed successfully!")
    print("=" * 60)

    return {
        "total_generated": total_generated,
        "invalid_removed": len(rejected_records),
        "duplicates_removed": num_duplicates,
        "clean_records": len(enriched_records),
        "summary": summary,
    }
