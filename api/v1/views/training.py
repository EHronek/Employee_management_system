#!/usr/bin/python3
from models import storage
from api.v1.views import app_views
from models.training import Training
from flask import request, jsonify

@app_views.route('/training', methods=['GET'], strict_slashes=False)
def get_trainings():
    """Retrieve all training records."""
    all_training = storage.all(Training)
    if not all_training:
        return jsonify({"error": "not found"}), 404
    trainings = [training.to_dict() for training in storage.all(Training).values()]
    return jsonify(trainings), 200


@app_views.route('/training/<training_id>', methods=['GET'], strict_slashes=False)
def get_training(training_id):
    """Retrieve a specific training record."""
    training = storage.get(Training, training_id)
    if not training:
        return jsonify({'error': 'Training not found'}), 404
    return jsonify(training.to_dict()), 200


@app_views.route('/training', methods=['POST'], strict_slashes=False)
def create_training():
    """Create a new training record."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid data'}), 400
    
    required_fields = ['employee_id', 'training_name', 'trainer_name', 'training_date']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400
    
    new_training = Training(**data)
    storage.new(new_training)
    storage.save()
    return jsonify(new_training.to_dict()), 201


@app_views.route('/training/<training_id>', methods=['PUT'], strict_slashes=False)
def update_training(training_id):
    """Update an existing training record."""
    training = storage.get(Training, training_id)
    if not training:
        return jsonify({'error': 'Training not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid data'}), 400
    
    for key, value in data.items():
        if hasattr(training, key):
            setattr(training, key, value)
    
    storage.save()
    return jsonify(training.to_dict()), 200


@app_views.route('/training/<training_id>', methods=['DELETE'], strict_slashes=False)
def delete_training(training_id):
    """Delete a training record."""
    training = storage.get(Training, training_id)
    if not training:
        return jsonify({'error': 'Training not found'}), 404
    
    storage.delete(training)
    storage.save()
    return jsonify({'message': 'Training deleted successfully'}), 200
