# import pprint
import json

def failed_login_summary(events, threshold=2):
    result = {
        "failed_counts": 0,
        "failed_users": [],
        "failures_by_user": {},
        "flagged_user": [],
        "skipped_events": 0
    }

    for event in events:
        if "user" not in event or "status" not in event:
            result["skipped_events"] += 1
            continue

        user = event["user"]
        status = event["status"]

        if not isinstance(user, str) or not user.strip():
            result["skipped_events"] += 1
            continue

        if status not in ["failed", "success"]:
            result["skipped_events"] += 1
            continue

        if status == "failed":
            result["failed_counts"] += 1
            result["failed_users"].append(user)

            if user not in result["failures_by_user"]:
                result["failures_by_user"][user] = 1
            else:
                result["failures_by_user"][user] += 1

    
    for user, count in result["failures_by_user"].items():
        if count >= threshold:
            result["flagged_user"].append(user)

    return result


def successful_login_summary(events):
    result = {
        "successful_count": 0,
        "successful_by_user": {},
        "skipped_event": 0
    }

    for event in events:

        if "user" not in event or "status" not in event:
            result["skipped_event"] += 1
            continue
        
        user = event["user"]
        status = event["status"]

        if not isinstance(user, str) or not user.strip() or status not in ["failed", "success"]:
            result["skipped_event"] += 1
            continue

        if status == "success":
            result["successful_count"] += 1

            if user not in result["successful_by_user"]:
                result["successful_by_user"][user] = 0

            result["successful_by_user"][user] += 1

    return result
    


# pprint.pprint(failed_login_summary(events, threshold=3))
# pprint.pprint(successful_login_summary(events))

# with open("event.json", "r", encoding="utf-8") as file:
#     events = json.load(file)


# summary = successful_login_summary(events)


# with open("summary.json", "w", encoding="utf-8") as file:
#     json.dump(summary, file, indent=4)



try:
    with open("something.json", "r", encoding="utf-8") as file:
        events = json.load(file)

except FileNotFoundError:
    print("file not found")

else:

    summary = successful_login_summary(events)

    with open("summary.json", "w", encoding="utf-8") as file:
        json.dump(summary, file, indent=4)