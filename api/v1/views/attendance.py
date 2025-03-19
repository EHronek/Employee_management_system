#!/usr/bin/python3
"""Defines the Attendance API endpoint"""
from flask import jsonify, request, abort
from models.attendance import Attendance
from models.employee import Employee
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route("/attendances", methods=["GET"], strict_slashes=False)
def get_attendances():
    attendances = storage.all(Attendance).values()
    if not attendances:
        return jsonify({"error": "not found"}), 404

    return jsonify([att.to_dict() for att in attendances])


@app_views.route("/attendances/<attendance_id>", methods=["GET"], strict_slashes=False)
def get_attendance(attendance_id):
    """Get the specific attendance id"""
    attendance = storage.get(Attendance, attendance_id)
    if not attendance:
        return jsonify({"error": "attendance not found"}), 404
    return jsonify(attendance.to_dict()), 200


@app_views.route("/attendances", methods=["POST"], strict_slashes=False)
def create_attendance():
    """creates an attendance record"""
    data = request.get_json()
    if not data or 'employee_id' not in data:
        return jsonify({"error": "missing employee_id"}), 400
    
    employee = storage.get(Employee, data['employee_id'])
    if not employee:
        return jsonify({"error": "invalid employee_id"})
    
    new_attendance = Attendance(**data)
    storage.new(new_attendance)
    storage.save()
    return jsonify(new_attendance.to_dict()), 201


@app_views.route("/attendances/<attendance_id>", methods=['PUT'])
def update_attendance(attendance_id):
    attendance = storage.get(Attendance, attendance_id)

    if not attendance:
        return jsonify({"error": "not found"}), 404
    
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(attendance, key, value)
    storage.save()
    return jsonify(attendance.to_dict()), 200


@app_views.route("/attendances/<attendance_id>", methods=["DELETE"], strict_slashes=False)
def delete_attendance(attendance_id):
    """deletes an attendance record in storage"""
    attendance = storage.get(Attendance, attendance_id)
    if not attendance:
        return jsonify({"error":"not found"}), 404
    storage.delete(attendance)
    storage.save()
    return jsonify({"message": "attendance record has been deleted"}), 200
