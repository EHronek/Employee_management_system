from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from web_dynamic.auth import role_required
from models import storage
from models.employee import Employee
from models.department import Department
from models.position import Position
from models.attendance import Attendance
from web_dynamic.helper_function import get_logged_in_user, get_managers, get_user_data
from datetime import datetime
from models.leave_request import LeaveRequest
from models.user import User

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
    sess = storage.get_session()
    user = get_logged_in_user()
    user_data = get_user_data()
    
    if not user:
        flash("You must be logged in to access the dashboard", "error")
        return redirect(url_for('login'))
    
    all_employees = storage.all(Employee).values()
    all_leave_requests = storage.all(LeaveRequest).values()

    total_employees = len(all_employees)

    active_employees = sum(1 for emp in all_employees if emp.status == 'active')

    on_leave = sum(1 for leave in all_leave_requests if leave.status == 'approved')

    pending_approvals = sum(1 for leave in all_leave_requests if leave.status == 'pending')
    
    # compute department-wise employee count
    department_counts = {}
    for emp in all_employees:
        department = emp.department.name if emp.department else "Unknown"
        department_counts[department] = department_counts.get(department, 0) + 1

    recent_notifications = [
        {"message": "Upcoming Performance Reviews", "time": "2 days ago"},
        {"message": "Pending Payroll Processing", "time": "1 day ago"},
        {"message": "Employee Contract Expiry Reminders", "time": "5 hours ago"}
    ]

    recent_activities = [
        {"message": "New Employee Registration: John Doe", "time": "3 hours ago"},
        {"message": "Salary Updated for Jane Smith", "time": "1 day ago"},
        {"message": "Performance Review Feedback Submitted", "time": "2 days ago"}
    ]

    return render_template(
        "employee_dashboard.html",
        active_employees=active_employees,
        on_leave=on_leave,
        pending_approvals=pending_approvals,
        department_data=department_counts,
        recent_notifications=recent_notifications,
        recent_activities=recent_activities,
        employees=all_employees,
        total_employees=total_employees,
        department=department
        )


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


@admin_bp.route("/employees/edit/<string:employee_id>", methods=["GET", "POST"], strict_slashes=False)
@role_required(["admin", "hr", "system admin"])
def edit_employee(employee_id):
    """ Edit Employee """
    employee = storage.get(Employee, employee_id)
    departments = storage.all(Department).values()
    positions = storage.all(Position).values()
    supervisors = storage.all(Employee).values()

    if not employee:
        flash("employee doesn't exist", "error")
        return render_template("employee_dashboard.html")
    
    if request.method == 'POST':
            employee.first_name = request.form.get('firstName')
            employee.last_name = request.form.get('lastName')
            employee.phone_number = request.form.get('phoneNumber')
            employee.salary = request.form.get('salary')
            
            # Handle hire date update
            hire_date_str = request.form.get("hireDate")
            if hire_date_str:
                try:
                    employee.hire_date = datetime.strptime(hire_date_str, "%Y-%m-%d")
                except:
                    flash("Invalid date format", "error")
                    return redirect(url_for("admin.edit_employee", employee_id=employee.id))
            
            employee.department_id = request.form.get('department_id')



            employee.position_id = request.form.get('position_id')
            employee.supervisor_id = request.form.get('supervisor_id')
            employee.status = request.form.get('status')

            try:
                employee.save()
                flash("Employee details updated successfully!", "success")

            except Exception as e:
                storage.get_session().rollback()
                flash(f"Error updating employee: {str(e)}", "danger")

            # return redirect(url_for('admin.employee_dashboard'))
    

    return render_template("edit_employee.html",
                           employee=employee,
                           departments=departments,
                           supervisors=supervisors,
                           positions=positions)


@admin_bp.route("/employees/view", methods=["GET"], strict_slashes=False)
def view_employees():
    """Render the view employees page with dynamic data"""
    search_query = request.args.get('search', '').strip().lower()
    filter_status = request.args.get('status', '').strip().lower()

    employees = storage.all(Employee).values()

    # Apply searching
    if search_query:
        employees = [emp for emp in employees if search_query in f"{emp.first_name} {emp.last_name}".lower()]

    if filter_status:
        employees = [emp for emp in employees if emp.status.lower() == filter_status]

    return render_template('view_employee.html', employees=employees)


@admin_bp.route("employees/delete/<string:employee_id>", methods=["POST"], strict_slashes=False)
def delete_employee(employee_id):
    employee = storage.get(Employee, employee_id)

    if not employee:
        flash("Employee not found", "danger")
        return redirect(url_for('admin.view_employee'))
    
    storage.delete(employee)
    storage.save()

    flash("employee deleted successfully", "success")


@admin_bp.route("/departments", methods=["GET"], strict_slashes=False)
@role_required(["admin", "hr", "system admin"])
def department_dashboard():
    """ Department Management """
    current_user = get_logged_in_user()
    user_data = get_user_data()

    departments = storage.all(Department).values()

    department_data = []
    for dept in departments:
        manager = storage.get(Employee, dept.manager_id) if dept.manager_id else None
        employees_count = len([emp for emp in storage.all(Employee).values() if emp.department_id == dept.id])

        department_data.append({
            "id": dept.id,
            "name": dept.name,
            "manager": f"{manager.first_name} {manager.last_name}" if manager else "N/A",
            "budget": f"${dept.budget:,.2f}",
            "employees": employees_count
        })
    

    return render_template("department.html", departments=department_data, user=user_data)


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


@admin_bp.route("/departments/edit/<string:dept_id>", methods=["GET", "POST"], strict_slashes=False)
@role_required(["admin", "hr", "system admin"])
def edit_department(dept_id):
    """ Edit Department """
    redirect_url = None  # Initialize redirect variable
    department = storage.get(Department, dept_id)

    if not department:
        flash("Department not found!", "error")
        return redirect(url_for('admin.department_dashboard'))

    if request.method == "POST":
        name = request.form.get('name')
        description = request.form.get('description')
        manager_id = request.form.get('departmentManager')
        budget = request.form.get('budget')

        # Check if required fields are provided
        if not name or not budget or not description or not manager_id:
            flash("All fields are required!", "error")
            return render_template("edit_department.html", department=department, managers=get_managers(), user_data=get_user_data())

        # Ensure budget is a valid number
        try:
            budget = float(budget)
            if budget < 0:
                flash("Budget must be a positive number.", "error")
                return render_template("edit_department.html", department=department, managers=get_managers(), user_data=get_user_data())
        except ValueError:
            flash("Invalid budget amount.", "error")
            return render_template("edit_department.html", department=department, managers=get_managers(), user_data=get_user_data())

        # Check if another department has the same name
        existing_department = storage.all(Department).values()
        for dep in existing_department:
            if dep.name.lower() == name.lower() and dep.id != dept_id:
                flash("Another department with this name already exists.", "error")
                return render_template("edit_department.html", department=department, managers=get_managers(), user_data=get_user_data())

        # Update department details
        department.name = name
        department.description = description
        department.manager_id = manager_id
        department.budget = budget

        storage.save()

        flash("Department updated successfully!", "success")
        redirect_url = url_for('admin.department_dashboard')

    return render_template("edit_department.html", department=department, managers=get_managers(), user_data=get_user_data(), redirect_url=redirect_url)



@admin_bp.route("/departments/delete", methods=["GET", "POST"], strict_slashes=False)
@role_required(["admin", "hr", "system admin"])
def delete_department():
    """ Delete Department by department ID"""
    current_user = get_logged_in_user()
    if not current_user:
        return redirect(url_for("login_page"))
    
    dept_id = request.args.get("dept_id")
    if not dept_id:
        flash("Invalid department ID!", "danger")
        return redirect(url_for("admin.department_dashboard"))
    
    department = storage.get(Department, dept_id)
    if not department:
        flash("Department not found", "danger")
        return redirect(url_for("admin.department_dashboard"))
    
    try:
        storage.delete(department)
        storage.save()
        flash("Department deleted successfully!", "success")

    except Exception as e:
        storage.get_session().rollback()
        flash(f"Error deleting department: {str(e)}", "danger")

  
    return redirect(url_for("admin.department_dashboard"))


@admin_bp.route("/create_user", methods=["GET", "POST"], strict_slashes=False)
@role_required(["admin", "hr", "system admin"])
def create_user():
    """Creates a new user"""
    employees = storage.all(Employee).values()
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get("password")
        role = request.form.get('role')
        employee_id = request.form.get('employee_id')
        status =request.form.get('status')

        if not all([username, password, role, employee_id]):
            flash("All fields are required", "danger")
            return redirect(url_for('admin.create_user'))
        
        existing_user = storage.get_user_by_username(username)
        if existing_user:
            flash("username already exists", "danger")
            return redirect(url_for('admin.create_user'))
        
        new_user = User(username=username, role=role, employee_id=employee_id)
        new_user.password = new_user._hash_password(password)
        storage.new(new_user)
        storage.save()
        flash('User created successfully', 'success')
        return redirect(url_for('admin.admin_dashboard'))

    
    return render_template('create_user.html', employees=employees)


@admin_bp.route("/edit_user<string:user_id>", methods=["GET"], strict_slashes=False)
@role_required(["admin", "hr", "system admin"])
def edit_user(user_id):
    """edits an existing user data"""
    user = storage.get(User, user_id)
    if not user:
        flash("User not found", 'danger')
        return redirect(url_for('admin.admin_dashboard'))
    
    if request.method == "POST":
        username = request.form.get('username')
        role = request.form.get('role')
        employee_id = request.form.get('employee_id')
        status = request.form.get('status')

        if not all([username, role, employee_id, status]):
            flash("All fields are required", "danger")
            return redirect(url_for('edit_user', user_id=user_id))
        
        user.username = username
        user.role = role
        user.employee_id = employee_id
        user.status = status
        storage.save()
        flash("user updated successfully", "success")
        return redirect(url_for("admin.admin_dashboard"))
    
    employees = storage.all(Employee).values()
    return render_template('edit_user.html', user=user, employees=employees)


@admin_bp.route('/users', methods=['GET'])
def list_users():
    users = storage.all(User).values()  # Fetch all users from the database
    return render_template('list_users.html', users=users)


@admin_bp.route('/delete_user/<string:user_id>', methods=['POST'])
def delete_user(user_id):
    """Handles deleting a user"""
    user = User.query.get(user_id)
    if user:
        storage.delete(user)
        storage.save()
        flash("User deleted successfully", "success")
    else:
        flash("User not found", "error")
    return redirect(url_for('admin.list_users'))



@admin_bp.route("/reports", methods=["GET"], strict_slashes=False)
@role_required(["admin", "hr", "system admin"])
def generate_reports():
    """ Generate Reports """
    return render_template("generate_reports.html")
