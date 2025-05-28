import unittest
from src.transform import transform_animal

class TestTransform(unittest.TestCase):

    def test_transform_friends(self):
        animal = {"friends": "Tom, Jerry"}
        result = transform_animal(animal)
        self.assertEqual(result["friends"], ["Tom", "Jerry"])

    def test_transform_empty_friends(self):
        animal = {"friends": ""}
        result = transform_animal(animal)
        self.assertEqual(result["friends"], [])

    def test_transform_born_at(self):
        animal = {"born_at": 1716900000000}  # Should convert to ISO 8601
        result = transform_animal(animal)
        self.assertTrue(result["born_at"].endswith("Z"))

    def test_transform_no_born_at(self):
        animal = {}
        result = transform_animal(animal)
        self.assertIsNone(result["born_at"])

if __name__ == "__main__":
    unittest.main()
