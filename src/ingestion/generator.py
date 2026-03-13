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

CITY_COORDS = {
    "Bengaluru": (12.9716, 77.5946),
    "Mumbai": (19.0760, 72.8777),
    "Delhi": (28.7041, 77.1025),
    "Hyderabad": (17.3850, 78.4867),
    "Chennai": (13.0827, 80.2707),
    "Kolkata": (22.5726, 88.3639)
}

PAYMENT_VARIANTS = ["UPI","upi","Card","card","cash","wallet"]

BASE_DATE = datetime(2026,1,1)

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


def generate_reservations(n=2000):

    rows=[]

    for i in range(n):

        res_id=f"RES-{str(i+1).zfill(5)}"

        pickup_dt,pickup=random_timestamp()

        duration=random.randint(4,200)

        return_dt=pickup_dt+timedelta(hours=duration)

        return_ts=return_dt.strftime("%Y-%m-%d %H:%M")

        booking_ts=(pickup_dt-timedelta(hours=random.randint(1,72))).strftime("%Y-%m-%d %H:%M")

        city_key = random.choice(CITIES)
        city_name = random.choice(CITY_VARIANTS[city_key])

        lat, lon = CITY_COORDS[city_key]

        pickup_lat = lat + random.uniform(-0.02, 0.02)
        pickup_lon = lon + random.uniform(-0.02, 0.02)

        drop_lat = lat + random.uniform(-0.02, 0.02)
        drop_lon = lon + random.uniform(-0.02, 0.02)

        rows.append({

        "Reservation_ID":res_id,
        "Customer_ID":f"C{random.randint(1000,9999)}",
        "Vehicle_ID":dirty_vehicle(random.choice(VEHICLES)),
        "Vehicle_Class":random.choice(VEHICLE_CLASSES),

        "Booking_TS":booking_ts,

        "Pickup_TS":pickup,
        "Return_TS":return_ts,

        "City":city_name,

        "Pickup_Lat":round(pickup_lat,6),
        "Pickup_Lon":round(pickup_lon,6),
        "Drop_Lat":round(drop_lat,6),
        "Drop_Lon":round(drop_lon,6),


        "Payment":random.choice(PAYMENT_VARIANTS)

        })

    return rows


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


def write_csv(path,rows):

    with open(path,"w",newline="",encoding="utf-8") as f:

        writer=csv.DictWriter(f,fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


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

    duplicates = merged.sample(80, replace=True)
    merged = pd.concat([merged, duplicates], ignore_index=True)

    merged.to_csv(FINAL_FILE,index=False)



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