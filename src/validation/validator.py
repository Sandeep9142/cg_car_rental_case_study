from datetime import datetime
import re


VALID_PAYMENTS = {"UPI", "CARD", "CASH", "WALLET"}

VALID_PROMOS = {"SAVE10", "DISC15", "FLAT100", "FIRST50", "LOYAL20"}
EXPIRED_PROMOS = {"EXPIRED20", "OFF30", "SUMMER22", "FEST21", "DIWALI22"}

TS_FORMAT = "%Y-%m-%d %H:%M"

LICENSE_PATTERN = r"^[A-Z]{2}\d{2}"

# 8.

def validate_timestamps(record):

    pickup = record.get("Pickup_TS")
    return_ts = record.get("Return_TS")

    if not pickup or not return_ts:
        return False, "Missing timestamp(s)"

    try:
        pickup_dt = datetime.strptime(str(pickup), TS_FORMAT)
        return_dt = datetime.strptime(str(return_ts), TS_FORMAT)
    except:
        return False, "Unparseable timestamp(s)"

    if return_dt <= pickup_dt:
        return False, f"Return_TS ({return_ts}) not after Pickup_TS ({pickup})"

    return True, ""

# 10.

def validate_odometer(record):

    odo_start = record.get("Odo_Start")
    odo_end = record.get("Odo_End")

    if odo_start is None or odo_end is None:
        return False, "Missing odometer value(s)"

    try:
        start = int(odo_start)
        end = int(odo_end)
    except:
        return False, "Non-numeric odometer value(s)"

    if end < start:
        return False, f"Odo_End ({end}) < Odo_Start ({start})"

    return True, ""


def validate_fuel_level(record):

    fuel = record.get("Fuel_Level")

    if fuel is None:
        return False, "Missing fuel level"

    try:
        fuel_val = float(fuel)
    except:
        return False, "Non-numeric fuel level"

    if fuel_val < 0 or fuel_val > 1:
        return False, f"Fuel_Level ({fuel_val}) out of range [0, 1]"

    return True, ""


def validate_payment(record):

    payment = record.get("Payment")

    if not payment:
        return False, "Missing payment method"

    if str(payment).strip().upper() not in VALID_PAYMENTS:
        return False, f"Invalid payment method: {payment}"

    return True, ""


def validate_required_fields(record):

    required = [
        "Reservation_ID",
        "Vehicle_ID",
        "Pickup_TS",
        "Return_TS",
        "Odo_Start",
        "Odo_End",
        "Rate",
        "City",
    ]

    for field in required:
        val = record.get(field)

        if val is None or (isinstance(val, str) and val.strip() == ""):
            return False, f"Missing required field: {field}"

    return True, ""


# 14.

def validate_driver_license(record):

    dl = record.get("Driver_License")

    if not dl:
        return True, ""   # optional field

    if not re.match(LICENSE_PATTERN, str(dl)):
        return False, f"Invalid driver license format: {dl}"

    return True, ""

# 15.

def validate_promo_code(record):

    promo = record.get("Promo_Code")

    if not promo or str(promo).strip() == "":
        return True, ""

    promo = str(promo).strip().upper()

    if promo in EXPIRED_PROMOS:
        return False, f"Expired promo code: {promo}"

    if promo not in VALID_PROMOS:
        return False, f"Invalid promo code: {promo}"

    return True, ""

# 20.

def validate_gst(record):

    gst = record.get("GST_Amount")
    rate = record.get("Rate")

    if gst in (None, "") or rate in (None, ""):
        return True, ""

    try:
        rate_val = float(rate)
        gst_val = float(gst)
    except:
        return False, "Invalid GST or Rate value"

    expected = round(rate_val * 0.05, 2)

    if abs(gst_val - expected) > 5:
        return False, f"Incorrect GST amount ({gst_val}) expected ~{expected}"

    return True, ""

def validate_record(record):

    validators = [
        validate_required_fields,
        validate_timestamps,
        validate_odometer,
        validate_fuel_level,
        validate_payment,
        validate_driver_license,
        validate_promo_code,
        validate_gst,
    ]

    reasons = []

    for validator_fn in validators:
        is_valid, reason = validator_fn(record)

        if not is_valid:
            reasons.append(reason)

    return len(reasons) == 0, reasons


def validate_all(records):

    valid = []
    rejected = []

    for record in records:

        is_valid, reasons = validate_record(record)

        if is_valid:
            valid.append(record)

        else:
            rejected_record = record.copy()
            rejected_record["Rejection_Reasons"] = "; ".join(reasons)
            rejected.append(rejected_record)

    return valid, rejected