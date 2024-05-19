#!/usr/bin/python3
"""Module defining the City class, inheriting from BaseModel."""

from models.base_model import BaseModel

class City(BaseModel):
    """Represents a city, inheriting from BaseModel."""

    state_id = ""
    name = ""
