#!/usr/bin/python3
"""Checks the status of our api"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.user import User
from models.attendance import Attendance
from models.department import Department
from models.employee import Employee
from models.leave_request import LeaveRequest
from models.payroll import Payroll
from models.position import Position
from models.attendance import Attendance
from models.benefits import Benefits
from models.company_asset import CompanyAssets
from models.performance_review import PerformanceReview
from models.overtime import Overtime
from models.training import Training


@app_views.route('/status', methods=["GET"], strict_slashes=False)
def status():
    """Returns the status of the api"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """Retrieves the number of each object by type"""
    stats_data = {
        "users" : storage.count(User),
        "departments": storage.count(Department),
        "company_assets": storage.count(CompanyAssets),
        "employees": storage.count(Employee),
        "positions": storage.count(Position) 
    }

    return jsonify(stats_data), 200
