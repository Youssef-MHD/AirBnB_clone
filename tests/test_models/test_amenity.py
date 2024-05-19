#!/usr/bin/python3
"""
Unittests for models/amenity.py.

Unittest classes:
    TestAmenityInstantiation
    TestAmenitySave
    TestAmenityToDict
"""
import os
import unittest
from datetime import datetime
from time import sleep
from models.amenity import Amenity
import models


class TestAmenityInstantiation(unittest.TestCase):
    """Tests instantiation of the Amenity class."""

    def test_no_args_instantiates(self):
        self.assertIsInstance(Amenity(), Amenity)

    def test_new_instance_stored_in_objects(self):
        self.assertIn(Amenity(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertIsInstance(Amenity().id, str)

    def test_created_at_is_public_datetime(self):
        self.assertIsInstance(Amenity().created_at, datetime)

    def test_updated_at_is_public_datetime(self):
        self.assertIsInstance(Amenity().updated_at, datetime)

    def test_name_is_public_class_attribute(self):
        am = Amenity()
        self.assertIsInstance(Amenity.name, str)
        self.assertTrue(hasattr(Amenity, "name"))
        self.assertFalse(hasattr(am, "name"))

    def test_two_amenities_unique_ids(self):
        am1 = Amenity()
        am2 = Amenity()
        self.assertNotEqual(am1.id, am2.id)

    def test_two_amenities_different_created_at(self):
        am1 = Amenity()
        sleep(0.05)
        am2 = Amenity()
        self.assertLess(am1.created_at, am2.created_at)

    def test_two_amenities_different_updated_at(self):
        am1 = Amenity()
        sleep(0.05)
        am2 = Amenity()
        self.assertLess(am1.updated_at, am2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        am = Amenity()
        am.id = "123456"
        am.created_at = am.updated_at = dt
        expected_str = f"[Amenity] (123456) {am.__dict__}"
        self.assertEqual(str(am), expected_str)

    def test_args_unused(self):
        am = Amenity(None)
        self.assertNotIn(None, am.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        am = Amenity(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(am.id, "345")
        self.assertEqual(am.created_at.isoformat(), dt_iso)
        self.assertEqual(am.updated_at.isoformat(), dt_iso)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Amenity(id=None, created_at=None, updated_at=None)


class TestAmenitySave(unittest.TestCase):
    """Tests the save method of the Amenity class."""

    @classmethod
    def setUpClass(cls):
        cls.tmp_file = "file.json"
        cls.backup_file = "tmp"
        if os.path.exists(cls.tmp_file):
            os.rename(cls.tmp_file, cls.backup_file)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.tmp_file):
            os.remove(cls.tmp_file)
        if os.path.exists(cls.backup_file):
            os.rename(cls.backup_file, cls.tmp_file)

    def test_one_save(self):
        am = Amenity()
        sleep(0.05)
        first_updated_at = am.updated_at
        am.save()
        self.assertLess(first_updated_at, am.updated_at)

    def test_two_saves(self):
        am = Amenity()
        sleep(0.05)
        first_updated_at = am.updated_at
        am.save()
        second_updated_at = am.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        am.save()
        self.assertLess(second_updated_at, am.updated_at)

    def test_save_with_arg(self):
        am = Amenity()
        with self.assertRaises(TypeError):
            am.save(None)

    def test_save_updates_file(self):
        am = Amenity()
        am.save()
        with open(self.tmp_file, "r") as f:
            self.assertIn(f"Amenity.{am.id}", f.read())


class TestAmenityToDict(unittest.TestCase):
    """Tests the to_dict method of the Amenity class."""

    def test_to_dict_type(self):
        self.assertIsInstance(Amenity().to_dict(), dict)

    def test_to_dict_contains_correct_keys(self):
        am = Amenity()
        am_dict = am.to_dict()
        self.assertIn("id", am_dict)
        self.assertIn("created_at", am_dict)
        self.assertIn("updated_at", am_dict)
        self.assertIn("__class__", am_dict)

    def test_to_dict_contains_added_attributes(self):
        am = Amenity()
        am.middle_name = "Holberton"
        am.my_number = 98
        self.assertEqual(am.middle_name, "Holberton")
        self.assertIn("my_number", am.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        am = Amenity()
        am_dict = am.to_dict()
        self.assertIsInstance(am_dict["id"], str)
        self.assertIsInstance(am_dict["created_at"], str)
        self.assertIsInstance(am_dict["updated_at"], str)

    def test_to_dict_output(self):
        dt = datetime.today()
        am = Amenity()
        am.id = "123456"
        am.created_at = am.updated_at = dt
        expected_dict = {
            'id': '123456',
            '__class__': 'Amenity',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(am.to_dict(), expected_dict)

    def test_contrast_to_dict_dunder_dict(self):
        am = Amenity()
        self.assertNotEqual(am.to_dict(), am.__dict__)

    def test_to_dict_with_arg(self):
        am = Amenity()
        with self.assertRaises(TypeError):
            am.to_dict(None)


if __name__ == "__main__":
    unittest.main()

