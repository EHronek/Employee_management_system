#!/usr/bin/python3
"""Define API endpoint for departments and all crud operations"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.department import Department

@app_views.route("/departments", methods=['GET'], strict_slashes=False)
def get_departments():
    """Retrieves all Departments"""
    all_departments = storage.all(Department).values()
    return jsonify([department.to_dict() for department in all_departments]), 200


@app_views.route("/departments/<department_id>", methods=["GET"], strict_slashes=False)
def get_department_by_id(department_id):
    """Gets a specific department by id"""
    fetched_department = storage.get(Department, department_id)

    if not fetched_department:
        return jsonify({"error": "not found"}), 404
    return jsonify(fetched_department.to_dict())


@app_views.route('/departments', methods=["POST"], strict_slashes=False)
def create_department():
    """Creates a new department"""
    request_data = request.get_json(silent=True)
    if not request_data:
        return jsonify({"error": "not a json"}), 400
    if "name"not in request_data:
        return jsonify({"error": f"missing name"}), 400
    elif "description" not in request_data:
        return jsonify({'error': 'missing description'}), 400
    elif "budget" not in request_data:
        return jsonify({"error": "missing budget"}), 400
    
    new_department = Department(**request_data)
    storage.new(new_department)
    storage.save()
    return jsonify(new_department.to_dict()), 201

@app_views.route('/departments/<department_id>', methods=["PUT"], strict_slashes=False)
def update_department(department_id):
    """Updates an existing department data"""
    department = storage.get(Department, department_id)

    if not department:
        abort(404)

    new_data = request.get_json(silent=True)
    if not new_data:
        return jsonify({"error": "not a JSON"}), 400
    
    keys_to_ignore = {"id", "created_at", "updated_at"}
    for k, v in new_data.items():
        if k not in keys_to_ignore:
            setattr(department, k, v)
    department.save()
    return jsonify(department.to_dict()), 200

@app_views.route('/departments/<department_id>', methods=["DELETE"], strict_slashes=False)
def delete_department(department_id):
    """Deletes an existing department from the database"""
    department = storage.get(Department, department_id)

    if not department:
        jsonify({"error", "record not found"}), 404
    storage.delete(department)
    storage.save()
    return jsonify({"succes": "deletion successful"}), 200

