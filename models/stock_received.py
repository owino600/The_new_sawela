#!/usr/bin/python3
"""
Defines the StockReceived class
"""

from models.base_model import BaseModel
from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime


class StockReceived(BaseModel):
    """Represents received stock"""
    __tablename__ = 'stock_received'
    item = Column(String(60), nullable=False)
    quantity = Column(Integer(), nullable=False)
    received_date = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initializes stock received attributes"""
        self.item = kwargs.get('item', "")
        self.quantity = kwargs.get('quantity', 0)
        self.received_date = kwargs.get('received_date', datetime.utcnow())
        super().__init__(*args, **kwargs)