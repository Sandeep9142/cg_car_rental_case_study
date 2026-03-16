import pandas as pd

# ANALYTICS ENGINE
from src.analytics.analytics_engine import AnalyticalEngine


print("\n==============================")
print(" ADVANCED ANALYTICS DEMO")
print("==============================\n")


# -------------------------------------------------
# Sample dataset with required columns
# -------------------------------------------------
records = [
{
"Reservation_ID":"RES-001",
"Vehicle_ID":"CAR-01",
"Vehicle_Class": "SUV", 
"Driver_License":"DL12345",
"Pickup_TS":"2026-03-10 10:00",
"Return_TS":"2026-03-10 18:30",
"Booking_TS":"2026-03-09 09:00",

    "Pickup_Lat": 12.9716,
    "Pickup_Lon": 77.5946,
    "Drop_Lat": 12.9352,
    "Drop_Lon": 77.6245,
"Odo_Start":50000,
"Odo_End":50200,
"Fuel_Level":50,
"Rate":1500,
"City":"Bangalore",
"Payment":"UPI",
"Rental_Hours":8,
"Revenue":1500,
"Harsh_Events":2,
"Max_Speed_kmh":110,
"Damage_Flag":0
},

{
"Reservation_ID":"RES-002",
"Vehicle_ID":"CAR-02",
"Vehicle_Class": "Luxury", 
"Driver_License":"DL12345",
"Pickup_TS":"2026-04-02 09:00",
"Return_TS":"2026-04-02 17:00",
"Booking_TS":"2026-04-01 10:00",

    "Pickup_Lat": 13.9716,
    "Pickup_Lon": 71.5946,
    "Drop_Lat": 22.9352,
    "Drop_Lon": 79.6245,
"Odo_Start":30000,
"Odo_End":30250,
"Fuel_Level":60,
"Rate":1200,
"City":"Bangalore",
"Payment":"Card",
"Rental_Hours":8,
"Revenue":1200,
"Harsh_Events":1,
"Max_Speed_kmh":100,
"Damage_Flag":0
}
]

df = pd.DataFrame(records)

engine = AnalyticalEngine(df)


print("1. Utilization calculation")
print(engine.compute_utilization())
print()


print("2. RevPAC calculation")
print(engine.compute_revpac())
print()


print("3. Distance & Cost per km")
print(engine.compute_distance_cost())
print()

print("4. Idle time calculation")
print(engine.compute_idle_time())
print()

print("5. Dynamic pricing features")
print(engine.dynamic_pricing_features())
print()

print("6. Fuel efficiency estimation")
print(engine.fuel_efficiency())
print()


print("7. Damage rate calculation")
print(engine.damage_rate())
print()

print("Damage incidence KPI:")
damage_rate = engine.damage_incidence_rate()
print(f"Damage incidents per 100 rentals: {damage_rate:.2f}")
print()

print("8. Customer cohort retention tagging")
print(engine.cohort_retention())
print()

print("9. Fraud risk scoring")
print(engine.fraud_risk())
print()

print("10. Maintenance due forecast")
print(engine.maintenance_due())
print()

print("11. Overstay detection & penalty")
print(engine.overstay_detection())
print()

print("12. Pickup / Return punctuality stats")
engine.pickup_punctuality()
print(engine.df[["Pickup_Delay", "Return_Delay_Min"]])
print()


print("13. Geo hotspot score")
print(engine.geo_hotspots())
print()

print("14. Upsell opportunity flags")
print(engine.upsell_flags())
print()

print("15. Cancellation rate simulation")
print(engine.cancellation_rate())
print()


print("16. Driver behavior score")
print(engine.driver_behavior())
print()

print("17. Vehicle class mix optimization")
print(engine.vehicle_mix())
print()


print("18. Lead time price elasticity features")
print(engine.price_elasticity())
print()


print("19. Fleet health score")
print(engine.fleet_health())
print()


print("20. Churn likelihood prediction")
print(engine.churn_prediction())
print()

print("====================================")
print(" ALL 20 ANALYTICS SCENARIOS COMPLETE")
print("====================================")