#!/usr/bin/python3
"""
Module for the class BaseModel
"""
import uuid
from datetime import datetime
import models
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Column, DateTime

Base = declarative_base()


class BaseModel:
    """
    Class for the BaseModel
    """
    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime(60), nullable=False)
    updated_at = Column(DateTime(60), nullable=False)
    
    def __init__(self, *args, **kwargs):
        """
        Constructor method
        """
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if kwargs.get("created_at", None) and type(self.created_at) is str:
                self.created_at = datetime.strptime(kwargs["created_at"],
                                                    "%Y-%m-%dT%H:%M:%S.%f")
            else:
                self.created_at = datetime.utcnow()
            if kwargs.get("updated_at", None) and type(self.updated_at) is str:
                self.updated_at = datetime.strptime(kwargs["updated_at"],
                                                    "%Y-%m-%dT%H:%M:%S.%f")
            else:
                self.updated_at = datetime.utcnow()
            if kwargs.get("id", None) is None:
                self.id = str(uuid.uuid4())
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            
            self.updated_at = self.created_at
    def save(self):
        """
        Method to save the object
        """
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()
        
    def to_dict(self):
        """Convert instance into dict format"""
        new_dict = self.__dict__.copy()
        if "created_at" in new_dict:
            new_dict["created_at"] = new_dict["created_at"].strftime("%Y-%m-%dT%H:%M:%S.%f")
        if "updated_at" in new_dict:
            new_dict["updated_at"] = new_dict["updated_at"].strftime("%Y-%m-%dT%H:%M:%S.%f")
        new_dict["__class__"] = self.__class__.__name__
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]
        return new_dict
            
    def __str__(self):
        """
        String representation of the object
        """
        return "[{}] ({}) {}".format(self.__class__.__name__,
                                     self.id, self.__dict__)