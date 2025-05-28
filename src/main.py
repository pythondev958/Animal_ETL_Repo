import asyncio
import aiohttp
import logging
from src.api import fetch_all_animals, fetch_animal_detail, post_animals
from src.transform import transform_animal

# Setup basic logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

async def run_etl():
    async with aiohttp.ClientSession() as session:
        logging.info("Fetching all animal summaries...")
        summaries = await fetch_all_animals(session)
        logging.info(f"Fetched {len(summaries)} animal summaries.")

        logging.info("Fetching animal details...")
        detail_tasks = [fetch_animal_detail(session, animal['id']) for animal in summaries]
        details = await asyncio.gather(*detail_tasks)

        details = [d for d in details if d]
        logging.info(f"Fetched full details for {len(details)} animals.")

        for i in range(0, len(details), 100):
            batch = details[i:i+100]
            transformed = [transform_animal(animal) for animal in batch]
            logging.info(f"Posting batch from index {i} (size {len(transformed)}), sample animal:")
            logging.info(transformed[0])

            success = await post_animals(session, transformed)
            if success:
                logging.info(f"Batch {i}-{i+len(transformed)} posted successfully.")
            else:
                logging.error(f"Failed to post batch {i}-{i+len(transformed)}.")

if __name__ == "__main__":
    asyncio.run(run_etl())
