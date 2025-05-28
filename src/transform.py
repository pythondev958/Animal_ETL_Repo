import datetime
from typing import Dict, Any


def transform_animal(animal: Dict[str, Any]) -> Dict[str, Any]:
    transformed = animal.copy()

    # Transform friends field: comma-separated string to list
    friends_str = transformed.get("friends")
    if friends_str and isinstance(friends_str, str):
        if "," in friends_str:
            friends_list = [f.strip() for f in friends_str.split(",")]
        else:
            friends_list = [friends_str.strip()]
        transformed["friends"] = friends_list
    else:
        transformed["friends"] = []

    # Transform born_at field from milliseconds timestamp to ISO8601 UTC string
    born_at_val = transformed.get("born_at")
    if born_at_val is not None:
        try:
            ts_seconds = born_at_val / 1000
            dt = datetime.datetime.fromtimestamp(ts_seconds, datetime.timezone.utc)
            transformed["born_at"] = dt.isoformat()
        except Exception:
            transformed["born_at"] = None
    else:
        transformed["born_at"] = None

    return transformed
