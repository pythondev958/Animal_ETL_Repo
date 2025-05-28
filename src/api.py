import asyncio
import aiohttp
from typing import List, Dict, Any, Optional

BASE_URL = "http://localhost:3123/animals/v1"

async def fetch_page(session: aiohttp.ClientSession, page: int) -> Optional[Dict[str, Any]]:
    try:
        async with session.get(f"{BASE_URL}/animals?page={page}") as resp:
            if resp.status == 200:
                return await resp.json()
            return None
    except Exception:
        return None

async def fetch_all_animals(session: aiohttp.ClientSession) -> List[Dict[str, Any]]:
    animals, page = [], 1
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
    retries = 3
    for attempt in range(retries):
        try:
            async with session.get(f"{BASE_URL}/animals/{animal_id}") as resp:
                if resp.status == 200:
                    return await resp.json()
                if resp.status in {500, 502, 503, 504}:
                    await asyncio.sleep(2 ** attempt)
                else:
                    return None
        except:
            await asyncio.sleep(2 ** attempt)
    return None

async def post_animals(session: aiohttp.ClientSession, animals: List[Dict[str, Any]]) -> bool:
    retries = 3
    for attempt in range(retries):
        try:
            async with session.post(f"{BASE_URL}/home", json=animals) as resp:
                if resp.status == 200:
                    return True
                if resp.status in {500, 502, 503, 504}:
                    await asyncio.sleep(2 ** attempt)
                else:
                    return False
        except:
            await asyncio.sleep(2 ** attempt)
    return False
