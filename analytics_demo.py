import pandas as pd

# ANALYTICS ENGINE
from src.analytics.analytics_engine import AnalyticalEngine


print("\n==============================")
print(" ADVANCED ANALYTICS DEMO")
print("==============================\n")


# Sample dataset
records = [
    {
        "Reservation_ID": "RES-001",
        "Vehicle_ID": "CAR-01",
        "Pickup_TS": "2026-03-10 10:00",
        "Return_TS": "2026-03-10 18:00",
        "Odo_Start": 50000,
        "Odo_End": 50200,
        "Fuel_Level": 50,
        "Rate": 1500,
        "City": "Bangalore",
        "Payment": "UPI",
        "Rental_Hours": 8,
        "Revenue": 1500,
    }
]

df = pd.DataFrame(records)

engine = AnalyticalEngine(df)


# -------------------------------------------------
# Scenario 1
# -------------------------------------------------
print("1. Utilization calculation")
print(engine.compute_utilization())
print()


# -------------------------------------------------
# Scenario 2
# -------------------------------------------------
print("2. RevPAC calculation")
print(engine.compute_revpac())
print()


# -------------------------------------------------
# Scenario 3
# -------------------------------------------------
print("3. Distance & Cost per km")
print(engine.compute_distance_cost())
print()


# -------------------------------------------------
# Scenario 4
# -------------------------------------------------
print("4. Idle time calculation")
print(engine.compute_idle_time())
print()


# -------------------------------------------------
# Scenario 5
# -------------------------------------------------
print("5. Dynamic pricing features")
print(engine.dynamic_pricing_features())
print()


# -------------------------------------------------
# Scenario 6
# -------------------------------------------------
print("6. Fuel efficiency estimation")
print(engine.fuel_efficiency())
print()


# -------------------------------------------------
# Scenario 7
# -------------------------------------------------
print("7. Damage rate calculation")
print(engine.damage_rate())
print()


# -------------------------------------------------
# Scenario 8
# -------------------------------------------------
print("8. Cohort retention tagging")
print(engine.cohort_retention())
print()


# -------------------------------------------------
# Scenario 9
# -------------------------------------------------
print("9. Fraud risk scoring")
print(engine.fraud_risk())
print()


# -------------------------------------------------
# Scenario 10
# -------------------------------------------------
print("10. Maintenance due forecast")
print(engine.maintenance_due())
print()


# -------------------------------------------------
# Scenario 11
# -------------------------------------------------
print("11. Overstay detection")
print(engine.overstay_detection())
print()


# -------------------------------------------------
# Scenario 12
# -------------------------------------------------
print("12. Pickup delay stats")
print(engine.pickup_punctuality())
print()


# -------------------------------------------------
# Scenario 13
# -------------------------------------------------
print("13. Geo hotspot score")
print(engine.geo_hotspots())
print()


# -------------------------------------------------
# Scenario 14
# -------------------------------------------------
print("14. Upsell opportunity flags")
print(engine.upsell_flags())
print()


# -------------------------------------------------
# Scenario 15
# -------------------------------------------------
print("15. Cancellation simulation")
print(engine.cancellation_rate())
print()


# -------------------------------------------------
# Scenario 16
# -------------------------------------------------
print("16. Driver behavior score")
print(engine.driver_behavior())
print()


# -------------------------------------------------
# Scenario 17
# -------------------------------------------------
print("17. Vehicle mix optimization")
print(engine.vehicle_mix())
print()


# -------------------------------------------------
# Scenario 18
# -------------------------------------------------
print("18. Lead time price elasticity")
print(engine.price_elasticity())
print()


# -------------------------------------------------
# Scenario 19
# -------------------------------------------------
print("19. Fleet health score")
print(engine.fleet_health())
print()


# -------------------------------------------------
# Scenario 20
# -------------------------------------------------
print("20. Churn risk prediction")
print(engine.churn_prediction())
print()


print("ANALYTICS DEMO COMPLETE")