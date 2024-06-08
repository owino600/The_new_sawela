#!/usr/bin/python3
"""
Module for the class BaseModel
"""
import uuid
from datetime import datetime
import models

class BaseModel:
    """
    Class for the BaseModel
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor method
        """
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        models.storage.new(self)
        
        if kwargs:
            for key, value in kwargs.items():
                if key in ("updated_at", "created_at"):
                    self.__dict__[key] = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                elif key[0] == "id":
                    self.__dict__[key] = str(value)
                else:
                    self.__dict__[key] = value

        
    def save(self):
        """
        Method to save the object
        """
        self.updated_at = datetime.now()
        models.storage.save()
        
    def to_dict(self):
        """
        Method to convert the object to a dictionary
        """
        map_objects = {}
        for key, value in self.__dict__.items():
            if key == "created_at" or key == "updated_at":
                map_objects[key] = value.isoformat()
            else:
                map_objects[key] = value
                map_objects["__class__"] = self.__class__.__name__
                return map_objects
            
    def __str__(self):
        """
        String representation of the object
        """
        return "[{}] ({}) {}".format(self.__class__.__name__,
                                     self.id, self.__dict__)