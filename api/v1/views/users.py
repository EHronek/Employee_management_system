#!/usr/bin/python3
"""User API endpoint"""
from flask import jsonify, request
from models.user import User
from api.v1.views import app_views
from models import storage

@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users]), 200


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    user = storage.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict()), 200


@app_views.route('/users/', methods=["POST"], strict_slashes=False)
def create_user():
    """creates a new user """
    data = request.get_json()
    if not data or not all(key in data for key in ['username', 'password', 'role', 'employee_id']):
        return jsonify({"error": "missing required fields"}), 400
    
    if storage.find(User, username=data['username']):
        return jsonify({"error": "username already exists"}), 400
    
    new_user = User(
        username=data['username'],
        password=User()._hash_password(data['password']),
        role=data['role'],
        employee_id = data['employee_id']
    )
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=True)
def update_user(user_id):
    """Updates an existing user"""
    user = storage.get(User, user_id)

    if not user:
        return jsonify({"error": "user not found"}), 404
    
    data = request.get_json(silent=True)
    if not data:
        jsonify({"error": "not a valid json"}), 400

    for key, value in data.items():
        if key == 'password':
            value = user._hash_password(value)
        if key in ['username', 'role', 'status', 'password']:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
    

@app_views.route("/users/<user_id>", methods=['DELETE'], strict_slashes=True)
def delete_user(user_id):
    """Deletes a User from db"""
    user = storage.get(User, user_id)

    if not user:
        return jsonify({"error": "user not found"}), 404
    
    storage.delete(user)
    storage.save()
    return jsonify({"message": "User deleted"}), 200

