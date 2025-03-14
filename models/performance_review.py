#!/usr/bin/python3
"""Defines the performance review model"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import String, Column, DateTime, ForeignKey, Date, Integer, Text
from sqlalchemy.orm import relationship
from datetime import datetime


class PerformanceReview(BaseModel, Base):
    """Perfomance review"""
    if models.storage_type == 'db':
        __tablename__ = "performance_reviews"

        employee_id = Column(String(60), ForeignKey('employees.id'), nullable=False)
        review_date = Column(Date, default=datetime.utcnow)
        score = Column(Integer, nullable=False)
        comments = Column(Text, nullable=True)

        employee = relationship('Employee', back_populates='performance_reviews')

    else:
        employee_id = ''
        review_date = datetime.utcnow
        score = 0
        comments = ''

    def __init__(self, *args, **kwargs):
        """Intialization of the perfomance_review"""
        super().__init__(*args, **kwargs)

