#!/usr/bin/python3
"""Defines endpoint for payroll"""
from flask import Flask, jsonify, request, abort
from models import storage
from models.payroll import Payroll
from api.v1.views import app_views


@app_views.route('/payrolls', methods=['GET'], strict_slashes=False)
def get_payrolls():
    """Retrieve all payroll records"""
    payrolls = [payroll.to_dict() for payroll in storage.all(Payroll).values()]
    if not payrolls:
        return jsonify({"error": "payrolls not found"}), 404
    return jsonify(payrolls), 200


@app_views.route('/payrolls/<payroll_id>', methods=['GET'], strict_slashes=False)
def get_payroll(payroll_id):
    """Retrieve a specific payroll record"""
    payroll = storage.get(Payroll, payroll_id)
    if not payroll:
        return jsonify({"error": "payroll not found"}), 404
    return jsonify(payroll.to_dict()), 200


@app_views.route('/payrolls', methods=['POST'], strict_slashes=False)
def create_payroll():
    """Create a new payroll record"""
    if not request.json:
        jsonify({"error": "Not a JSON"})
    
    required_fields = ["employee_id", "basic_salary", "deductions", "net_pay", "payment_status"]
    for field in required_fields:
        if field not in request.json:
            jsonify({"error": f"Missing {field}"}), 400
    
    data = request.get_json()
    payroll = Payroll(**data)
    payroll.save()
    return jsonify(payroll.to_dict()), 201


@app_views.route('/payrolls/<payroll_id>', methods=['PUT'], strict_slashes=False)
def update_payroll(payroll_id):
    """Update an existing payroll record"""
    payroll = storage.get(Payroll, payroll_id)
    if not payroll:
        jsonify({"error": "payroll not exists"}), 404
    
    if not request.json:
        jsonify({"Not a JSON"}), 400
    
    ignored_keys = ["id", "employee_id", "created_at", "updated_at"]
    for key, value in request.json.items():
        if key not in ignored_keys:
            if hasattr(payroll, key):
                setattr(payroll, key, value)
    
    payroll.save()
    return jsonify(payroll.to_dict())


@app_views.route('/payrolls/<payroll_id>', methods=['DELETE'], strict_slashes=False)
def delete_payroll(payroll_id):
    """Delete a payroll record"""
    payroll = storage.get(Payroll, payroll_id)
    if not payroll:
        abort(404)
    
    storage.delete(payroll)
    storage.save()
    return jsonify({}), 200
