#!/usr/bin/python3
from flask import Flask, jsonify, request, abort
from models import storage
from models.payroll import Payroll
from api.v1.views import app_views

@app_views.route('/payrolls', methods=['GET'], strict_slashes=False)
def get_payrolls():
    """Retrieve all payroll records"""
    payrolls = [payroll.to_dict() for payroll in storage.all(Payroll).values()]
    return jsonify(payrolls)

@app_views.route('/payrolls/<payroll_id>', methods=['GET'], strict_slashes=False)
def get_payroll(payroll_id):
    """Retrieve a specific payroll record"""
    payroll = storage.get(Payroll, payroll_id)
    if not payroll:
        abort(404)
    return jsonify(payroll.to_dict())

@app_views.route('/payrolls', methods=['POST'], strict_slashes=False)
def create_payroll():
    """Create a new payroll record"""
    if not request.json:
        abort(400, "Not a JSON")
    
    required_fields = ["employee_id", "basic_salary", "deductions", "net_pay", "payment_status"]
    for field in required_fields:
        if field not in request.json:
            abort(400, f"Missing {field}")
    
    data = request.get_json()
    payroll = Payroll(**data)
    payroll.save()
    return jsonify(payroll.to_dict()), 201

@app_views.route('/payrolls/<payroll_id>', methods=['PUT'], strict_slashes=False)
def update_payroll(payroll_id):
    """Update an existing payroll record"""
    payroll = storage.get(Payroll, payroll_id)
    if not payroll:
        abort(404)
    
    if not request.json:
        abort(400, "Not a JSON")
    
    ignored_keys = ["id", "employee_id", "created_at", "updated_at"]
    for key, value in request.json.items():
        if key not in ignored_keys:
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
