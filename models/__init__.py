#!/usr/bin/python3
"""
initialize package to create a 
unique FileStorage instance
"""
from os import getenv

storage_t = getenv('STORE_TYPE_STORAGE')
from models.engine.db_storage import DBStorage
if storage_t == 'db':
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
    storage.reload()