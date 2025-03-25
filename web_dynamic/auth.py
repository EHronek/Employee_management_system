from flask import session, redirect, url_for, jsonify, request, Blueprint, render_template, flash
from functools import wraps
from models import storage
from models.user import User
import bcrypt


def role_required(allowed_roles):
    '''Restricts access to users with specific roles'''
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if "user_id" not in session:
                return redirect(url_for("login_page"))
            
            if session.get("role") not in allowed_roles:
                return jsonify({"error": "Unauthorized"}), 403
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

