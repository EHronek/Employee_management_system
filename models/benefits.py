#!/usr/bin/python3
"""Defines the Benefits model"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Text, ForeignKey
import models


class Benefits(BaseModel, Base):
    """Benefits model"""
    if models.storage_type == 'db':
        __tablename__ = 'benefits'

        employee_id = Column(String(60), ForeignKey('employees.id'), nullable=False)
        benefit_type = Column(String(128), nullable=False)
        details = Column(Text, nullable=True)

    else:
        employee_id = ''
        benefit_type = ''
        details =  ''

    def __init__(self, *args, **kwargs):
        """Initialization of Benefits"""
        super().__init__(*args, **kwargs)

