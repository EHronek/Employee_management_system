#!/usr/bin/python3
"""Defines the attendance"""
from models.base_model import BaseModel, Base
import models
from sqlalchemy import Column, String, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship


class Attendance(BaseModel, Base):
    """Representation of Attendance of each employee"""
    if models.storage_type == "db":

        __tablename__ = 'attendances'

        employee_id = Column(String(60), ForeignKey('employees.id'), nullable=False)
        date = Column(DateTime, default=datetime.utcnow, nullable=False)
        check_in_time = Column(DateTime)
        check_out_time = Column(DateTime)
        status = Column(String(30), default="pending", nullable=False)

        employee = relationship("Employee", back_populates='attendance_records')
    else:

        employee_id = ""
        date = ""
        status = ""
        check_in_time = ""
        check_out_time = ""

    def __init__(self, *args, **kwargs):
        """Intializes the attendance """
        super().__init__(*args, **kwargs)

