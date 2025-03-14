#!/usr/bin/python3
"""Defines the Overtime model"""
import models
from models.base_model import Base, BaseModel
from sqlalchemy import Column, String, Date, Float, ForeignKey
from datetime import datetime


class Overtime(BaseModel, Base):
    """Overtime"""
    if models.storage_type == 'db':
        __tablename__ = 'overtimes'
        employee_id = Column(String(60), ForeignKey('employees.id'), nullable=False)
        overtime_hours = Column(Float, nullable=False)
        overtime_date = Column(Date, default=datetime.utcnow)
        status = Column(String(20), default='pending')

    else:
        employee_id = ''
        overtime_hours = 0.0
        overtime_date = 0.0
        status = 'pending'


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


