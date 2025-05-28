import asyncio
import aiohttp
from typing import List, Dict, Any, Optional

API_BASE_URL = "http://localhost:3123/animals/v1"


async def fetch_page(
    session: aiohttp.ClientSession, page: int
) -> Optional[Dict[str, Any]]:
    url = f"{API_BASE_URL}/animals?page={page}"
    try:
        async with session.get(url) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                print(f"Failed to fetch page {page}, status: {resp.status}")
                return None
    except Exception as exc:
        print(f"Exception fetching page {page}: {exc}")
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


async def fetch_animal_detail(
    session: aiohttp.ClientSession, animal_id: int
) -> Optional[Dict[str, Any]]:
    url = f"{API_BASE_URL}/animals/{animal_id}"
    retries = 3

    for attempt in range(1, retries + 1):
        try:
            async with session.get(url) as resp:
                if resp.status == 200:
                    return await resp.json()
                elif resp.status in {500, 502, 503, 504}:
                    print(
                        f"Retryable error {resp.status} fetching animal {animal_id}, attempt {attempt}"
                    )
                    await asyncio.sleep(2**attempt)
                else:
                    print(
                        f"Non-retryable error {resp.status} fetching animal {animal_id}"
                    )
                    return None
        except Exception as exc:
            print(f"Exception fetching animal {animal_id}: {exc}")
            await asyncio.sleep(2**attempt)

    return None


async def post_animals(
    session: aiohttp.ClientSession, animals_batch: List[Dict[str, Any]]
) -> bool:
    url = f"{API_BASE_URL}/home"
    retries = 3

    for attempt in range(1, retries + 1):
        try:
            async with session.post(
                url,
                json=animals_batch,
            ) as resp:
                if resp.status == 200:
                    print(f"Successfully posted batch of {len(animals_batch)} animals.")
                    return True
                elif resp.status in {500, 502, 503, 504}:
                    print(
                        f"Retryable error {resp.status} posting batch attempt {attempt}"
                    )
                    await asyncio.sleep(2**attempt)
                else:
                    print(f"Non-retryable error {resp.status} posting batch")
                    return False
        except Exception as exc:
            print(f"Exception posting batch: {exc}")
            await asyncio.sleep(2**attempt)

    return False
