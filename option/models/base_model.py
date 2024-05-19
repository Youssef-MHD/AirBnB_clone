#!/usr/bin/python3
"""This script defines the base model class."""

import uuid
from datetime import datetime
from models import storage


class BaseModel:
    """Base class for all other models."""

    def __init__(self, *args, **kwargs):
        """Initialize instance attributes.

        Args:
            *args (list): List of arguments.
            **kwargs (dict): Dictionary of key-value arguments.
        """
        if kwargs:
            self._initialize_from_kwargs(kwargs)
        else:
            self._initialize_new_instance()

    def _initialize_from_kwargs(self, kwargs):
        """Initialize instance from keyword arguments."""
        for key, value in kwargs.items():
            if key in ("created_at", "updated_at"):
                setattr(self, key, datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f"))
            else:
                setattr(self, key, value)

    def _initialize_new_instance(self):
        """Initialize a new instance with default values."""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        storage.new(self)

    def __str__(self):
        """Return the string representation of the instance."""
        return "[{}] ({}) {}".format(type(self).__name__, self.id, self.__dict__)

    def save(self):
        """Update `updated_at` attribute and save the instance to storage."""
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """Return a dictionary representation of the instance."""
        instance_dict = self.__dict__.copy()
        instance_dict["__class__"] = type(self).__name__
        instance_dict["created_at"] = instance_dict["created_at"].isoformat()
        instance_dict["updated_at"] = instance_dict["updated_at"].isoformat()
        return instance_dict

