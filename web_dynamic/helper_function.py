#!/usr/bin/python3
"""Defines some Helper functions"""
from models import storage
from models.user import User
from flask import session, g
from models.employee import Employee

def get_logged_in_user():
    """Fetches the logged in user and stores in Flask's global `g`"""

    user_id = session.get("user_id")

    if not user_id:
        return None
    
    sess = storage.get_session()

    user = sess.query(User).filter_by(id=user_id).first()

    return user


# Helper functions for getting managers and user data
def get_user_data():
    current_user = get_logged_in_user()
    if current_user:
        return storage.get(Employee, current_user.employee_id)
    return None

def get_managers():
    return [manager for manager in storage.all(Employee).values()]