import asyncio
import aiohttp
from src.api import fetch_all_animals, fetch_animal_detail, post_animals
from src.transform import transform_animal


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
            batch = animal_details[i:i + batch_size]
            transformed_batch = [transform_animal(animal) for animal in batch]

            print(f"Posting batch starting at index {i}, example transformed animal:")
            print(transformed_batch[0])

            success = await post_animals(session, transformed_batch)
            if not success:
                print(f"Failed to post batch starting at index {i}")


if __name__ == "__main__":
    asyncio.run(main())
