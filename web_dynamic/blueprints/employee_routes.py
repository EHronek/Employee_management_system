from flask import Blueprint, render_template
from web_dynamic.auth import role_required

employee_bp = Blueprint("employee", __name__)

@employee_bp.route("/dashboard", methods=["GET"], strict_slashes=False)
@role_required(["employee", "admin"])
def employee_dashboard():
    """ Employee Dashboard """
    return render_template("employeeDashboard.html")


@employee_bp.route("/attendance", methods=["GET"], strict_slashes=False)
@role_required(["employee", "admin"])
def employee_attendance():
    """ Employee Attendance """
    return render_template("employeeAttendance.html")


@employee_bp.route("/leave", methods=["GET"], strict_slashes=False)
@role_required(["employee", "admin"])
def employee_leave_request():
    """ Leave Request """
    return render_template("leaveRequest.html")


@employee_bp.route("/announcements", methods=["GET"], strict_slashes=False)
@role_required(["employee", "admin"])
def company_announcements():
    """ Company Announcements """
    return render_template("companyAnnouncements.html")

@employee_bp.route("/training", methods=["GET"], strict_slashes=False)
def training_development():
    """ Training and Development """
    return render_template("training_development.html")


@employee_bp.route("/settings", methods=["GET"], strict_slashes=False)
@role_required(["employee", "admin"])
def account_settings():
    """ Account Settings """
    return render_template("account_settings.html")
