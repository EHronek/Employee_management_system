#!/usr/bin/python3
"""Define the user class that handles user authentication"""
from models.base_model import BaseModel, Base
import bcrypt
import models
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship



class User(BaseModel, Base):
    """Represent the User model for authentication"""
    if models.storage_type == "db":
        __tablename__ = "users"

        username = Column(String(128), unique=True, nullable=False)
        password = Column(String(256), nullable=False)
        role = Column(String(50), nullable=False)
        employee_id = Column(String(60), ForeignKey('employees.id'), nullable=False)
        status = Column(String(20), nullable=False, default='active')

        employee = relationship("Employee")

    else:
        username = ""
        password = ""
        role = ""
        status = ""
        employee_id = ""

    def __init__(self, *args, **kwargs):
        """Initializes the user"""
        super().__init__(*args, **kwargs)


    def _hash_password(self, password):
        """
        Hashes a password securely using bcrypt
        """
        password_bytes = password.encode('utf-8')

        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)

        return hashed.decode('utf-8')

