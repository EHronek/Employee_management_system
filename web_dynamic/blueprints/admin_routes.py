from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from web_dynamic.auth import role_required
from models import storage
from models.employee import Employee
from models.department import Department
from models.position import Position
from models.attendance import Attendance
from web_dynamic.helper_function import get_logged_in_user, get_managers, get_user_data

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/dashboard", methods=["GET"], strict_slashes=False)
@role_required(["admin", "hr", "system admin"])
def admin_dashboard():
    """ Admin Dashboard """
    if request.method == "GET":
        user = get_logged_in_user()

        if not user:
            return redirect(url_for("login_page"))
        
        employee_id = user.employee_id

        user_data = storage.get(Employee, employee_id)

        employees = storage.all(Employee).values()
        departments = storage.all(Department).values()
        positions = storage.all(Position).values()



        data = {
            "employees" : employees,
            "departments": departments,
            "positions" : positions,
            "storage": storage,
            "user" : user,
            "user_data": user_data
        }
        return render_template("admin_dashboard.html", **data)


@admin_bp.route("/employees", methods=["GET"], strict_slashes=False)
@role_required(["admin", "hr", "system admin"])
def employee_dashboard():
    """ Employee Management """
    return render_template("employee_dashboard.html")


@admin_bp.route("/employees/add", methods=["GET", "POST"], strict_slashes=False)
@role_required(["admin", "hr", "system admin"])
def add_employee():
    """ Add Employee """
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        work_email = request.form.get("work_email")
        phone_number = request.form.get("phone_number")
        salary = request.form.get('salary')
        hire_date = request.form.get('hire_date')
        department_id = request.form.get('department_id')
        position_id = request.form.get('position_id')
        supervisor_id = request.form.get('supervisor_id')
        status = request.form.get('status')

        if not all([first_name, last_name, work_email, phone_number, salary,hire_date, department_id, position_id, supervisor_id, status]):
            flash("All fields are required!", "error")
            return redirect(url_for('add_employee'))
        
        new_employee = Employee(
            first_name=first_name,
            last_name=last_name,
            work_email=work_email,
            phone_number=phone_number,
            salary=salary,
            hire_date=hire_date,
            department_id=department_id,
            position_id=position_id,
            supervisor_id=supervisor_id,
            status=status
        )

        storage.new(new_employee)
        storage.save()
        flash("Employee added successfully!", "success")
        return redirect(url_for("admin.admin_dashboard"))
    
    user = get_logged_in_user()

    if not user:
        return redirect(url_for("login_page"))
    
    employee_id = user.employee_id
    user_data = storage.get(Employee, employee_id)

    employees = storage.all(Employee).values()
    positions = list(storage.all(Position).values())
    departments = list(storage.all(Department).values())

    supervisors = [emp for emp in employees if emp.id != employee_id]

    data = {
        "user_data": user_data,
        "positions": positions,
        "departments": departments,
        "supervisors": supervisors

    }
    return render_template("add_employee.html", **data)


@admin_bp.route("/employees/edit", methods=["GET"], strict_slashes=False)
@role_required(["admin", "hr", "system admin"])
def edit_employee():
    """ Edit Employee """
    return render_template("edit_employee.html")


@admin_bp.route("/departments", methods=["GET"], strict_slashes=False)
@role_required(["admin", "hr", "system admin"])
def department_dashboard():
    """ Department Management """
    return render_template("department.html")


@admin_bp.route("/departments/add", methods=["GET", "POST"], strict_slashes=False)
@role_required(["admin", "hr", "system admin"])
def add_department():
    """ Add Department """
    redirect_url = None  # Initialize redirect variable

    if request.method == "POST":
        name = request.form.get('name')
        description = request.form.get('description')
        manager_id = request.form.get('departmentManager')
        budget = request.form.get('budget')

        # Check if required fields are provided
        if not name or not budget or not description or not manager_id:
            flash("All fields are required!", "error")
            return render_template("add_department.html", managers=get_managers(), user_data=get_user_data())

        # Ensure budget is a valid number
        try:
            budget = float(budget)
            if budget < 0:
                flash("Budget must be a positive number.", "error")
                return render_template("add_department.html", managers=get_managers(), user_data=get_user_data())
        except ValueError:
            flash("Invalid budget amount.", "error")
            return render_template("add_department.html", managers=get_managers(), user_data=get_user_data())

        # Check if department already exists
        existing_department = storage.all(Department).values()
        for dep in existing_department:
            if dep.name.lower() == name.lower():
                flash("Department already exists and must be unique.", "error")
                return render_template("add_department.html", managers=get_managers(), user_data=get_user_data())

        # Create new department only if all validations pass
        new_department = Department(
            name=name,
            description=description,
            manager_id=manager_id,
            budget=budget
        )

        storage.new(new_department)
        storage.save()

        flash("Department added successfully!", "success")
        redirect_url = url_for('admin.department_dashboard')  # Set redirect URL

    return render_template("add_department.html", managers=get_managers(), user_data=get_user_data(), redirect_url=redirect_url)


@admin_bp.route("/reports", methods=["GET"], strict_slashes=False)
@role_required(["admin", "hr", "system admin"])
def generate_reports():
    """ Generate Reports """
    return render_template("generate_reports.html")
