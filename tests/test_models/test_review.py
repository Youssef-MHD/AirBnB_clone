#!/usr/bin/python3
"""
Defines unittests for models/review.py.

Unittest classes:
    TestReviewInstantiation
    TestReviewSave
    TestReviewToDict
"""
import os
import unittest
from datetime import datetime
from time import sleep
from models.review import Review
import models


class TestReviewInstantiation(unittest.TestCase):
    """Unittests for testing instantiation of the Review class."""

    def test_no_args_instantiates(self):
        self.assertIsInstance(Review(), Review)

    def test_new_instance_stored_in_objects(self):
        review = Review()
        self.assertIn(review, models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertIsInstance(Review().id, str)

    def test_created_at_is_public_datetime(self):
        self.assertIsInstance(Review().created_at, datetime)

    def test_updated_at_is_public_datetime(self):
        self.assertIsInstance(Review().updated_at, datetime)

    def test_place_id_is_public_class_attribute(self):
        self.assertIsInstance(Review.place_id, str)
        self.assertIn("place_id", dir(Review()))
        self.assertNotIn("place_id", Review().__dict__)

    def test_user_id_is_public_class_attribute(self):
        self.assertIsInstance(Review.user_id, str)
        self.assertIn("user_id", dir(Review()))
        self.assertNotIn("user_id", Review().__dict__)

    def test_text_is_public_class_attribute(self):
        self.assertIsInstance(Review.text, str)
        self.assertIn("text", dir(Review()))
        self.assertNotIn("text", Review().__dict__)

    def test_two_reviews_unique_ids(self):
        rv1 = Review()
        rv2 = Review()
        self.assertNotEqual(rv1.id, rv2.id)

    def test_two_reviews_different_created_at(self):
        rv1 = Review()
        sleep(0.05)
        rv2 = Review()
        self.assertLess(rv1.created_at, rv2.created_at)

    def test_two_reviews_different_updated_at(self):
        rv1 = Review()
        sleep(0.05)
        rv2 = Review()
        self.assertLess(rv1.updated_at, rv2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        rv = Review()
        rv.id = "123456"
        rv.created_at = rv.updated_at = dt
        rv_str = str(rv)
        self.assertIn("[Review] (123456)", rv_str)
        self.assertIn("'id': '123456'", rv_str)
        self.assertIn("'created_at': " + repr(dt), rv_str)
        self.assertIn("'updated_at': " + repr(dt), rv_str)

    def test_args_unused(self):
        rv = Review(None)
        self.assertNotIn(None, rv.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        rv = Review(id="345", created_at=dt.isoformat(), updated_at=dt.isoformat())
        self.assertEqual(rv.id, "345")
        self.assertEqual(rv.created_at, dt)
        self.assertEqual(rv.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Review(id=None, created_at=None, updated_at=None)


class TestReviewSave(unittest.TestCase):
    """Unittests for testing save method of the Review class."""

    @classmethod
    def setUp(cls):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDown(cls):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        rv = Review()
        sleep(0.05)
        first_updated_at = rv.updated_at
        rv.save()
        self.assertLess(first_updated_at, rv.updated_at)

    def test_two_saves(self):
        rv = Review()
        sleep(0.05)
        first_updated_at = rv.updated_at
        rv.save()
        second_updated_at = rv.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        rv.save()
        self.assertLess(second_updated_at, rv.updated_at)

    def test_save_with_arg(self):
        rv = Review()
        with self.assertRaises(TypeError):
            rv.save(None)

    def test_save_updates_file(self):
        rv = Review()
        rv.save()
        rvid = "Review." + rv.id
        with open("file.json", "r") as f:
            self.assertIn(rvid, f.read())


class TestReviewToDict(unittest.TestCase):
    """Unittests for testing to_dict method of the Review class."""

    def test_to_dict_type(self):
        self.assertIsInstance(Review().to_dict(), dict)

    def test_to_dict_contains_correct_keys(self):
        rv = Review()
        rv_dict = rv.to_dict()
        self.assertIn("id", rv_dict)
        self.assertIn("created_at", rv_dict)
        self.assertIn("updated_at", rv_dict)
        self.assertIn("__class__", rv_dict)

    def test_to_dict_contains_added_attributes(self):
        rv = Review()
        rv.middle_name = "Holberton"
        rv.my_number = 98
        rv_dict = rv.to_dict()
        self.assertIn("middle_name", rv_dict)
        self.assertIn("my_number", rv_dict)
        self.assertEqual(rv_dict["middle_name"], "Holberton")
        self.assertEqual(rv_dict["my_number"], 98)

    def test_to_dict_datetime_attributes_are_strs(self):
        rv = Review()
        rv_dict = rv.to_dict()
        self.assertIsInstance(rv_dict["id"], str)
        self.assertIsInstance(rv_dict["created_at"], str)
        self.assertIsInstance(rv_dict["updated_at"], str)

    def test_to_dict_output(self):
        dt = datetime.today()
        rv = Review()
        rv.id = "123456"
        rv.created_at = rv.updated_at = dt
        expected_dict = {
            'id': '123456',
            '__class__': 'Review',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertEqual(rv.to_dict(), expected_dict)

    def test_contrast_to_dict_dunder_dict(self):
        rv = Review()
        self.assertNotEqual(rv.to_dict(), rv.__dict__)

    def test_to_dict_with_arg(self):
        rv = Review()
        with self.assertRaises(TypeError):
            rv.to_dict(None)


if __name__ == "__main__":
    unittest.main()

