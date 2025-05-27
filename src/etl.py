import asyncio
import requests
import aiohttp
from typing import List, Dict
from datetime import datetime

API_URL = "http://localhost:3123/animals/v1/animals"
HOME_URL = "http://localhost:3123/animals/v1/home"

def fetch_animal_list() -> List[Dict]:
    animals = []
    page = 1
    while True:
        response = requests.get(API_URL, params={"page": page})
        data = response.json()
        animals.extend(data["animals"])
        if not data["next"]:
            break
        page += 1
    return animals

def transform_animal_data(animal: Dict) -> Dict:
    return {
        "id": animal["id"],
        "name": animal["name"],
        "friends": animal["friends"].split(","),
        "born_at": datetime.fromtimestamp(animal["born_at"]).isoformat() if animal["born_at"] else None
    }

async def post_to_home(animal_batch: List[Dict], session: aiohttp.ClientSession):
    async with session.post(HOME_URL, json=animal_batch) as response:
        if response.status not in {200, 201}:
            print(f"Failed to post batch: {response.status}")
        else:
            print(f"Successfully posted batch of {len(animal_batch)} animals.")

async def load_animal_data(animals: List[Dict]):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(0, len(animals), 100):
            batch = animals[i:i+100]
            tasks.append(post_to_home(batch, session))
        await asyncio.gather(*tasks)

def run_etl():
    animals = fetch_animal_list()
    transformed = [transform_animal_data(animal) for animal in animals]
    asyncio.run(load_animal_data(transformed))



