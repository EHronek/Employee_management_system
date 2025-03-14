#!/usr/bin/python3
"""Defines the training class"""
import models
from sqlalchemy import Column, String, ForeignKey, Float, Date
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from datetime import datetime

class Training(BaseModel, Base):
    """Training model"""
    if models.storage_type == 'db':
        __tablename__ = 'trainings'

        employee_id = Column(String(60), ForeignKey('employees.id'), nullable=False)
        training_name = Column(String(128), nullable=False)
        trainer_name = Column(String(128), nullable=False)
        training_cost = Column(Float, nullable=True)
        training_date = Column(Date, nullable=False, default=datetime.utcnow)

    else:
        employee_id = ''
        training_name = ''
        trainer_name = ''
        training_cost = 0.0
        training_date = 0.0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

