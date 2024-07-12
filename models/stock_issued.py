#!/usr/bin/python3
"""
Defines the StockIssued class
"""

from models.base_model import BaseModel
from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime


class StockIssued(BaseModel):
    """Represents issued stock"""
    __tablename__ = 'stock_issued'
    item = Column(String(60), nullable=False)
    quantity = Column(Integer(), nullable=False)
    issued_date = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initializes stock issued attributes"""
        self.item = kwargs.get('item', "")
        self.quantity = kwargs.get('quantity', 0)
        self.issued_date = kwargs.get('issued_date', datetime.utcnow())
        super().__init__(*args, **kwargs)