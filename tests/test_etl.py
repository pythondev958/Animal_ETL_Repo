import unittest
from src.transform import transform_animal


class TestTransformAnimal(unittest.TestCase):

    def test_transform_friends_comma_separated(self):
        animal = {"friends": "dog, cat, rabbit"}
        transformed = transform_animal(animal)
        self.assertEqual(transformed["friends"], ["dog", "cat", "rabbit"])

    def test_transform_friends_single(self):
        animal = {"friends": "dog"}
        transformed = transform_animal(animal)
        self.assertEqual(transformed["friends"], ["dog"])

    def test_transform_friends_none(self):
        animal = {}
        transformed = transform_animal(animal)
        self.assertEqual(transformed["friends"], [])

    def test_transform_born_at_valid_timestamp(self):
        # timestamp for 2020-01-01T00:00:00Z in milliseconds
        ts = 1577836800000
        animal = {"born_at": ts}
        transformed = transform_animal(animal)
        self.assertTrue(transformed["born_at"].startswith("2020-01-01T00:00:00"))

    def test_transform_born_at_none(self):
        animal = {"born_at": None}
        transformed = transform_animal(animal)
        self.assertIsNone(transformed["born_at"])

    def test_transform_born_at_invalid(self):
        animal = {"born_at": "invalid"}
        transformed = transform_animal(animal)
        self.assertIsNone(transformed["born_at"])


if __name__ == "__main__":
    unittest.main()
