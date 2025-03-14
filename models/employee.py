#!/usr/bin/python3
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from datetime import datetime
import models
from models.leave_request import LeaveRequest


class Employee(BaseModel, Base):
    """Employee model"""
    if models.storage_type == "db":
        __tablename__ = 'employees'
        
        first_name = Column(String(128), nullable=False)
        last_name = Column(String(128), nullable=False)
        work_email = Column(String(128), unique=True, nullable=False)
        phone_number = Column(String(128), nullable=False)
        salary = Column(Float, nullable=False)
        hire_date = Column(DateTime, default=datetime.utcnow, nullable=False)
        department_id = Column(String(60), ForeignKey('departments.id'), nullable=False)
        position_id = Column(String(60), ForeignKey('positions.id'), nullable=True)
        supervisor_id = Column(String(60), ForeignKey('employees.id'), nullable=True)
        status = Column(String(50), nullable=True, default='full-time')

        department = relationship("Department", back_populates="employees", foreign_keys=[department_id])
        attendance_records = relationship("Attendance", back_populates="employee", cascade='all, delete-orphan')
        leave_requests = relationship("LeaveRequest", back_populates="employee", foreign_keys="LeaveRequest.employee_id", cascade="all, delete-orphan")
        performance_reviews = relationship("PerformanceReview", back_populates="employee", cascade="all, delete-orphan")
        payroll_records = relationship("Payroll", back_populates="employee", cascade='all, delete-orphan')
        position = relationship("Position", back_populates="employees")
        supervisor = relationship('Employee', remote_side="Employee.id", backref='subordinates', foreign_keys=[supervisor_id])


    else:
        first_name = ""
        last_name = ""
        work_email = ""
        phone_number = ""
        salary = 0.0
        hire_date = ""
        department_id = ""
        status = ""
        position_id = ""
        supervisor_id = ""

    def __init__(self, *args, **kwargs):
        """Initializes the employee"""
        super().__init__(*args, **kwargs)

