#!/usr/bin/python3
from models import storage
import uuid
from os import environ
from flask import Flask, render_template


app = Flask(__name__)


@app.teardown_appcontext
def close_db(error):
    """Remove the current session"""
    storage.close()


@app.route("/", methods=["GET"], strict_slashes=False)
def landing_page():
    """Main landing page"""
    cache_id = uuid.uuid4()
    return render_template("landingPage.html", cache_id=cache_id)


@app.route("/login", methods=["GET"], strict_slashes=False)
def login_page():
    """Login"""
    cache_id = uuid.uuid4()
    return render_template("login.html", cache_id=cache_id)


@app.route("/sign-up", methods=["GET"], strict_slashes=False)
def sign_up():
    """Login"""
    cache_id = uuid.uuid4()
    return render_template("signup.html", cache_id=cache_id)



@app.route("/admin_dashboard", methods=["GET"], strict_slashes=False)
def admin_dashboard():
    """admin dashboard"""
    cache_id = uuid.uuid4()
    return render_template("admin_dashboard.html", cache_id=cache_id)


@app.route("/admin_dashboard/employees/add_employee", methods=["GET"], strict_slashes=False)
def add_new_employee():
    """form to add new employee"""
    cache_id = uuid.uuid4()
    return render_template("add_employee.html", cache_id=cache_id)


@app.route("/admin_dashboard/employees", methods=["GET"], strict_slashes=False)
def employee_dashboard():
    """edit and existing employee"""
    cache_id = uuid.uuid4()
    return render_template("employee_dashboard.html", cache_id=cache_id)


@app.route("/admin_dashboard/employees/edit_employee", methods=["GET"], strict_slashes=False)
def edit_employee():
    """edit and existing employee"""
    cache_id = uuid.uuid4()
    return render_template("edit_employee.html", cache_id=cache_id)


@app.route("/admin_dashboard/employees/view_employee", methods=["GET"], strict_slashes=False)
def view_employee():
    """view and existing employee"""
    cache_id = uuid.uuid4()
    return render_template("view_employee.html", cache_id=cache_id)


@app.route("/admin_dashboard/departments", methods=["GET"], strict_slashes=False)
def departments():
    """department_dashboard"""
    cache_id = uuid.uuid4()
    return render_template("department.html", cache_id=cache_id)


@app.route("/admin_dashboard/departments/add_department", methods=["GET"], strict_slashes=False)
def add_departments():
    """ add department"""
    cache_id = uuid.uuid4()
    return render_template("add_department.html", cache_id=cache_id)


@app.route("/admin_dashboard/departments/update_department", methods=["GET"], strict_slashes=False)
def update_departments():
    """ update department"""
    cache_id = uuid.uuid4()
    return render_template("update_department.html", cache_id=cache_id)



@app.route("/admin_dashboard/reports", methods=["GET"], strict_slashes=False)
def generate_reports():
    """ Generate reports"""
    cache_id = uuid.uuid4()
    return render_template("generate_reports.html", cache_id=cache_id)


@app.route("/employees/employee_dashboard", methods=["GET"], strict_slashes=False)
def employee_dash():
    """ Retrieves the employee dashboard """
    cache_id = uuid.uuid4()
    return render_template("employeeDashboard.html", cache_id=cache_id)


@app.route("/employees/employee_attendance", methods=["GET"], strict_slashes=False)
def employee_attendance():
    """ Retrieves the employee attendance """
    cache_id = uuid.uuid4()
    return render_template("employeeAttendance.html", cache_id=cache_id)


@app.route("/employees/leave_request", methods=["GET"], strict_slashes=False)
def employee_leave_request():
    """ Retrieves the employee attendance """
    cache_id = uuid.uuid4()
    return render_template("leaveRequest.html", cache_id=cache_id)


@app.route("/employees/company_announcements", methods=["GET"], strict_slashes=False)
def company_announcements():
    """ Retrieves the employee attendance """
    cache_id = uuid.uuid4()
    return render_template("companyAnnouncements.html", cache_id=cache_id)


@app.route("/employees/account_settings", methods=["GET"], strict_slashes=False)
def account_settings():
    """ Account settings """
    cache_id = uuid.uuid4()
    return render_template("account_settings.html", cache_id=cache_id)


@app.route("/employees/training_development", methods=["GET"], strict_slashes=False)
def training_development():
    """ Training development """
    cache_id = uuid.uuid4()
    return render_template("training_development.html", cache_id=cache_id)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)