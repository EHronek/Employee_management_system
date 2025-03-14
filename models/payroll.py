#!/usr/bin/python3
"""Defines the Payroll"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import models
from datetime import datetime


class Payroll(BaseModel, Base):
    """Represent the Payroll for each employeee"""
    if models.storage_type == "db":
        __tablename__ = 'payrolls'

        employee_id = Column(String(60), ForeignKey('employees.id'), nullable=False)
        basic_salary = Column(Float, nullable=False)
        deductions = Column(Float, nullable=False)
        net_pay = Column(Float, nullable=False)
        payment_date = Column(DateTime, default=datetime.utcnow, nullable=False)
        overtime_pay = Column(Float, default=0.0)
        bonuses = Column(Float, default=0.0)
        payment_status = Column(String(20), nullable=False, default='pending')

        employee = relationship("Employee", back_populates='payroll_records')

    else:
        employee_id = ""
        basic_salary = 0.0
        deductions = 0.0
        net_pay = 0.0
        payment_date = ""
        overtime_pay = 0.0
        bonuses = 0.0
        payment_status = "pending"

    def __init__(self, *args, **kwargs):
        """intializes the Payroll"""
        super().__init__(*args, **kwargs)

