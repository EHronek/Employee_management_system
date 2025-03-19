#!/usr/bin/python3
"""Defines the ENDpoint for benefits"""
from models import storage
from models.benefits import Benefits
from api.v1.views import app_views
from flask import jsonify, request


@app_views.route("/benefits", methods=["GET"], strict_slashes=True)
def get_benefits():
    """Retrieve all benefits"""
    benefits = storage.all(Benefits).values()
    if not benefits:
        return jsonify({"error": "not found"}), 404
    return jsonify([benefit.to_dict() for benefit in benefits]), 200


@app_views.route("/benefits/<benefit_id>", methods=["GET"], strict_slashes=False)
def get_benefit(benefit_id):
    """Retrieve a specific benefit"""
    benefit = storage.get(Benefits, benefit_id)

    if not benefit:
        return jsonify({"error": "benefit not found"})
    return jsonify(benefit.to_dict())



@app_views.route("/benefits", methods=["POST"], strict_slashes=False)
def create_benefit():
    """Create a new benefit"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "not a valid json"}), 400
    
    fields = ["employee_id", "benefit_type"]
    for field in fields:
        if field not in data:
            return jsonify({"error": f"missing attribute name {field}"})
        
    benefit = Benefits(**data)
    benefit.save()
    return jsonify(benefit.to_dict()), 201


@app_views.route("/benefits/<benefit_id>", methods=["PUT"])
def update_benefit(benefit_id):
    """Update existing benefit"""
    benefit = storage.get(Benefits, benefit_id)
    if not benefit:
        return jsonify({"error": "benefit not found"}), 404
    
    data = request.get_json(silent=True)
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            if hasattr(benefit, key):
                setattr(benefit, key, value)

    benefit.save()
    return jsonify(benefit.to_dict()), 200


@app_views.route("/benefits/<benefit_id>", methods=["True"], strict_slashes=True)
def delete_benefit(benefit_id):
    """Delete a benefit"""
    benefit = storage.get(Benefits, benefit_id)
    if not benefit:
        return jsonify({"error": "benefit not found"}), 404
    storage.delete(benefit)
    storage.save()
    return jsonify({"message": "benefit deleted"}), 200

