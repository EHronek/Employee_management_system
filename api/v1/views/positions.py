#!/usr/bin/python3
"""Defines the API endpoint for positions"""
from models import storage
from flask import jsonify, request
from models.position import Position
from api.v1.views import app_views


@app_views.route("/positions", methods=["GET"], strict_slashes=False)
def get_positions():
    """Retrieves all job positions"""
    all_positions = storage.all(Position).values()
    
    if not all_positions:
        return jsonify({"error": "positions not found"}), 404
    
    return jsonify([position.to_dict() for position in all_positions]), 200


@app_views.route("/positions/<position_id>", methods=["GET"], strict_slashes=False)
def get_position_by_id(position_id):
    """Retrieves a specific job position"""
    fetched_position = storage.get(Position, position_id)

    if not fetched_position:
        return jsonify({"error": "position not found"}), 400
    return jsonify(fetched_position.to_dict()), 200


@app_views.route("/positions", methods=["POST"], strict_slashes=False)
def create_position():
    """Creates a new job position"""
    new_data = request.get_json(silent=True)

    if not new_data:
        return jsonify({"error": "not a valid JSON"})

    if "title" not in new_data:
        return jsonify({"error": "missing title"}), 400
    elif "salary_range_min" not in new_data:
        return jsonify({"error": "missing salary_range_min"}), 400
    elif "salary_range_max" not in new_data:
        return jsonify({"error": "missing salary_range_max"}), 400
    elif "job_description" not in new_data:
        return jsonify({"error": "missing job_description"}), 400
    
    new_position = Position(**new_data)

    storage.new(new_position)
    storage.save()
    return jsonify(new_position.to_dict()), 200

@app_views.route("/positions/<position_id>", methods=["PUT"], strict_slashes=False)
def update_position(position_id):
    """Updates a Job position details"""
    position = storage.get(Position, position_id)

    if not position:
        return jsonify({"error": "Position not found"}), 404
    
    new_data = request.get_json(silent=True)
    
    if not new_data:
        return jsonify({"error": "not a valid json"}), 400
    
    keys_to_ignore = {"id", "created_at", "updated_at"}
    for key, value in new_data.items():
        if key not in keys_to_ignore:
            setattr(position, key, value)
    position.save()
    return jsonify(position.to_dict()), 200

@app_views.route("/positions/<position_id>", methods=["DELETE"], strict_slashes=False)
def delete_position(position_id):
    """Delete a job position"""
    position = storage.get(Position, position_id)

    if not position:
        return jsonify({"error": "position not found"}), 404
    
    storage.delete(position)
    storage.save()
    return jsonify({"success":f"success deleted positon : {position.title}"}), 200
    