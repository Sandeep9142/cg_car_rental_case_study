"""
Data Cleaning Module
Developer 2 - Responsible for cleaning and normalizing raw car rental data.
"""

import re
from datetime import datetime


# ---------------------------------------------------------
# Mappings
# ---------------------------------------------------------

CITY_MAP = {
    "blr": "Bengaluru",
    "bangalore": "Bengaluru",
    "bengaluru": "Bengaluru",
    "mumbai": "Mumbai",
    "delhi": "Delhi",
    "hyderabad": "Hyderabad",
    "hyd": "Hyderabad",
    "chennai": "Chennai",
    "kolkata": "Kolkata",
}

VALID_PAYMENTS = {"UPI", "CARD", "CASH", "WALLET"}

TIMESTAMP_PARSE_FORMATS = [
    "%Y/%m/%d %H:%M",
    "%Y-%m-%d %H:%M",
    "%d-%m-%Y %H:%M",
    "%Y-%m-%d %H:%M:%S",
    "%d/%m/%Y %H:%M",
    "%Y-%m-%dT%H:%M",
]

TARGET_TS_FORMAT = "%Y-%m-%d %H:%M"

DAMAGE_KEYWORDS = ["scratch", "dent", "damage", "crack", "accident", "broken"]


# ---------------------------------------------------------
# Vehicle ID
# ---------------------------------------------------------

# 1.

def clean_vehicle_id(value):

    if not value:
        return None

    value = value.strip().upper()

    value = value.replace(" ", "-")

    return value


# ---------------------------------------------------------
# Timestamp
# ---------------------------------------------------------

# 2.

def _fix_invalid_minutes(ts_str):

    match = re.search(r'(\d{1,2}):(\d{2})(?::(\d{2}))?', ts_str)

    if not match:
        return ts_str

    hour = int(match.group(1))
    minute = int(match.group(2))
    second = int(match.group(3)) if match.group(3) else None

    if minute >= 60:
        hour += minute // 60
        minute = minute % 60

    if second is not None:
        new_time = f"{hour:02d}:{minute:02d}:{second:02d}"
    else:
        new_time = f"{hour:02d}:{minute:02d}"

    return ts_str[:match.start()] + new_time + ts_str[match.end():]


def clean_timestamp(value):

    if not value:
        return None

    value = str(value).strip()

    value = _fix_invalid_minutes(value)

    for fmt in TIMESTAMP_PARSE_FORMATS:

        try:
            dt = datetime.strptime(value, fmt)
            return dt.strftime(TARGET_TS_FORMAT)

        except ValueError:
            continue

    return None


# ---------------------------------------------------------
# Odometer
# ---------------------------------------------------------


# 3. 

def clean_odometer(value):

    if not value:
        return None

    value = str(value)

    # remove km, commas etc
    value = re.sub(r"[^\d\-\.]", "", value)

    try:
        return int(float(value))
    except:
        return None


# ---------------------------------------------------------
# Fuel
# ---------------------------------------------------------

# 4.

def clean_fuel_level(value):

    if not value:
        return None

    value = str(value).lower().strip()

    value = value.replace("percent", "").replace("%", "")

    try:

        fuel = float(value)

        if fuel > 1:
            fuel = fuel / 100

        return round(fuel, 2)

    except:
        return None


# ---------------------------------------------------------
# Rate
# ---------------------------------------------------------

# 5. 

def clean_rate(value):

    if not value:
        return None

    value = str(value).lower()

    value = value.replace("₹", "")
    value = value.replace("rs.", "")
    value = value.replace("rs", "")
    value = value.replace("/day", "")
    value = value.replace("per day", "")
    value = value.replace(",", "")

    value = re.sub(r"[^\d\.]", "", value)

    try:
        return int(float(value))
    except:
        return None


# ---------------------------------------------------------
# City
# ---------------------------------------------------------

# 6.

def clean_city(value):

    if not value:
        return None

    key = value.strip().lower()

    return CITY_MAP.get(key, key.title())


# ---------------------------------------------------------
# Payment
# ---------------------------------------------------------

# 9.

def clean_payment(value):

    if not value:
        return None

    value = str(value).strip().upper()

    if value in VALID_PAYMENTS:
        return value

    if value in ["CREDIT CARD", "DEBIT CARD"]:
        return "CARD"

    return value


# ---------------------------------------------------------
# Driver License Masking
# ---------------------------------------------------------

# 14.

def mask_driver_license(dl):

    if not dl:
        return ""

    dl = str(dl).strip()

    if len(dl) < 6:
        return dl

    return dl[:4] + "XXXXXXX"


# ---------------------------------------------------------
# GPS smoothing
# ---------------------------------------------------------

# 16.

def smooth_gps(value):

    try:
        return round(float(value), 4)
    except:
        return None


# ---------------------------------------------------------
# Speed normalization
# ---------------------------------------------------------

# 17.

def normalize_speed(value):

    if not value:
        return None

    value = str(value).lower()

    value = value.replace("kmh", "").replace("km/h", "").strip()

    try:
        return int(value)
    except:
        return None


# ---------------------------------------------------------
# PII Redaction
# ---------------------------------------------------------

# 18.

def redact_pii(text):

    if not text:
        return text

    text = re.sub(r'\b\d{10}\b', '[PHONE]', text)
    text = re.sub(r'\S+@\S+', '[EMAIL]', text)

    return text


# ---------------------------------------------------------
# Damage detection
# ---------------------------------------------------------

#13. 

def detect_damage(notes):

    if not notes:
        return False

    notes = notes.lower()

    for word in DAMAGE_KEYWORDS:
        if word in notes:
            return True

    return False


# ---------------------------------------------------------
# Record Cleaning
# ---------------------------------------------------------

def clean_record(record):

    cleaned = record.copy()

    cleaned["Vehicle_ID"] = clean_vehicle_id(record.get("Vehicle_ID"))
    cleaned["Pickup_TS"] = clean_timestamp(record.get("Pickup_TS"))
    cleaned["Return_TS"] = clean_timestamp(record.get("Return_TS"))

    cleaned["Odo_Start"] = clean_odometer(record.get("Odo_Start"))
    cleaned["Odo_End"] = clean_odometer(record.get("Odo_End"))

    cleaned["Fuel_Level"] = clean_fuel_level(record.get("Fuel_Level"))

    cleaned["Rate"] = clean_rate(record.get("Rate"))

    cleaned["City"] = clean_city(record.get("City"))

    cleaned["Payment"] = clean_payment(record.get("Payment"))

    cleaned["Driver_License"] = mask_driver_license(
        record.get("Driver_License")
    )

    cleaned["GPS_Lat"] = smooth_gps(record.get("GPS_Lat"))
    cleaned["GPS_Lon"] = smooth_gps(record.get("GPS_Lon"))

    cleaned["Max_Speed_kmh"] = normalize_speed(record.get("Max_Speed_kmh"))

    cleaned["Notes"] = redact_pii(record.get("Notes"))
    cleaned["Customer_Feedback"] = redact_pii(
        record.get("Customer_Feedback")
    )

    cleaned["Damage_Reported"] = detect_damage(record.get("Notes"))

    return cleaned


# ---------------------------------------------------------
# Clean All
# ---------------------------------------------------------

def clean_all(records):

    return [clean_record(r) for r in records]