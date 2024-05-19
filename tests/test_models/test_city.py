#!/usr/bin/python3
"""Defines unittests for models/city.py.

Unittest classes:
    TestCityInstantiation
    TestCitySave
    TestCityToDict
"""
import os
import unittest
from datetime import datetime
from time import sleep
from models.city import City
import models


class TestCityInstantiation(unittest.TestCase):
    """Unittests for testing instantiation of the City class."""

    def test_no_args_instantiates(self):
        self.assertIsInstance(City(), City)

    def test_new_instance_stored_in_objects(self):
        city_instance = City()
        self.assertIn(city_instance, models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertIsInstance(City().id, str)

    def test_created_at_is_public_datetime(self):
        self.assertIsInstance(City().created_at, datetime)

    def test_updated_at_is_public_datetime(self):
        self.assertIsInstance(City().updated_at, datetime)

    def test_state_id_is_public_class_attribute(self):
        self.assertTrue(hasattr(City, 'state_id'))
        self.assertNotIn('state_id', City().__dict__)

    def test_name_is_public_class_attribute(self):
        self.assertTrue(hasattr(City, 'name'))
        self.assertNotIn('name', City().__dict__)

    def test_two_cities_unique_ids(self):
        city1 = City()
        city2 = City()
        self.assertNotEqual(city1.id, city2.id)

    def test_two_cities_different_created_at(self):
        city1 = City()
        sleep(0.05)
        city2 = City()
        self.assertLess(city1.created_at, city2.created_at)

    def test_two_cities_different_updated_at(self):
        city1 = City()
        sleep(0.05)
        city2 = City()
        self.assertLess(city1.updated_at, city2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        city_instance = City()
        city_instance.id = "123456"
        city_instance.created_at = city_instance.updated_at = dt
        city_str = str(city_instance)
        self.assertIn("[City] (123456)", city_str)
        self.assertIn(f"'id': '123456'", city_str)
        self.assertIn(f"'created_at': {repr(dt)}", city_str)
        self.assertIn(f"'updated_at': {repr(dt)}", city_str)

    def test_args_unused(self):
        city_instance = City(None)
        self.assertNotIn(None, city_instance.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt_iso = datetime.today().isoformat()
        city_instance = City(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(city_instance.id, "345")
        self.assertEqual(city_instance.created_at, datetime.fromisoformat(dt_iso))
        self.assertEqual(city_instance.updated_at, datetime.fromisoformat(dt_iso))

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            City(id=None, created_at=None, updated_at=None)


class TestCitySave(unittest.TestCase):
    """Unittests for testing save method of the City class."""

    @classmethod
    def setUpClass(cls):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDownClass(cls):
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass

    def test_one_save(self):
        city_instance = City()
        sleep(0.05)
        first_updated_at = city_instance.updated_at
        city_instance.save()
        self.assertLess(first_updated_at, city_instance.updated_at)

    def test_two_saves(self):
        city_instance = City()
        sleep(0.05)
        first_updated_at = city_instance.updated_at
        city_instance.save()
        second_updated_at = city_instance.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        city_instance.save()
        self.assertLess(second_updated_at, city_instance.updated_at)

    def test_save_with_arg(self):
        city_instance = City()
        with self.assertRaises(TypeError):
            city_instance.save(None)

    def test_save_updates_file(self):
        city_instance = City()
        city_instance.save()
        city_id = "City." + city_instance.id
        with open("file.json", "r") as file:
            self.assertIn(city_id, file.read())


class TestCityToDict(unittest.TestCase):
    """Unittests for testing to_dict method of the City class."""

    def test_to_dict_type(self):
        self.assertIsInstance(City().to_dict(), dict)

    def test_to_dict_contains_correct_keys(self):
        city_instance = City()
        city_dict = city_instance.to_dict()
        self.assertIn("id", city_dict)
        self.assertIn("created_at", city_dict)
        self.assertIn("updated_at", city_dict)
        self.assertIn("__class__", city_dict)

    def test_to_dict_contains_added_attributes(self):
        city_instance = City()
        city_instance.middle_name = "Holberton"
        city_instance.my_number = 98
        city_dict = city_instance.to_dict()
        self.assertEqual(city_instance.middle_name, "Holberton")
        self.assertIn("my_number", city_dict)

    def test_to_dict_datetime_attributes_are_strs(self):
        city_instance = City()
        city_dict = city_instance.to_dict()
        self.assertIsInstance(city_dict["id"], str)
        self.assertIsInstance(city_dict["created_at"], str)
        self.assertIsInstance(city_dict["updated_at"], str)

    def test_to_dict_output(self):
        dt = datetime.today()
        city_instance = City()
        city_instance.id = "123456"
        city_instance.created_at = city_instance.updated_at = dt
        expected_dict = {
            'id': '123456',
            '__class__': 'City',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(city_instance.to_dict(), expected_dict)

    def test_contrast_to_dict_dunder_dict(self):
        city_instance = City()
        self.assertNotEqual(city_instance.to_dict(), city_instance.__dict__)

    def test_to_dict_with_arg(self):
        city_instance = City()
        with self.assertRaises(TypeError):
            city_instance.to_dict(None)


if __name__ == "__main__":
    unittest.main()

