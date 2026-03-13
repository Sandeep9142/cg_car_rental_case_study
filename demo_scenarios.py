# CLEANING FUNCTIONS
from src.cleaning.cleaner import (
    clean_vehicle_id,
    clean_timestamp,
    clean_odometer,
    clean_fuel_level,
    clean_rate,
    clean_city,
    clean_payment,
    mask_driver_license,
    smooth_gps,
    normalize_speed,
    redact_pii,
    detect_damage,
)

# VALIDATION FUNCTIONS
from src.validation.validator import (
    validate_timestamps,
    validate_odometer,
    validate_promo_code,
    validate_gst,
)

# PROCESSING FUNCTIONS
from src.processing.deduplicator import (
    remove_duplicates,
    detect_overlapping_bookings,
)

# ANALYTICS FUNCTIONS
from src.analytics.transformer import (
    detect_refueling,
    map_rate_plan,
)

print("\n==============================")
print(" CAR RENTAL PIPELINE DEMO")
print("==============================\n")

# -------------------------------------------------
# Scenario 1
# -------------------------------------------------
print("1. Vehicle_ID normalization")
print("Raw:", " car-09 ")
print("Cleaned:", clean_vehicle_id(" car-09 "))
print()


# -------------------------------------------------
# Scenario 2
# -------------------------------------------------
print("2. Timestamp normalization")
print("Raw:", "2026/03/09 10:75")
print("Cleaned:", clean_timestamp("2026/03/09 10:75"))
print()


# -------------------------------------------------
# Scenario 3
# -------------------------------------------------
print("3. Odometer cleaning")
print("Raw:", "45,000 km")
print("Cleaned:", clean_odometer("45,000 km"))
print()


# -------------------------------------------------
# Scenario 4
# -------------------------------------------------
print("4. Fuel normalization")
print("Raw:", "50%")
print("Cleaned:", clean_fuel_level("50%"))
print()


# -------------------------------------------------
# Scenario 5
# -------------------------------------------------
print("5. Rate normalization")
print("Raw:", "₹1,500/day")
print("Cleaned:", clean_rate("₹1,500/day"))
print()


# -------------------------------------------------
# Scenario 6
# -------------------------------------------------
print("6. City normalization")
print("Raw:", "blr")
print("Cleaned:", clean_city("blr"))
print()


# -------------------------------------------------
# Scenario 7
# -------------------------------------------------
print("7. Duplicate reservation detection")

records = [
    {"Reservation_ID": "RES-001"},
    {"Reservation_ID": "RES-002"},
    {"Reservation_ID": "RES-001"},
]

unique, removed = remove_duplicates(records)

print("Duplicates removed:", removed)
print()


# -------------------------------------------------
# Scenario 8
# -------------------------------------------------
print("8. Return before pickup validation")

rec = {
    "Pickup_TS": "2026-03-10 10:00",
    "Return_TS": "2026-03-09 10:00",
}

print(validate_timestamps(rec))
print()


# -------------------------------------------------
# Scenario 9
# -------------------------------------------------
print("9. Payment normalization")
print("Raw:", "upi")
print("Cleaned:", clean_payment("upi"))
print()


# -------------------------------------------------
# Scenario 10
# -------------------------------------------------
print("10. Mileage sanity check")

rec = {"Odo_Start": 50000, "Odo_End": 49000}

print(validate_odometer(rec))
print()
# --------------------------------------------------
# 11 Refueling event detection
# --------------------------------------------------
print("SCENARIO 11 — Refueling detection")

rec = {
    "Distance_km": 20,
    "Fuel_Level": 0.92
}

print(detect_refueling(rec))
print()

# --------------------------------------------------
# 12 Vehicle booking overlap detection
# --------------------------------------------------
print("SCENARIO 12 — Vehicle overlap detection")

records = [
    {
        "Reservation_ID": "RES-1",
        "Vehicle_ID": "CAR-01",
        "Pickup_TS": "2026-01-01 10:00",
        "Return_TS": "2026-01-02 10:00",
    },
    {
        "Reservation_ID": "RES-2",
        "Vehicle_ID": "CAR-01",
        "Pickup_TS": "2026-01-01 15:00",
        "Return_TS": "2026-01-02 12:00",
    },
]

print(detect_overlapping_bookings(records))
print()

# --------------------------------------------------
# 13 Damage detection
# --------------------------------------------------
print("SCENARIO 13 — Damage detection from notes")

print(detect_damage("scratch on bumper"))
print()

# --------------------------------------------------
# 14 Driver license masking
# --------------------------------------------------
print("SCENARIO 14 — Driver license masking")

print(mask_driver_license("DL12345678"))
print()

# --------------------------------------------------
# 15 Promo code validation
# --------------------------------------------------
print("SCENARIO 15 — Promo code validation")

rec = {"Promo_Code": "DISC15"}

print(validate_promo_code(rec))
print()

# --------------------------------------------------
# 16 GPS jitter smoothing
# --------------------------------------------------
print("SCENARIO 16 — GPS jitter smoothing")

print(smooth_gps("13.1234567"))
print()

# --------------------------------------------------
# 17 Speed normalization
# --------------------------------------------------
print("SCENARIO 17 — Speed normalization")

print(normalize_speed("120 kmh"))
print()

# --------------------------------------------------
# 18 PII redaction
# --------------------------------------------------
print("SCENARIO 18 — PII redaction")

print(redact_pii("Contact me at 9876543210 or email test@gmail.com"))
print()

# --------------------------------------------------
# 19 Rate plan mapping
# --------------------------------------------------
print("SCENARIO 19 — Rate plan mapping")

rec = {"Rate_Plan": "prem"}

print(map_rate_plan(rec))
print()

# --------------------------------------------------
# 20 GST validation
# --------------------------------------------------
print("SCENARIO 20 — GST validation")

rec = {
    "Rate": 2000,
    "GST_Amount": 100
}

print(validate_gst(rec))
print()

print("DEMO COMPLETE")