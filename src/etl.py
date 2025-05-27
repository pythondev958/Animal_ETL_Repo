import asyncio
import aiohttp
import datetime
from typing import List, Dict, Any, Optional

API_BASE_URL = "http://localhost:3123/animals/v1"

def transform_animal(animal: Dict[str, Any]) -> Dict[str, Any]:
    transformed = animal.copy()

    # Transform friends field: comma-separated string to list
    friends_str = transformed.get("friends")
    if friends_str and isinstance(friends_str, str):
        # Split by comma or single friend string to list
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
            dt = datetime.datetime.utcfromtimestamp(ts_seconds)
            transformed["born_at"] = dt.isoformat() + "Z"
        except Exception:
            transformed["born_at"] = None
    else:
        transformed["born_at"] = None

    return transformed


async def fetch_page(session: aiohttp.ClientSession, page: int) -> Optional[Dict[str, Any]]:
    url = f"{API_BASE_URL}/animals?page={page}"
    try:
        async with session.get(url) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                print(f"Failed to fetch page {page}, status: {resp.status}")
                return None
    except Exception as e:
        print(f"Exception fetching page {page}: {e}")
        return None


async def fetch_all_animals(session: aiohttp.ClientSession) -> List[Dict[str, Any]]:
    animals = []
    page = 1
    while True:
        data = await fetch_page(session, page)
        if not data or "items" not in data:
            break

        animals.extend(data["items"])

        if page >= data.get("total_pages", 0):
            break
        page += 1
    return animals


async def fetch_animal_detail(session: aiohttp.ClientSession, animal_id: int) -> Optional[Dict[str, Any]]:
    url = f"{API_BASE_URL}/animals/{animal_id}"
    retries = 3
    for attempt in range(1, retries + 1):
        try:
            async with session.get(url) as resp:
                if resp.status == 200:
                    return await resp.json()
                elif resp.status in {500, 502, 503, 504}:
                    print(f"Retryable error {resp.status} fetching animal {animal_id}, attempt {attempt}")
                    await asyncio.sleep(2 ** attempt)
                else:
                    print(f"Non-retryable error {resp.status} fetching animal {animal_id}")
                    return None
        except Exception as e:
            print(f"Exception fetching animal {animal_id}: {e}")
            await asyncio.sleep(2 ** attempt)
    return None


async def post_animals(session: aiohttp.ClientSession, animals_batch: List[Dict[str, Any]]) -> bool:
    url = f"{API_BASE_URL}/home"
    retries = 3
    for attempt in range(1, retries + 1):
        try:
            async with session.post(url, json=animals_batch) as resp:
                if resp.status == 200:
                    print(f"Successfully posted batch of {len(animals_batch)} animals.")
                    return True
                elif resp.status in {500, 502, 503, 504}:
                    print(f"Retryable error {resp.status} posting batch attempt {attempt}")
                    await asyncio.sleep(2 ** attempt)
                else:
                    print(f"Non-retryable error {resp.status} posting batch")
                    return False
        except Exception as e:
            print(f"Exception posting batch: {e}")
            await asyncio.sleep(2 ** attempt)
    return False


async def main():
    async with aiohttp.ClientSession() as session:
        print("Fetching all animals summary...")
        animal_summaries = await fetch_all_animals(session)

        print(f"Total animals fetched: {len(animal_summaries)}")

        print("Fetching animal details...")
        detail_tasks = [fetch_animal_detail(session, animal["id"]) for animal in animal_summaries]
        animal_details = await asyncio.gather(*detail_tasks)

        # Filter out None results (failed fetches)
        animal_details = [a for a in animal_details if a]

        print(f"Fetched details for {len(animal_details)} animals.")

        batch_size = 100
        for i in range(0, len(animal_details), batch_size):
            batch = animal_details[i : i + batch_size]
            transformed_batch = [transform_animal(animal) for animal in batch]

            # Debug print first transformed animal in batch
            print(f"Posting batch starting at index {i}, example transformed animal:")
            print(transformed_batch[0])

            success = await post_animals(session, transformed_batch)
            if not success:
                print(f"Failed to post batch starting at index {i}")

if __name__ == "__main__":
    asyncio.run(main())
