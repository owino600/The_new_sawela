#!/usr/bin/python3
"""
Module for the class BaseModel
"""
import uuid
from datetime import datetime
import models
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, column, DateTime

Base = declarative_base()

class BaseModel:
    """
    Class for the BaseModel
    """
    id = column(String(60), nullable=False, primary_key=True)
    created_at = column(DateTime(60), nullable=False)
    updated_at = column(DateTime(60), nullable=False)
    
    def __init__(self, *args, **kwargs):
        """
        Constructor method
        """
        if not kwargs:
            from models import storage
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

        else:
            kwargs['updated_at'] = datetime.strptime(kwargs['updated_at'],
                                                     '%Y-%m-%dT%H:%M:%S.%f')
            kwargs['created_at'] = datetime.strptime(kwargs['created_at'],
                                                     '%Y-%m-%dT%H:%M:%S.%f')
            del kwargs['__class__']
            self.__dict__.update(kwargs)

        
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