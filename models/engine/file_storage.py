#!/usr/bin/python3
"""
Module for serializing and deserializing data
"""
import json
import os
from models.base_model import BaseModel


classes = {
            'BaseModel': BaseModel, 
}
class FileStorage:
    """
    Class for serializing and deserializing data
    """
    __file_path = "file.json"
    __objects = {}
    
    
    def all(self, cls=None):
        """
        Returns the dictionary __objects
        """
        if cls is not None:
            new_dict = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    new_dict[key] = value
            return new_dict
        return self.__objects
    
    def new(self, obj):
        """
        Sets in __objects the obj with key <obj class name>.id
        """
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects[key] = obj
        
    def save(self):
        """
        Serializes __objects to the JSON file (path: __file_path)
        """
        json_dict = {}

        for key in self.__objects:
            json_dict[key] = self.__objects[key].to_dict()
        with open(self.__file_path, 'w') as f:
            json.dump(json_dict, f)
            
    def reload(self):
        """
        Deserializes the JSON file to __objects
        (only if the JSON file (__file_path) exists;
        otherwise, do nothing.
        If the file doesn’t exist, no exception should be raised)
        """
        try:
            with open(self.__file_path, 'r') as f:
                jo = json.load(f)
            for key in jo:
                self.__objects[key] = classes[jo[key]["__class__"]](**jo[key])
        except FileNotFoundError:
            pass
    
    def delete(self, obj=None):
        """
        Deletes obj from __objects if it’s inside
        """
        if obj is not None:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            if key in self.__objects:
                del self.__objects[key]
                
    def close(self):
        """call reload() method for deserializing the JSON file to objects"""
        self.reload()
        
    def get(self, cls, id):
        """Retrieve one object"""
        if cls not in classes:
            return None
        key = cls + "." + id
        return self.__objects.get(key, None)

    def count(self, cls=None):
        """Count the number of objects in storage"""
        if cls is None:
            return len(self.__objects)
        return len(self.all(cls))