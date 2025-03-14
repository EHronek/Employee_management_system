#!/usr/bin/python3
"""Defines the Position Class"""
from models.base_model import BaseModel, Base
import models
from sqlalchemy import Column, String, Float, Text
from sqlalchemy.orm import relationship, validates


class Position(BaseModel, Base):
    """Position class"""
    if models.storage_type == "db":
        __tablename__ = 'positions'

        title = Column(String(128), unique=True, nullable=False)
        salary_range_min = Column(Float, nullable=False)
        salary_range_max = Column(Float, nullable=False)
        job_description = Column(Text, nullable=False)

        employees = relationship("Employee", back_populates="position")


    else:
        title = ""
        salary_range_min = 0.0
        salary_range_max = 0.0
        description = ""
        job_responsibilities = ""


    def __init__(self, *args, **kwargs):
        """initializes the position"""
        super().__init__(*args, **kwargs)


    @validates('salary_range_min', 'salary_range_max')
    def validate_salary_range(self, key, value):
        """Validates that salary_range_min <= salary_range_max."""
        if key == 'salary_range_min':
            try:
                # Ensure salary_range_max is not None before comparing
                if self.salary_range_max is not None and value > self.salary_range_max:
                    raise ValueError("Minimum salary must be less than or equal to maximum salary")
            except Exception as e:
                print("minimum salary")
        elif key == 'salary_range_max':

            try:
                # Ensure salary_range_min is not None before comparing
                if self.salary_range_min is not None and self.salary_range_min > value:
                    raise ValueError("Maximum salary must be greater than or equal to minimum salary")
            
            except Exception as e:
                print(f"Maximum salary: {e}")
        return value
