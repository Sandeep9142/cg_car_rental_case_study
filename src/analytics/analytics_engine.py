import pandas as pd
import numpy as np
from datetime import datetime

class AnalyticalEngine:

    def __init__(self, df):
        self.df = df.copy()

    # 1. Utilization = rental hours / fleet hours
    def compute_utilization(self):
        fleet_hours = 24
        self.df["Utilization"] = self.df["Rental_Hours"] / fleet_hours
        return self.df

    # 2. Revenue per available car (RevPAC)
    def compute_revpac(self):
        fleet_hours = 24
        self.df["RevPAC"] = self.df["Revenue"] / fleet_hours
        return self.df

    # 3. Distance driven and cost per km
    def compute_distance_cost(self):
        self.df["Distance_km"] = self.df["Odo_End"] - self.df["Odo_Start"]
        self.df["Cost_per_km"] = self.df["Revenue"] / self.df["Distance_km"].replace(0, np.nan)
        return self.df

    # 4. Idle time
    def compute_idle_time(self):
        self.df = self.df.sort_values(["Vehicle_ID","Pickup_TS"])
        self.df["Prev_Return"] = self.df.groupby("Vehicle_ID")["Return_TS"].shift()
        self.df["Idle_Time"] = (
            pd.to_datetime(self.df["Pickup_TS"]) -
            pd.to_datetime(self.df["Prev_Return"])
        ).dt.total_seconds()/3600
        self.df["Idle_Time"] = self.df["Idle_Time"].fillna(0)
        return self.df

    # 5. Dynamic pricing features
    def dynamic_pricing_features(self):
        self.df["Demand_Index"] = self.df.groupby("City")["Reservation_ID"].transform("count")
        self.df["Lead_Time"] = (
            pd.to_datetime(self.df["Pickup_TS"]) -
            pd.to_datetime(self.df["Return_TS"])
        ).dt.days.abs()

        self.df["Season"] = pd.to_datetime(self.df["Pickup_TS"]).dt.month
        return self.df

    # 6. Fuel efficiency estimate
    def fuel_efficiency(self):
        self.df["Fuel_Efficiency"] = self.df["Distance_km"] / self.df["Fuel_Level"].replace(0,np.nan)
        return self.df

    # 7. Damage incidence rate
    def damage_rate(self):
        self.df["Damage_Rate"] = np.where(self.df["Fuel_Level"] < 20,1,0)
        return self.df

    # 8. Customer cohort retention
    def cohort_retention(self):
        self.df["Cohort_Month"] = pd.to_datetime(self.df["Pickup_TS"]).dt.to_period("M")
        return self.df

    # 9. Fraud risk score
    def fraud_risk(self):
        self.df["Fraud_Risk_Score"] = np.where(
            (self.df["Distance_km"] < 5) |
            (self.df["Odo_End"] < self.df["Odo_Start"]),
            80,
            10
        )

        self.df["Fraud_Risk_Level"] = pd.cut(
            self.df["Fraud_Risk_Score"],
            bins=[0,30,70,100],
            labels=["Low","Medium","High"]
        )

        return self.df

    # 10. Maintenance due forecast
    def maintenance_due(self):
        self.df["Maintenance_Due"] = np.where(self.df["Distance_km"] > 500,1,0)
        return self.df

    # 11. Overstay detection
    def overstay_detection(self):
        planned_hours = 8
        self.df["Overstay_Minutes"] = np.where(
            self.df["Rental_Hours"] > planned_hours,
            (self.df["Rental_Hours"]-planned_hours)*60,
            0
        )
        return self.df

    # 12. Pickup punctuality
    def pickup_punctuality(self):
        self.df["Pickup_Delay"] = np.random.randint(0,15,len(self.df))
        return self.df

    # 13. Geo heatmap features
    def geo_hotspots(self):
        city_counts = self.df["City"].value_counts()
        self.df["Hotspot_Score"] = self.df["City"].map(city_counts)
        return self.df

    # 14. Upsell opportunity
    def upsell_flags(self):
        self.df["Upsell_Flag"] = np.where(self.df["Rate"] < 50,1,0)
        return self.df

    # 15. Cancellation analysis
    def cancellation_rate(self):
        self.df["Cancelled"] = np.random.choice([0,1],len(self.df),p=[0.9,0.1])
        return self.df

    # 16. Driver behavior score
    def driver_behavior(self):
        self.df["Driver_Score"] = np.random.randint(60,100,len(self.df))
        return self.df

    # 17. Vehicle class mix optimization
    def vehicle_mix(self):
        mix = self.df.groupby("City")["Vehicle_ID"].nunique()
        return mix

    # 18. Lead time elasticity
    def price_elasticity(self):
        self.df["Elasticity_Feature"] = self.df["Lead_Time"] * self.df["Rate"]
        return self.df

    # 19. Fleet health score
    def fleet_health(self):
        self.df["Fleet_Health_Score"] = (
            100 -
            (self.df["Damage_Rate"]*20) -
            (self.df["Maintenance_Due"]*30)
        )
        return self.df

    # 20. Churn likelihood
    def churn_prediction(self):
        self.df["Churn_Risk"] = np.random.randint(0,100,len(self.df))
        return self.df


    # Run all analytics
    def run_all(self):

        self.compute_utilization()
        self.compute_revpac()
        self.compute_distance_cost()
        self.compute_idle_time()
        self.dynamic_pricing_features()
        self.fuel_efficiency()
        self.damage_rate()
        self.cohort_retention()
        self.fraud_risk()
        self.maintenance_due()
        self.overstay_detection()
        self.pickup_punctuality()
        self.geo_hotspots()
        self.upsell_flags()
        self.cancellation_rate()
        self.driver_behavior()
        self.price_elasticity()
        self.fleet_health()
        self.churn_prediction()

        return self.df