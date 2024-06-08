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
        models.storage.new(self)
        models.storage.save()
        
    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        return dictionary
            
    def __str__(self):
        """
        String representation of the object
        """
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return "[{}] ({}) {}".format(self.__class__.__name__,
                                     self.id, self.__dict__)