#!/usr/bin/python3
"""Ensure your Session is thread-safe"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from os import getenv
from models.base_model import BaseModel
from models.inventory import Inventory
from models.stock_received import StockReceived
from models.stock_issued import StockIssued


Base = declarative_base()
classes = {"BaseModel": BaseModel,
           "Inventory": Inventory,
           "StockReceived": StockReceived,
           "StockIssued": StockIssued}

class DBStorage:
    """DBStorage class"""
    __engine = None
    __session = None

    def __init__(self):
        """Initializes the DBStorage class"""

        STORE_MYSQL_USER = getenv('STORE_MYSQL_USER')
        STORE_MYSQL_PWD = getenv('STORE_MYSQL_PWD')
        STORE_MYSQL_HOST = getenv('STORE_MYSQL_HOST')
        STORE_MYSQL_DB = getenv('STORE_MYSQL_DB')
        STORE_ENV = getenv('HBNB_ENV')

        if None in (STORE_MYSQL_USER, STORE_MYSQL_PWD, STORE_MYSQL_HOST, STORE_MYSQL_DB):
            raise ValueError("Database configuration environment variables are not set")

        self.__engine = create_engine(
            f"mysql+mysqlconnector://{STORE_MYSQL_USER}:{STORE_MYSQL_PWD}@{STORE_MYSQL_HOST}/{STORE_MYSQL_DB}",
            pool_pre_ping=True
        )

        if STORE_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls in {classes[clss], clss}:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = f"{obj.__class__.__name__}.{obj.id}"
                    new_dict[key] = obj
        return new_dict

    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)
            self.save()

    def reload(self):
        """Create all tables in the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session()

    def close(self):
        """Close the current database session"""
        self.__session.remove()

    def get(self, cls, id):
        """Get an object based on class name and its ID"""
        if cls not in classes:
            return None
        return self.__session.query(classes[cls]).get(id)

    def count(self, cls=None):
        """Count the number of objects in storage"""
        if cls is None:
            return sum(len(self.all(c)) for c in classes)
        if cls not in classes:
            return 0
        return len(self.all(cls))
