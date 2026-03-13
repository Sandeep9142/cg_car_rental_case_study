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
    
   # Repositioning analytics
    def repositioning_distance(self):

        # convert lat/lon to numeric
        self.df["Pickup_Lat"] = pd.to_numeric(self.df["Pickup_Lat"], errors="coerce")
        self.df["Pickup_Lon"] = pd.to_numeric(self.df["Pickup_Lon"], errors="coerce")
        self.df["Drop_Lat"] = pd.to_numeric(self.df["Drop_Lat"], errors="coerce")
        self.df["Drop_Lon"] = pd.to_numeric(self.df["Drop_Lon"], errors="coerce")

        self.df = self.df.sort_values(["Vehicle_ID","Pickup_TS"])

        self.df["Prev_Drop_Lat"] = self.df.groupby("Vehicle_ID")["Drop_Lat"].shift()
        self.df["Prev_Drop_Lon"] = self.df.groupby("Vehicle_ID")["Drop_Lon"].shift()

        # calculate reposition distance
        self.df["Reposition_Distance"] = (
            (self.df["Pickup_Lat"] - self.df["Prev_Drop_Lat"])**2 +
            (self.df["Pickup_Lon"] - self.df["Prev_Drop_Lon"])**2
        )**0.5

        self.df["Reposition_Distance"] = self.df["Reposition_Distance"].fillna(0)

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

        self.df["Damage_Flag"] = np.where(self.df["Fuel_Level"] < 20, 1, 0)

        return self.df


    def damage_incidence_rate(self):

        # ensure flag exists
        if "Damage_Flag" not in self.df.columns:
            self.damage_rate()

        total_rentals = len(self.df)
        damage_cases = self.df["Damage_Flag"].sum()

        rate = (damage_cases / total_rentals) * 100 if total_rentals > 0 else 0

        self.damage_incidence_per_100 = round(rate, 2)

        return self.damage_incidence_per_100

    # 8. Customer cohort retention
    def cohort_retention(self):

        self.df["Pickup_TS"] = pd.to_datetime(self.df["Pickup_TS"])

        # customer first rental month
        self.df["Cohort_Month"] = self.df.groupby("Driver_License")["Pickup_TS"].transform("min").dt.to_period("M")

        # activity month
        self.df["Activity_Month"] = self.df["Pickup_TS"].dt.to_period("M")

        # months since first rental
        self.df["Cohort_Index"] = (
            (self.df["Activity_Month"].dt.year - self.df["Cohort_Month"].dt.year) * 12
            + (self.df["Activity_Month"].dt.month - self.df["Cohort_Month"].dt.month)
        )

        return self.df
    

    def nps_rollups(self):

        # simulate rating if not present
        if "NPS_Score" not in self.df.columns:
            self.df["NPS_Score"] = np.random.randint(0, 11, len(self.df))

        promoters = (self.df["NPS_Score"] >= 9).sum()
        detractors = (self.df["NPS_Score"] <= 6).sum()
        total = len(self.df)

        promoter_pct = promoters / total * 100
        detractor_pct = detractors / total * 100

        self.nps_score = round(promoter_pct - detractor_pct, 2)

        return self.nps_score

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

        # 10. Maintenance due forecast (km/time based)
    def maintenance_due(self):

        km_condition = self.df["Distance_km"] > 500
        time_condition = self.df["Rental_Hours"] > 72

        self.df["Maintenance_Due"] = np.where(
            km_condition | time_condition,
            1,
            0
        )

        return self.df
    
    #11. Overstay detection and penalty calculation.
    def overstay_detection(self):
        planned_hours = 8
        penalty_rate_per_hour = 10  # example, you can change

        # Calculate overstay minutes
        self.df["Overstay_Minutes"] = np.where(
            self.df["Rental_Hours"] > planned_hours,
            (self.df["Rental_Hours"] - planned_hours) * 60,
            0
        )

        # Calculate overstay penalty
        self.df["Overstay_Penalty"] = np.where(
            self.df["Overstay_Minutes"] > 0,
            (self.df["Overstay_Minutes"] / 60) * penalty_rate_per_hour,
            0
        )

        return self.df

    # 12. Pickup/Return punctuality stats
    def pickup_punctuality(self):

        # Convert timestamps
        self.df["Pickup_TS"] = pd.to_datetime(self.df["Pickup_TS"])
        self.df["Return_TS"] = pd.to_datetime(self.df["Return_TS"])

        # Planned return time = Pickup_TS + Rental_Hours
        self.df["Planned_Return_TS"] = self.df["Pickup_TS"] + pd.to_timedelta(self.df["Rental_Hours"], unit="h")

        # Pickup delay: assume 0 if no separate planned pickup, else 0 for demonstration
        self.df["Pickup_Delay"] = 0  # placeholder since dataset has no planned pickup

        # Return delay in minutes
        self.df["Return_Delay_Min"] = (self.df["Return_TS"] - self.df["Planned_Return_TS"]).dt.total_seconds() / 60

        # Compute punctuality stats
        self.avg_return_delay = round(self.df["Return_Delay_Min"].mean(), 2)
        self.on_time_returns = round((self.df["Return_Delay_Min"] <= 0).mean() * 100, 2)  # % on-time or early

        return self.df

    # 13. Geo heatmap hotspots
    def geo_hotspots(self):

        # pickup hotspots
        pickup_counts = (
            self.df
            .groupby(["Pickup_Lat","Pickup_Lon"])
            .size()
            .reset_index(name="Pickup_Hotspot")
        )

        # drop hotspots
        drop_counts = (
            self.df
            .groupby(["Drop_Lat","Drop_Lon"])
            .size()
            .reset_index(name="Drop_Hotspot")
        )

        # merge back
        self.df = self.df.merge(
            pickup_counts,
            on=["Pickup_Lat","Pickup_Lon"],
            how="left"
        )

        self.df = self.df.merge(
            drop_counts,
            on=["Drop_Lat","Drop_Lon"],
            how="left"
        )

        return self.df

    # 14. Upsell / Cross-sell opportunity flags
    def upsell_flags(self):

        self.df["Upsell_Flag"] = np.where(
            (self.df["Rate"] <= 1000) |
            (self.df["Rental_Hours"] > 24) |
            (self.df["Distance_km"] > 300),
            1,
            0
        )

        return self.df

  # 15. Cancellation rate and reasons analysis
    def cancellation_rate(self):

        # cancellation flag
        self.df["Cancelled"] = np.random.choice(
            [0,1],
            len(self.df),
            p=[0.9,0.1]
        )

        # cancellation reasons
        reasons = [
            "Customer Cancelled",
            "Vehicle Unavailable",
            "Payment Failure",
            "Price Too High",
            "Duplicate Booking"
        ]

        self.df["Cancellation_Reason"] = np.where(
            self.df["Cancelled"] == 1,
            np.random.choice(reasons, len(self.df)),
            "None"
        )

        return self.df

  # 16. Driver behavior scoring from telematics
    def driver_behavior(self):

        score = 100

        # convert columns to numeric
        self.df["Harsh_Events"] = pd.to_numeric(self.df["Harsh_Events"], errors="coerce")
        
        # remove "kmh" text then convert
        self.df["Max_Speed_kmh"] = (
            self.df["Max_Speed_kmh"]
            .astype(str)
            .str.replace("kmh","",regex=False)
            .str.strip()
        )
        self.df["Max_Speed_kmh"] = pd.to_numeric(self.df["Max_Speed_kmh"], errors="coerce")

        self.df["Damage_Flag"] = pd.to_numeric(self.df["Damage_Flag"], errors="coerce")

        # penalties
        harsh_penalty = self.df["Harsh_Events"] * 2
        speed_penalty = np.where(self.df["Max_Speed_kmh"] > 120, 10, 0)
        damage_penalty = self.df["Damage_Flag"] * 20

        # final score
        self.df["Driver_Score"] = score - harsh_penalty - speed_penalty - damage_penalty

        return self.df

    # 17. Vehicle class mix optimization
    def vehicle_mix(self):

        mix = (
            self.df
            .groupby(["City","Vehicle_Class"])
            .size()
            .unstack(fill_value=0)
        )

        return mix

    # 18. Lead-time price elasticity features
    def price_elasticity(self):

        # convert timestamps
        self.df["Pickup_TS"] = pd.to_datetime(self.df["Pickup_TS"], errors="coerce")
        self.df["Booking_TS"] = pd.to_datetime(self.df["Booking_TS"], errors="coerce")

        # calculate lead time (hours)
        self.df["Lead_Time"] = (
            self.df["Pickup_TS"] - self.df["Booking_TS"]
        ).dt.total_seconds() / 3600

        # ensure rate numeric
        self.df["Rate"] = pd.to_numeric(self.df["Rate"], errors="coerce")

        # elasticity feature
        self.df["Elasticity_Feature"] = self.df["Lead_Time"] * self.df["Rate"]

        return self.df
    
    # 19. Fleet health score
    def fleet_health(self):

        self.df["Damage_Flag"] = pd.to_numeric(self.df["Damage_Flag"], errors="coerce")
        self.df["Maintenance_Due"] = pd.to_numeric(self.df["Maintenance_Due"], errors="coerce")
        self.df["Distance_km"] = pd.to_numeric(self.df["Distance_km"], errors="coerce")

        usage_penalty = np.where(self.df["Distance_km"] > 500, 10, 0)

        self.df["Fleet_Health_Score"] = (
            100
            - (self.df["Damage_Flag"] * 20)
            - (self.df["Maintenance_Due"] * 30)
            - usage_penalty
        )

        return self.df

   # 20. Churn likelihood
    def churn_prediction(self):

        self.df["Driver_Score"] = pd.to_numeric(self.df["Driver_Score"], errors="coerce")
        self.df["Pickup_Delay"] = pd.to_numeric(self.df["Pickup_Delay"], errors="coerce")

        churn_score = (
            (100 - self.df["Driver_Score"]) * 0.4 +
            (self.df["Pickup_Delay"]) * 0.3 +
            (self.df["Damage_Flag"] * 20) * 0.3
        )

        self.df["Churn_Risk"] = churn_score.clip(0,100)

        return self.df

    # Run all analytics
    def run_all(self):

        self.compute_utilization()
        self.compute_revpac()
        self.compute_distance_cost()
        self.compute_idle_time()
        self.repositioning_distance()
        self.dynamic_pricing_features()
        self.fuel_efficiency()
        self.damage_rate()
        self.cohort_retention()
        self.cohort_retention()
        self.fraud_risk()
        self.maintenance_due()
        self.overstay_detection()
        self.pickup_punctuality()
        self.geo_hotspots()
        self.upsell_flags()
        self.cancellation_rate()
        self.driver_behavior()
        self.vehicle_mix()
        self.price_elasticity()
        self.fleet_health()
        self.churn_prediction()

        return self.df