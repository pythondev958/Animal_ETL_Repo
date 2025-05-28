import datetime
from typing import Dict, Any

def transform_animal(animal: Dict[str, Any]) -> Dict[str, Any]:
    transformed = animal.copy()

    # Friends field
    friends_str = transformed.get("friends", "")
    if isinstance(friends_str, str):
        transformed["friends"] = [f.strip() for f in friends_str.split(",") if f.strip()]
    else:
        transformed["friends"] = []

    # Born_at field
    born_at_val = transformed.get("born_at")
    try:
        if born_at_val:
            ts_seconds = born_at_val / 1000
            dt = datetime.datetime.utcfromtimestamp(ts_seconds)
            transformed["born_at"] = dt.isoformat() + "Z"
        else:
            transformed["born_at"] = None
    except Exception:
        transformed["born_at"] = None

    return transformed
