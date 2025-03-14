#!/usr/bin/python3
"""Defines the CompanyAssets"""
import models
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Date, ForeignKey, Date
from models.base_model import Base, BaseModel
from datetime import datetime


class CompanyAssets(BaseModel, Base):
    if models.storage_type == 'db':
    
        __tablename__ = 'company_assets'

        employee_id = Column(String(60), ForeignKey("employees.id"), nullable=False)
        asset_name = Column(String(128), nullable=False)
        asset_serial = Column(String(128), nullable=False, unique=True)
        issued_date = Column(Date, default=datetime.utcnow)
        return_date = Column(Date, nullable=True)

    else:
        employee_id = ''
        asset_name = ''
        asset_serial = ''
        issued_date = ''
        return_date = ''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


