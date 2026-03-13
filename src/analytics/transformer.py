from datetime import datetime
from collections import defaultdict


TS_FORMAT = "%Y-%m-%d %H:%M"


# SCENARIO 19 — Rate Plan Mapping
RATE_PLAN_MAP = {
    "eco": "Economy",
    "economy": "Economy",
    "budget": "Economy",
    "std": "Standard",
    "standard": "Standard",
    "regular": "Standard",
    "prem": "Premium",
    "premium": "Premium",
    "exec": "Premium",
    "lux": "Luxury",
    "luxury": "Luxury",
    "vip": "Luxury",
}


def map_rate_plan(record):

    plan = str(record.get("Rate_Plan", "")).strip().lower()

    record["Rate_Plan_Clean"] = RATE_PLAN_MAP.get(plan, "Standard")

    return record

# SCENARIO 11 — Refueling Detection
def detect_refueling(record):
    try:

        distance = int(record.get("Distance_km", 0))
        fuel = float(record.get("Fuel_Level", 0))

        if distance > 200 and fuel > 0.8:
            record["Refuel_Event"] = True
        else:
            record["Refuel_Event"] = False

    except:
        record["Refuel_Event"] = False

    return record

def compute_record_metrics(record):

    rec = record.copy()

    # Distance
    try:
        odo_start = int(rec.get("Odo_Start", 0))
        odo_end = int(rec.get("Odo_End", 0))

        rec["Distance_km"] = max(0, odo_end - odo_start)

    except:
        rec["Distance_km"] = 0

    # Rental duration
    try:
        pickup_dt = datetime.strptime(str(rec.get("Pickup_TS")), TS_FORMAT)
        return_dt = datetime.strptime(str(rec.get("Return_TS")), TS_FORMAT)

        delta = return_dt - pickup_dt

        rec["Rental_Hours"] = round(delta.total_seconds() / 3600, 2)

    except:
        rec["Rental_Hours"] = 0

    # Revenue
    try:
        rec["Revenue"] = int(rec.get("Rate", 0))
    except:
        rec["Revenue"] = 0

    # Cost per km
    if rec["Distance_km"] > 0:
        rec["Cost_per_km"] = round(rec["Revenue"] / rec["Distance_km"], 2)
    else:
        rec["Cost_per_km"] = 0

    # Scenario 19
    rec = map_rate_plan(rec)

    # Scenario 11
    rec = detect_refueling(rec)

    return rec


# Fleet Utilization

def compute_fleet_utilization(records):

    utilization = defaultdict(float)

    for rec in records:

        vid = rec.get("Vehicle_ID", "")
        hours = rec.get("Rental_Hours", 0)

        utilization[vid] += hours

    return dict(utilization)


# Revenue by City
def compute_revenue_by_city(records):

    revenue = defaultdict(int)

    for rec in records:

        city = rec.get("City", "Unknown")
        revenue[city] += rec.get("Revenue", 0)

    return dict(revenue)


# Average Rental Duration

def compute_avg_rental_duration(records):

    if not records:
        return 0

    total = sum(r.get("Rental_Hours", 0) for r in records)

    return round(total / len(records), 2)


# Vehicle Usage Frequency

def compute_vehicle_usage_frequency(records):

    freq = defaultdict(int)

    for rec in records:

        vid = rec.get("Vehicle_ID", "")
        freq[vid] += 1

    return dict(freq)


def transform_all(records):

    enriched = [compute_record_metrics(r) for r in records]

    fleet_util = compute_fleet_utilization(enriched)
    revenue_by_city = compute_revenue_by_city(enriched)
    avg_duration = compute_avg_rental_duration(enriched)
    usage_freq = compute_vehicle_usage_frequency(enriched)

    top_vehicles = sorted(fleet_util.items(), key=lambda x: x[1], reverse=True)[:10]
    top_cities = sorted(revenue_by_city.items(), key=lambda x: x[1], reverse=True)

    fraud_dist = defaultdict(int)

    for rec in enriched:

        level = rec.get("Fraud_Risk_Level", "None")
        fraud_dist[level] += 1

    summary = {

        "total_records": len(enriched),

        "total_distance_km": sum(r.get("Distance_km", 0) for r in enriched),

        "total_revenue": sum(r.get("Revenue", 0) for r in enriched),

        "avg_rental_hours": avg_duration,

        "avg_distance_km": round(
            sum(r.get("Distance_km", 0) for r in enriched) / max(len(enriched), 1), 2
        ),

        "avg_cost_per_km": round(
            sum(r.get("Cost_per_km", 0) for r in enriched) / max(len(enriched), 1), 2
        ),

        "top_vehicles_by_utilization": top_vehicles,

        "revenue_by_city": dict(top_cities),

        "vehicle_usage_frequency": dict(
            sorted(usage_freq.items(), key=lambda x: x[1], reverse=True)[:10]
        ),

        "fraud_risk_distribution": dict(fraud_dist),
    }

    return enriched, summary