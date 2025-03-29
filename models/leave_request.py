#!/usr/bin/python3
from models.base_model import BaseModel, Base
import models
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Integer


class LeaveRequest(BaseModel, Base):
    """Representation of a LeaveReuquest"""
    if models.storage_type == "db":
        __tablename__ = "leave_requests"

        employee_id = Column(String(60), ForeignKey('employees.id'), nullable=False)
        leave_type = Column(String(50), nullable=False)
        start_date = Column(DateTime, nullable=False)
        end_date = Column(DateTime, nullable=False)
        leave_balance = Column(Integer, nullable=False, default=30)
        status = Column(String(50), nullable=False, default='pending')
        approval_manager_id = Column(String(60), ForeignKey('employees.id'))
        reason = Column(Text, nullable=False)  # Added reason column
        document = Column(String(255), nullable=True)  # Added document column


        employee = relationship("Employee", back_populates='leave_requests', foreign_keys=[employee_id])
        approval_manager = relationship("Employee", foreign_keys=[approval_manager_id])

    else:
        start_date = ""
        end_date = ""
        leave_type = ""
        employee_id = ""
        status = ""
        approval_manager_id = ""
        reason = ""
        document = ""

    def __init__(self, *args, **kwargs):
        """Initializes the leaverequest """
        super().__init__(*args, **kwargs)

