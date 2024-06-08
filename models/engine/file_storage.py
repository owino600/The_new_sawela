#!/usr/bin/python3
"""
Module for serializing and deserializing data
"""
import json
import os
from models.base_model import BaseModel
from models. import
from models. import
from models. import
from models. import
from models. import
from models. import

class FileStorage:
    """
    Class for serializing and deserializing data
    """
    __file_path = "file.json"
    __objects = {}
    
    CLASSES = {
            'BaseModel': BaseModel,
            '': 
            '': 
            '': 
            '': 
            '': 
            }

    def all(self, cls=None):
        """
        Returns the dictionary __objects
        """
        if cls is not None:
            if type(cls) == str:
                cls = eval(cls)
            cls_dict = {}
            for k, v in self.__objects.items():
                if type(v) == cls:
                    cls_dict[k] = v
            return cls_dict
        return self.__objects
    def new(self, obj):
        """
        Sets in __objects the obj with key <obj class name>.id
        """
        obj_cls_name = obj.__class__.__name__

        key = "{}.{}".format(obj_cls_name, obj.id)

        self.__objects[key] = obj
        
    def save(self):
        """
        Serializes __objects to the JSON file (path: __file_path)
        """
        obj_dict = {}

        for key, obj in self.__objects.items():
            obj_dict[key] = obj.to_dict()

        with open(FileStorage.__file_path, "w") as file:
            json.dump(obj_dict, file)
            
    def reload(self):
        """
        Deserializes the JSON file to __objects (only if the JSON file (__file_path) exists ; otherwise, do nothing.
        If the file doesn’t exist, no exception should be raised)
        """
        if os.path.isfile(FileStorage.__file_path):
            with open(FileStorage.__file_path, "r") as file:
                try:
                    obj_dict = json.load(file)

                    for key, value in obj_dict.items():
                        class_name, obj_id = key.split('.')

                        cls = eval(class_name)

                        instance = cls(**value)

                        FileStorage.__objects[key] = instance
                except Exception:
                    pass
    
    def delete(self, obj=None):
        """
        Deletes obj from __objects if it’s inside
        """
        if obj is not None:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            if key in self.__objects:
                del self.__objects[key]