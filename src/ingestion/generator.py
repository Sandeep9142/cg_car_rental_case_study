# # """
# # Advanced Car Rental Dataset Generator
# # -------------------------------------

# # Generates messy rental data covering 20 cleaning scenarios.

# # Columns (21):
# # Reservation_ID
# # Vehicle_ID
# # Pickup_TS
# # Return_TS
# # Odo_Start
# # Odo_End
# # Fuel_Level
# # Rate
# # City
# # Payment
# # Driver_License
# # Promo_Code
# # GPS_Lat
# # GPS_Lon
# # Max_Speed_kmh
# # Harsh_Events
# # Notes
# # Customer_Feedback
# # Rate_Plan
# # GST_Amount
# # Total_Amount
# # """

# # import csv
# # import random
# # from datetime import datetime, timedelta


# # # -----------------------------
# # # CONSTANTS
# # # -----------------------------

# # VEHICLES = [f"CAR-{str(i).zfill(2)}" for i in range(1, 31)]

# # CITIES = ["Bengaluru", "Mumbai", "Delhi", "Hyderabad", "Chennai", "Kolkata"]

# # CITY_VARIANTS = {
# #     "Bengaluru": ["Bengaluru", "blr", "Bangalore"],
# #     "Mumbai": ["Mumbai", "mumbai"],
# #     "Delhi": ["Delhi", "delhi"],
# #     "Hyderabad": ["Hyderabad", "HYD"],
# #     "Chennai": ["Chennai", "CHENNAI"],
# #     "Kolkata": ["Kolkata", "kolkata"],
# # }

# # PAYMENTS = ["UPI", "CARD", "CASH", "WALLET"]

# # PROMOS_VALID = ["SAVE10", "DISC15", "FLAT100"]
# # PROMOS_INVALID = ["BOGUS99", "TEST01"]

# # RATE_VALUES = [800, 1000, 1200, 1500, 2000, 2500, 3000]

# # BASE_DATE = datetime(2026, 1, 1)


# # # -----------------------------
# # # HELPERS
# # # -----------------------------

# # def random_timestamp():
# #     days = random.randint(0, 90)
# #     hours = random.randint(0, 23)
# #     mins = random.randint(0, 59)
# #     return BASE_DATE + timedelta(days=days, hours=hours, minutes=mins)


# # def dirty_timestamp(dt):
# #     formats = [
# #         "%Y/%m/%d %H:%M",
# #         "%d-%m-%Y %H:%M",
# #         "%Y-%m-%d %H:%M",
# #         "%Y-%m-%dT%H:%M",
# #         "%Y-%m-%d %H:%M:%S",
# #     ]
# #     return dt.strftime(random.choice(formats))


# # def dirty_vehicle(vehicle):
# #     variants = [
# #         vehicle,
# #         vehicle.lower(),
# #         f" {vehicle} ",
# #         vehicle.replace("-", " "),
# #     ]
# #     return random.choice(variants)


# # def dirty_rate(rate):
# #     templates = [
# #         f"₹{rate}/day",
# #         f"{rate}/day",
# #         f"Rs.{rate}/day",
# #         f"{rate}",
# #     ]
# #     return random.choice(templates)


# # def dirty_fuel(value):
# #     options = [
# #         f"{int(value*100)}%",
# #         f"{value:.2f}",
# #         f"{int(value*100)} %",
# #     ]
# #     return random.choice(options)


# # def dirty_odo(v):
# #     options = [
# #         f"{v} km",
# #         f"{v:,}km",
# #         f"{v:,} km",
# #         str(v),
# #     ]
# #     return random.choice(options)


# # def random_license():
# #     if random.random() < 0.1:
# #         return ""
# #     return f"DL-{random.randint(100000,999999)}"


# # def random_promo():
# #     r = random.random()
# #     if r < 0.4:
# #         return ""
# #     if r < 0.7:
# #         return random.choice(PROMOS_VALID)
# #     return random.choice(PROMOS_INVALID)


# # def random_gps():
# #     lat = round(random.uniform(12.8, 13.2), random.choice([2,4,6]))
# #     lon = round(random.uniform(77.4, 77.7), random.choice([2,4,6]))
# #     return lat, lon


# # def random_speed():
# #     if random.random() < 0.35:
# #         return str(random.randint(120,180))
# #     return str(random.randint(40,100))


# # def random_notes():
# #     notes = [
# #         "minor scratch on bumper",
# #         "dent found on door",
# #         "Contact Rahul at 9876543210",
# #         "Email: test@gmail.com",
# #         "Normal rental",
# #         "",
# #     ]
# #     return random.choice(notes)


# # # -----------------------------
# # # MAIN GENERATOR
# # # -----------------------------

# # def generate_rows(num_records=2000, seed=42):

# #     random.seed(seed)

# #     rows = []

# #     for i in range(num_records):

# #         res_id = f"RES-{str(i+1).zfill(5)}"

# #         vehicle = dirty_vehicle(random.choice(VEHICLES))
# #         city_clean = random.choice(CITIES)

# #         pickup = random_timestamp()
# #         duration = random.randint(4,240)

# #         return_time = pickup + timedelta(hours=duration)

# #         odo_start = random.randint(5000,120000)
# #         distance = random.randint(10,2000)

# #         if random.random() < 0.05:
# #             odo_end = odo_start - random.randint(10,500)
# #         else:
# #             odo_end = odo_start + distance

# #         fuel = round(random.uniform(0.0,1.0),2)

# #         rate = random.choice(RATE_VALUES)

# #         lat, lon = random_gps()

# #         gst = round(rate * 0.05,2)
# #         total = rate + gst

# #         rows.append({

# #             "Reservation_ID":res_id,
# #             "Vehicle_ID":vehicle,
# #             "Pickup_TS":dirty_timestamp(pickup),
# #             "Return_TS":dirty_timestamp(return_time),

# #             "Odo_Start":dirty_odo(odo_start),
# #             "Odo_End":dirty_odo(odo_end),

# #             "Fuel_Level":dirty_fuel(fuel),

# #             "Rate":dirty_rate(rate),

# #             "City":random.choice(CITY_VARIANTS[city_clean]),

# #             "Payment":random.choice(["UPI","upi","Card","card","cash"]),

# #             "Driver_License":random_license(),

# #             "Promo_Code":random_promo(),

# #             "GPS_Lat":lat,
# #             "GPS_Lon":lon,

# #             "Max_Speed_kmh":random_speed(),
# #             "Harsh_Events":random.randint(0,6),

# #             "Notes":random_notes(),
# #             "Customer_Feedback":random_notes(),

# #             "Rate_Plan":random.choice(["eco","standard","prem"]),

# #             "GST_Amount":gst,
# #             "Total_Amount":total
# #         })


# #     # duplicates
# #     for _ in range(80):
# #         rows.append(random.choice(rows).copy())

# #     random.shuffle(rows)

# #     return rows


# # # -----------------------------
# # # WRITE CSV
# # # -----------------------------

# # def write_csv(rows, output_path):

# #     fieldnames = list(rows[0].keys())

# #     with open(output_path,"w",newline="",encoding="utf-8") as f:

# #         writer = csv.DictWriter(f,fieldnames=fieldnames)

# #         writer.writeheader()
# #         writer.writerows(rows)




# import csv
# import os
# import random
# import re
# from datetime import datetime, timedelta
# import pandas as pd

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# RAW_DIR = os.path.join(BASE_DIR, "../../data/raw")

# os.makedirs(RAW_DIR, exist_ok=True)

# RES_FILE = os.path.join(RAW_DIR, "reservations_raw.csv")
# TEL_FILE = os.path.join(RAW_DIR, "telematics_raw.csv")
# BILL_FILE = os.path.join(RAW_DIR, "billing_raw.csv")
# FINAL_FILE = os.path.join(RAW_DIR, "car_rental_raw.csv")

# random.seed(42)

# VEHICLES = [f"CAR-{str(i).zfill(2)}" for i in range(1,31)]

# VEHICLE_CLASSES = ["Economy", "Compact", "SUV", "Luxury"]

# CITIES = ["Bengaluru","Mumbai","Delhi","Hyderabad","Chennai","Kolkata"]

# CITY_VARIANTS = {
# "Bengaluru":["Bengaluru","blr","bangalore","BENGALURU"],
# "Mumbai":["Mumbai","mumbai"],
# "Delhi":["Delhi","delhi"],
# "Hyderabad":["Hyderabad","HYD"],
# "Chennai":["Chennai","CHENNAI"],
# "Kolkata":["Kolkata","kolkata"]
# }

# PAYMENT_VARIANTS = ["UPI","upi","Card","card","cash","wallet"]

# BASE_DATE = datetime(2026,1,1)


# def random_timestamp():

#     dt = BASE_DATE + timedelta(
#         days=random.randint(0,90),
#         hours=random.randint(0,23),
#         minutes=random.randint(0,59)
#     )

#     formats=[
#     "%Y/%m/%d %H:%M",
#     "%Y-%m-%d %H:%M",
#     "%d-%m-%Y %H:%M",
#     "%Y-%m-%d %H:%M:%S",
#     "%d/%m/%Y %H:%M"
#     ]

#     ts = dt.strftime(random.choice(formats))

#     if random.random() < 0.04:
#         ts = re.sub(r":\d\d",f":{random.randint(60,99)}",ts)

#     return dt, ts


# def dirty_vehicle(vehicle):

#     variants=[
#     vehicle,
#     vehicle.lower(),
#     f" {vehicle}",
#     f"{vehicle} ",
#     vehicle.replace("-"," ")
#     ]

#     return random.choice(variants)


# def dirty_odometer(value):

#     templates=[
#     f"{value:,} km",
#     f"{value}km",
#     f"{value}",
#     f"{value:,}km"
#     ]

#     return random.choice(templates)


# def dirty_fuel(value):

#     templates=[
#     f"{int(value*100)}%",
#     f"{value:.2f}",
#     f"{int(value*100)} %",
#     f"{value:.1f}"
#     ]

#     return random.choice(templates)


# def dirty_rate(rate):

#     templates=[
#     f"₹{rate}/day",
#     f"{rate}/day",
#     f"₹ {rate:,} /day",
#     f"{rate}"
#     ]

#     return random.choice(templates)


# # ---------------- RESERVATIONS ----------------

# def generate_reservations(n=2000):

#     rows=[]

#     for i in range(n):

#         res_id=f"RES-{str(i+1).zfill(5)}"

#         pickup_dt,pickup=random_timestamp()

#         duration=random.randint(4,200)

#         return_dt=pickup_dt+timedelta(hours=duration)

#         return_ts=return_dt.strftime("%Y-%m-%d %H:%M")

#         rows.append({

#         "Reservation_ID":res_id,
#         "Vehicle_ID":dirty_vehicle(random.choice(VEHICLES)),
#         "Pickup_TS":pickup,
#         "Return_TS":return_ts,
#         "City":random.choice(CITY_VARIANTS[random.choice(CITIES)]),
#         "Payment":random.choice(PAYMENT_VARIANTS)

#         })

#     return rows


# # ---------------- TELEMATICS ----------------

# def generate_telematics(res_ids):

#     rows=[]

#     for r in res_ids:

#         start=random.randint(5000,120000)
#         distance=random.randint(10,2000)

#         if random.random()<0.05:
#             end=start-random.randint(10,500)
#         else:
#             end=start+distance

#         fuel=round(random.uniform(0.05,1.0),2)

#         rows.append({

#         "Reservation_ID":r,
#         "Odo_Start":dirty_odometer(start),
#         "Odo_End":dirty_odometer(end),
#         "Fuel_Level":dirty_fuel(fuel),
#         "GPS_Lat":round(random.uniform(12,28),random.choice([2,4,6])),
#         "GPS_Lon":round(random.uniform(72,88),random.choice([2,4,6])),
#         "Max_Speed_kmh":random.choice([str(random.randint(40,100)),f"{random.randint(120,180)} kmh"]),
#         "Harsh_Events":random.randint(0,6)

#         })

#     return rows


# # ---------------- BILLING ----------------

# def generate_billing(res_ids):

#     rows=[]

#     for r in res_ids:

#         rate=random.choice([800,1000,1200,1500,2000,2500,3000])

#         gst=round(rate*0.05,2)

#         total=rate+gst

#         rows.append({

#         "Reservation_ID":r,
#         "Rate":dirty_rate(rate),
#         "Promo_Code":random.choice(["","SAVE10","DISC15","BOGUS99"]),
#         "GST_Amount":gst if random.random()>0.2 else "",
#         "Total_Amount":total,
#         "Rate_Plan":random.choice(["eco","standard","premium"])

#         })

#     return rows


# # ---------------- CSV WRITE ----------------

# def write_csv(path,rows):

#     with open(path,"w",newline="",encoding="utf-8") as f:

#         writer=csv.DictWriter(f,fieldnames=list(rows[0].keys()))
#         writer.writeheader()
#         writer.writerows(rows)


# # ---------------- MERGE ----------------

# def merge_datasets():

#     res=pd.read_csv(RES_FILE)
#     tel=pd.read_csv(TEL_FILE)
#     bill=pd.read_csv(BILL_FILE)

#     merged=res.merge(tel,on="Reservation_ID").merge(bill,on="Reservation_ID")

#     merged["Driver_License"]=[random.choice(["","DL12345","INVALID"]) for _ in range(len(merged))]
#     merged["Notes"]=[random.choice(["scratch on door","Contact Rahul 9876543210",""]) for _ in range(len(merged))]
#     merged["Customer_Feedback"]=[random.choice(["good service","email test@gmail.com",""]) for _ in range(len(merged))]

#     # -------- ADD DUPLICATES HERE --------
#     duplicates = merged.sample(80, replace=True)
#     merged = pd.concat([merged, duplicates], ignore_index=True)

#     merged.to_csv(FINAL_FILE,index=False)


# # ---------------- MAIN ----------------

# def generate_all():

#     reservations = generate_reservations()

#     res_ids = [r["Reservation_ID"] for r in reservations]

#     telematics = generate_telematics(res_ids)
#     billing = generate_billing(res_ids)

#     write_csv(RES_FILE, reservations)
#     write_csv(TEL_FILE, telematics)
#     write_csv(BILL_FILE, billing)

#     merge_datasets()

#     return 2000 + 80


# if __name__=="__main__":

#     count=generate_all()

#     print("Datasets generated:",count)




import csv
import os
import random
import re
from datetime import datetime, timedelta
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(BASE_DIR, "../../data/raw")

os.makedirs(RAW_DIR, exist_ok=True)

RES_FILE = os.path.join(RAW_DIR, "reservations_raw.csv")
TEL_FILE = os.path.join(RAW_DIR, "telematics_raw.csv")
BILL_FILE = os.path.join(RAW_DIR, "billing_raw.csv")
FINAL_FILE = os.path.join(RAW_DIR, "car_rental_raw.csv")

random.seed(42)

# ---------------- CONSTANTS ----------------

VEHICLES = [f"CAR-{str(i).zfill(2)}" for i in range(1,31)]

VEHICLE_CLASSES = ["Economy","Compact","SUV","Luxury"]

CITIES = ["Bengaluru","Mumbai","Delhi","Hyderabad","Chennai","Kolkata"]

CITY_VARIANTS = {
"Bengaluru":["Bengaluru","blr","bangalore","BENGALURU"],
"Mumbai":["Mumbai","mumbai"],
"Delhi":["Delhi","delhi"],
"Hyderabad":["Hyderabad","HYD"],
"Chennai":["Chennai","CHENNAI"],
"Kolkata":["Kolkata","kolkata"]
}

PAYMENT_VARIANTS = ["UPI","upi","Card","card","cash","wallet"]

BASE_DATE = datetime(2026,1,1)

# ---------------- HELPERS ----------------

def random_timestamp():

    dt = BASE_DATE + timedelta(
        days=random.randint(0,90),
        hours=random.randint(0,23),
        minutes=random.randint(0,59)
    )

    formats=[
    "%Y/%m/%d %H:%M",
    "%Y-%m-%d %H:%M",
    "%d-%m-%Y %H:%M",
    "%Y-%m-%d %H:%M:%S",
    "%d/%m/%Y %H:%M"
    ]

    ts = dt.strftime(random.choice(formats))

    if random.random() < 0.04:
        ts = re.sub(r":\d\d",f":{random.randint(60,99)}",ts)

    return dt, ts


def dirty_vehicle(vehicle):

    variants=[
    vehicle,
    vehicle.lower(),
    f" {vehicle}",
    f"{vehicle} ",
    vehicle.replace("-"," ")
    ]

    return random.choice(variants)


def dirty_odometer(value):

    templates=[
    f"{value:,} km",
    f"{value}km",
    f"{value}",
    f"{value:,}km"
    ]

    return random.choice(templates)


def dirty_fuel(value):

    templates=[
    f"{int(value*100)}%",
    f"{value:.2f}",
    f"{int(value*100)} %",
    f"{value:.1f}"
    ]

    return random.choice(templates)


def dirty_rate(rate):

    templates=[
    f"₹{rate}/day",
    f"{rate}/day",
    f"₹ {rate:,} /day",
    f"{rate}"
    ]

    return random.choice(templates)


# ---------------- RESERVATIONS ----------------

def generate_reservations(n=2000):

    rows=[]

    for i in range(n):

        res_id=f"RES-{str(i+1).zfill(5)}"

        pickup_dt,pickup=random_timestamp()

        duration=random.randint(4,200)

        return_dt=pickup_dt+timedelta(hours=duration)

        return_ts=return_dt.strftime("%Y-%m-%d %H:%M")

        booking_ts=(pickup_dt-timedelta(hours=random.randint(1,72))).strftime("%Y-%m-%d %H:%M")

        rows.append({

        "Reservation_ID":res_id,
        "Customer_ID":f"C{random.randint(1000,9999)}",
        "Vehicle_ID":dirty_vehicle(random.choice(VEHICLES)),
        "Vehicle_Class":random.choice(VEHICLE_CLASSES),

        "Booking_TS":booking_ts,

        "Pickup_TS":pickup,
        "Return_TS":return_ts,

        "City":random.choice(CITY_VARIANTS[random.choice(CITIES)]),

        "Payment":random.choice(PAYMENT_VARIANTS)

        })

    return rows


# ---------------- TELEMATICS ----------------

def generate_telematics(res_ids):

    rows=[]

    for r in res_ids:

        start=random.randint(5000,120000)
        distance=random.randint(10,2000)

        if random.random()<0.05:
            end=start-random.randint(10,500)
        else:
            end=start+distance

        fuel=round(random.uniform(0.05,1.0),2)

        rows.append({

        "Reservation_ID":r,

        "Odo_Start":dirty_odometer(start),
        "Odo_End":dirty_odometer(end),

        "Fuel_Level":dirty_fuel(fuel),

        "GPS_Lat":round(random.uniform(12,28),random.choice([2,4,6])),
        "GPS_Lon":round(random.uniform(72,88),random.choice([2,4,6])),

        "Max_Speed_kmh":random.choice([
        str(random.randint(40,100)),
        f"{random.randint(120,180)} kmh"
        ]),

        "Harsh_Events":random.randint(0,6),

        "Damage_Flag":random.choice([0,0,0,0,1])  # 20% damage

        })

    return rows


# ---------------- BILLING ----------------

def generate_billing(res_ids):

    rows=[]

    for r in res_ids:

        rate=random.choice([800,1000,1200,1500,2000,2500,3000])

        gst=round(rate*0.05,2)

        total=rate+gst

        rows.append({

        "Reservation_ID":r,

        "Rate":dirty_rate(rate),

        "Promo_Code":random.choice(["","SAVE10","DISC15","BOGUS99"]),

        "GST_Amount":gst if random.random()>0.2 else "",

        "Total_Amount":total,

        "Rate_Plan":random.choice(["eco","standard","premium"])

        })

    return rows


# ---------------- CSV WRITE ----------------

def write_csv(path,rows):

    with open(path,"w",newline="",encoding="utf-8") as f:

        writer=csv.DictWriter(f,fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


# ---------------- MERGE ----------------

def merge_datasets():

    res=pd.read_csv(RES_FILE)
    tel=pd.read_csv(TEL_FILE)
    bill=pd.read_csv(BILL_FILE)

    merged=res.merge(tel,on="Reservation_ID").merge(bill,on="Reservation_ID")

    merged["Driver_License"]=[
    random.choice(["","DL12345","INVALID"]) for _ in range(len(merged))
    ]

    merged["Notes"]=[
    random.choice(["scratch on door","Contact Rahul 9876543210",""])
    for _ in range(len(merged))
    ]

    merged["Customer_Feedback"]=[
    random.choice(["good service","email test@gmail.com",""])
    for _ in range(len(merged))
    ]

    # duplicates
    duplicates = merged.sample(80, replace=True)
    merged = pd.concat([merged, duplicates], ignore_index=True)

    merged.to_csv(FINAL_FILE,index=False)


# ---------------- MAIN ----------------

def generate_all():

    reservations = generate_reservations()

    res_ids = [r["Reservation_ID"] for r in reservations]

    telematics = generate_telematics(res_ids)
    billing = generate_billing(res_ids)

    write_csv(RES_FILE, reservations)
    write_csv(TEL_FILE, telematics)
    write_csv(BILL_FILE, billing)

    merge_datasets()

    return 2000 + 80


if __name__=="__main__":

    count=generate_all()

    print("Datasets generated:",count)