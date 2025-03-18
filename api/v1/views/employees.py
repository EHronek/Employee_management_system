#!/usr/bin/python3
"""Defines the API endpoint for employee crud operations"""
from flask import jsonify, request
from models import storage
from models.employee import Employee
from api.v1.views import app_views


@app_views.route('/employees', methods=['GET'], strict_slashes=False)
def get_employees():
    """Retrieves all employees"""
    all_employees = storage.all(Employee).values()
    if not all_employees:
       return jsonify({"error": "not found"})
    return jsonify([employee.to_dict() for employee in all_employees])


@app_views.route('/employees/<employee_id>', methods=["GET"], strict_slashes=False)
def get_employee_by_id(employee_id):
    """Retrieves a single employee"""
    fetched_employee = storage.get(Employee, employee_id)

    if not fetched_employee:
        return jsonify({"error": "not found"})
    return jsonify(fetched_employee.to_dict())


@app_views.route('/employees', methods=["POST"], strict_slashes=False)
def create_employee():
    """Create a new employee"""
    request_data = request.get_json(silent=True)
    if not request_data:
        return jsonify({"error": "not a JSON"}), 400
    
    if "first_name" not in request_data:
        return jsonify({"error": "missing first_name"}), 400
    elif "last_name" not in request_data:
        return jsonify({"error": "missing last_name"}), 400
    elif "work_email" not in request_data:
        return jsonify({"error": "missing work_email"}), 400
    elif "phone_number" not in request_data:
        return jsonify({"error": "missing phone number"}), 400
    elif "department_id" not in request_data:
        return jsonify({"error": "missing department id"}), 400
    elif "position_id" not in request_data:
        return jsonify({"error": "missing position id"}), 400
    
    new_employee = Employee(**request_data)

    storage.new(new_employee)
    storage.save()
    return jsonify(new_employee.to_dict()), 201

    
@app_views.route('/employees/<employee_id>', methods=["PUT"], strict_slashes=False)
def update_employee(employee_id):
    """Updates an employee"""
    fetched_employee = storage.get(Employee, employee_id)

    if not fetched_employee:
        return jsonify({"error": "employee record not found"}), 404
    
    new_data = request.get_json(silent=True)

    if not new_data:
        return jsonify({"error": "not valid JSON"})
    
    keys_to_ignore = {"id", "created_at", "updated_at"}

    for k, v in new_data.items():
        if k not in keys_to_ignore:
            setattr(fetched_employee, k, v)
    fetched_employee.save()
    return jsonify(fetched_employee.to_dict()), 200


@app_views.route('/employees/<employee_id>', methods=["DELETE"], strict_slashes=False)
def delete_employee(employee_id):
    """Deletes an employee from the database"""
    employee = storage.get(Employee, employee_id)

    if not employee:
        return jsonify({"error": "employee not found"})
    storage.delete(employee)
    storage.save()
    return jsonify({"success": f"employee with name {employee.first_name} deleted successfully"}), 200
