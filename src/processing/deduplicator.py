from datetime import datetime
from collections import defaultdict


TS_FORMAT = "%Y-%m-%d %H:%M"

# 7.

def remove_duplicates(records):

    seen = set()
    unique = []
    duplicates_count = 0

    for record in records:

        res_id = record.get("Reservation_ID", "")

        if res_id in seen:
            duplicates_count += 1
        else:
            seen.add(res_id)
            unique.append(record)

    return unique, duplicates_count

# 12. 

def detect_overlapping_bookings(records):

    vehicle_bookings = defaultdict(list)

    for record in records:

        vid = record.get("Vehicle_ID", "")
        pickup = record.get("Pickup_TS", "")
        return_ts = record.get("Return_TS", "")
        res_id = record.get("Reservation_ID", "")

        try:

            pickup_dt = datetime.strptime(str(pickup), TS_FORMAT)
            return_dt = datetime.strptime(str(return_ts), TS_FORMAT)

            vehicle_bookings[vid].append((pickup_dt, return_dt, res_id))

        except:
            continue

    flagged = set()

    for vid, bookings in vehicle_bookings.items():

        bookings.sort(key=lambda x: x[0])

        for i in range(len(bookings)):
            for j in range(i + 1, len(bookings)):

                a_start, a_end, a_id = bookings[i]
                b_start, b_end, b_id = bookings[j]

                if a_start < b_end and b_start < a_end:

                    flagged.add(a_id)
                    flagged.add(b_id)

                else:
                    break

    return flagged

# 10.

def detect_odometer_rollback(records):

    vehicle_readings = defaultdict(list)

    for record in records:

        vid = record.get("Vehicle_ID", "")
        pickup = record.get("Pickup_TS", "")
        res_id = record.get("Reservation_ID", "")

        try:

            pickup_dt = datetime.strptime(str(pickup), TS_FORMAT)

            odo_start = int(record.get("Odo_Start", 0))
            odo_end = int(record.get("Odo_End", 0))

            vehicle_readings[vid].append((pickup_dt, odo_start, odo_end, res_id))

        except:
            continue

    flagged = set()

    for vid, readings in vehicle_readings.items():

        readings.sort(key=lambda x: x[0])

        for i in range(1, len(readings)):

            prev_end = readings[i - 1][2]
            curr_start = readings[i][1]

            if curr_start < prev_end:

                flagged.add(readings[i - 1][3])
                flagged.add(readings[i][3])

    return flagged

# 9
def compute_fraud_risk(records):

    overlap_flagged = detect_overlapping_bookings(records)
    rollback_flagged = detect_odometer_rollback(records)

    enriched = []

    for record in records:

        rec = record.copy()
        score = 0

        res_id = rec.get("Reservation_ID", "")

        try:

            pickup_dt = datetime.strptime(str(rec.get("Pickup_TS", "")), TS_FORMAT)
            return_dt = datetime.strptime(str(rec.get("Return_TS", "")), TS_FORMAT)

            hours = (return_dt - pickup_dt).total_seconds() / 3600

            distance = int(rec.get("Odo_End", 0)) - int(rec.get("Odo_Start", 0))

            if hours < 4 and distance > 500:
                score += 3

        except:
            pass

        if res_id in overlap_flagged:

            rec["Vehicle_Overlap_Flag"] = True
            score += 2

        else:
            rec["Vehicle_Overlap_Flag"] = False

        if res_id in rollback_flagged:

            rec["Odometer_Rollback_Flag"] = True
            score += 3

        else:
            rec["Odometer_Rollback_Flag"] = False

        rec["Fraud_Risk_Score"] = score

        if score == 0:
            rec["Fraud_Risk_Level"] = "None"
        elif score <= 2:
            rec["Fraud_Risk_Level"] = "Low"
        elif score <= 4:
            rec["Fraud_Risk_Level"] = "Medium"
        else:
            rec["Fraud_Risk_Level"] = "High"

        enriched.append(rec)

    return enriched


def deduplicate_and_flag(records):

    unique_records, num_duplicates = remove_duplicates(records)

    enriched_records = compute_fraud_risk(unique_records)

    return enriched_records, num_duplicates