#!/usr/bin/python3
"""
Defines the Inventory class
"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, DateTime, Float, Text
from datetime import datetime


class Inventory(BaseModel, Base):
    """Represents inventory of items"""
    __tablename__ = 'inventory'
    item = Column(String(60), nullable=False)
    quantity = Column(Integer(), nullable=False)
    unit_price = Column(Float, nullable=False)
    supplier = Column(String(128), nullable=True)
    date_received = Column(DateTime, default=datetime.utcnow)
    expiration_date = Column(DateTime, nullable=True)

    def __init__(self, *args, **kwargs):
        """Initializes inventory attributes"""
        self.item = kwargs.get('item', "")
        self.quantity = kwargs.get('quantity', 0)
        self.unit_price = kwargs.get('unit_price', 0.0)
        self.supplier = kwargs.get('supplier', "")
        self.date_received = kwargs.get('date_received', datetime.utcnow())
        self.expiration_date = kwargs.get('expiration_date', None)
        super().__init__(*args, **kwargs)