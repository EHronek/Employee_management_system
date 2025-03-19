#!/usr/bin/python3
from models import storage
from api.v1.views import app_views
from flask import jsonify, request
from models.leave_request import LeaveRequest


@app_views.route("/leave_requests", methods=["GET"], strict_slashes=False)
def get_leave_requests():
    """Retrieves all the leave_requests"""
    leave_requests = storage.all(LeaveRequest).values()
    if not leave_requests:
        return jsonify({"error": "empty"}), 404
    return jsonify([leave.to_dict() for leave in leave_requests]), 200


@app_views.route("/leave_requests/<leave_id>", methods=["GET"], strict_slashes=False)
def get_leave_request(leave_id):
    """Gets a specific leave request"""
    leave = storage.get(LeaveRequest, leave_id)
    if not leave:
        return jsonify({"error": "Leave request not found"}), 404
    return jsonify(leave.to_dict()), 200


@app_views.route("/leave_requests", methods=["POST"], strict_slashes=False)
def create_leave_request():
    data = request.get_json(silent=True)
    '''if not data or "employee_id" not in data or "leave_type" not in data:
        return jsonify({"error": "Missing fields"}), 400'''
    if not data:
        return jsonify({"error": "Missing JSON request body"})
    
    required_fields = ["employee_id", "leave_type", "start_date", "end_date"]

    if not all(field in data for field in required_fields):
        return jsonify({"error", "Missing required fields"}), 400
    
    leave_request = LeaveRequest(**data)
    storage.new(leave_request)
    storage.save()
    return jsonify(leave_request.to_dict()), 201


@app_views.route("/leave_requests/<leave_id>", methods=["PUT"], strict_slashes=False)
def update_leave_request(leave_id):
    """updates a leave request record"""
    leave_request = storage.get(LeaveRequest, leave_id)
    if not leave_request:
        return jsonify({"error": "leave request not found"}), 404
    
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "invalid json"}), 400
    
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(leave_request, key, value)

    storage.save()
    return jsonify(leave_request.to_dict()), 200


@app_views.route("/leave_requests/<leave_id>", methods=["DELETE"], strict_slashes=False)
def delete_leave_request(leave_id):
    """Delete a leave request by ID"""
    leave = storage.get(LeaveRequest, leave_id)

    if not leave:
        return jsonify({"error": "Leave request not found"}), 404
    
    storage.delete(leave)
    storage.save()
    return jsonify({"message": "deleted successfully"}), 201

