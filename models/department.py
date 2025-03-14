#!/usr/bin/python3
"""Defines the Department model"""
from models.base_model import BaseModel, Base
import models
from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from models.employee import Employee


class Department(BaseModel, Base):
    """Representation of Department"""
    if models.storage_type == "db":
        __tablename__ = 'departments'

        name = Column(String(128), nullable=False, unique=True)
        description = Column(String(256), nullable=True)
        manager_id = Column(String(60), ForeignKey('employees.id'), nullable=True)
        budget = Column(Integer, nullable=True, default=0)
        total_employees = Column(Integer, default=0, nullable=True)

        employees = relationship("Employee", back_populates="department", foreign_keys=[Employee.department_id])


    else:
        name = ""
        description = ""
        budget = 0.0
        manager_id = ""

    def __init__(self, *args, **kwargs):
        '''Initializes each department'''
        super().__init__(*args, **kwargs)

