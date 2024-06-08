#!/usr/bin/pythom3
"""New engine DBStorage: (models/engine/db_storage.py)

Private class attributes:
__engine: set to None
__session: set to None
Public instance methods:
__init__(self):
create the engine (self.__engine)
the engine must be linked to the MySQL database and user created before (hbnb_dev and hbnb_dev_db):
dialect: mysql
driver: mysqldb
all of the following values must be retrieved via environment variables:
MySQL user: HBNB_MYSQL_USER
MySQL password: HBNB_MYSQL_PWD
MySQL host: HBNB_MYSQL_HOST (here = localhost)
MySQL database: HBNB_MYSQL_DB
don’t forget the option pool_pre_ping=True when you call create_engine
drop all tables if the environment variable HBNB_ENV is equal to test
all(self, cls=None):
query on the current database session (self.__session) all objects depending of the class name (argument cls)
if cls=None, query all types of objects (User, State, City, Amenity, Place and Review)
this method must return a dictionary: (like FileStorage)
key = <class-name>.<object-id>
value = object
new(self, obj): add the object to the current database session (self.__session)
save(self): commit all changes of the current database session (self.__session)
delete(self, obj=None): delete from the current database session obj if not None
reload(self):
create all tables in the database (feature of SQLAlchemy) (WARNING: all classes who inherit from Base must be imported before calling Base.metadata.create_all(engine))
create the current database session (self.__session) from the engine (self.__engine) by using a sessionmaker - the option expire_on_commit must be set to False ; and scoped_session - to make sure your Session is thread-safe"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from os import getenv
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
Base = declarative_base()
classes = {"BaseModel": BaseModel, "User": User, "State": State,
           "City": City, "Amenity": Amenity, "Place": Place,
           "Review": Review}
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
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".format(
            getenv("STORE_MYSQL_USER"),
            getenv("STOREMYSQL_PWD"),
            getenv("STORE_MYSQL_HOST"),
            getenv("STORE_MYSQL_DB")),
                                      pool_pre_ping=True)
        if getenv("STORE_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)
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
        """Create all tables in the database (feature of SQLAlchemy) (WARNING: all classes who inherit from Base must be imported before calling Base.metadata.create_all(engine))"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session()
        return self.__session
    def close(self):
        """Close the current database session"""
        self.__session.remove()
        self.__engine.dispose()
        return self.__session
    def get(self, cls, id):
        """
        Get an object based on class name and its ID
        """
        if cls not in classes:
            return None
        return self.__session.query(classes[cls]).get(id)
    def count(self, cls=None):
        """
        Count the number of objects in storage
        """
        if cls is None:
            return sum(len(self.all(c)) for c in classes)
        if cls not in classes:
            return 0
        return len(self.all(cls))
    