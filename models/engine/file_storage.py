#!/usr/bin/python3
"""Module for FileStorage class."""
import datetime
import json
import os

class FileStorage:
    """Class for storing and retrieving data"""
    
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary __objects"""
        return self.__class__.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id"""
        key = "{}.{}".format(type(obj).__name__, obj.id)
        self.__class__.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file (path: __file_path)"""
        with open(self.__class__.__file_path, "w", encoding="utf-8") as f:
            obj_dict = {key: obj.to_dict() for key, obj in self.__class__.__objects.items()}
            json.dump(obj_dict, f)

    def reload(self):
        """Reloads the stored objects from the JSON file"""
        if not os.path.isfile(self.__class__.__file_path):
            return
        with open(self.__class__.__file_path, "r", encoding="utf-8") as f:
            obj_dict = json.load(f)
            for key, value in obj_dict.items():
                class_name = value["__class__"]
                cls = self.classes().get(class_name)
                if cls:
                    self.__class__.__objects[key] = cls(**value)

    def classes(self):
        """Returns a dictionary of valid classes and their references"""
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        return {
            "BaseModel": BaseModel,
            "User": User,
            "State": State,
            "City": City,
            "Amenity": Amenity,
            "Place": Place,
            "Review": Review
        }

    def attributes(self):
        """Returns the valid attributes and their types for classname"""
        return {
            "BaseModel": {
                "id": str,
                "created_at": datetime.datetime,
                "updated_at": datetime.datetime
            },
            "User": {
                "email": str,
                "password": str,
                "first_name": str,
                "last_name": str
            },
            "State": {"name": str},
            "City": {
                "state_id": str,
                "name": str
            },
            "Amenity": {"name": str},
            "Place": {
                "city_id": str,
                "user_id": str,
                "name": str,
                "description": str,
                "number_rooms": int,
                "number_bathrooms": int,
                "max_guest": int,
                "price_by_night": int,
                "latitude": float,
                "longitude": float,
                "amenity_ids": list
            },
            "Review": {
                "place_id": str,
                "user_id": str,
                "text": str
            }
        }

