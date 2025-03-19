#!/usr/bin/python3
from flask import jsonify, request
from models import storage
from models.overtime import Overtime
from api.v1.views import app_views


@app_views.route('/overtime', methods=['GET'])
def get_overtimes():
    overtimes = storage.all(Overtime).values()
    return jsonify([overtime.to_dict() for overtime in overtimes])

# Get a single overtime record by ID
@app_views.route('/overtime/<overtime_id>', methods=['GET'])
def get_overtime(overtime_id):
    overtime = storage.get(Overtime, overtime_id)
    if not overtime:
        return jsonify({'error': 'Overtime record not found'}), 404
    return jsonify(overtime.to_dict())

# Create a new overtime record
@app_views.route('/overtime', methods=['POST'])
def create_overtime():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid input'}), 400

    required_fields = ['employee_id', 'overtime_hours']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing {field}'}), 400
    
    new_overtime = Overtime(**data)
    storage.new(new_overtime)
    storage.save()
    return jsonify(new_overtime.to_dict()), 201

# Update an existing overtime record
@app_views.route('/overtime/<overtime_id>', methods=['PUT'])
def update_overtime(overtime_id):
    overtime = storage.get(Overtime, overtime_id)
    if not overtime:
        return jsonify({'error': 'Overtime record not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid input'}), 400
    
    for key, value in data.items():
        if hasattr(overtime, key):
            setattr(overtime, key, value)
    
    storage.save()
    return jsonify(overtime.to_dict())

# Delete an overtime record
@app_views.route('/overtime/<overtime_id>', methods=['DELETE'])
def delete_overtime(overtime_id):
    overtime = storage.get(Overtime, overtime_id)
    if not overtime:
        return jsonify({'error': 'Overtime record not found'}), 404

    storage.delete(overtime)
    storage.save()
    return jsonify({'message': 'Overtime record deleted'}), 200
