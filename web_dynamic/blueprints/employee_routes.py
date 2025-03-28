from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from web_dynamic.auth import role_required
from web_dynamic.helper_function import get_logged_in_user, get_user_data
from models import storage
from models.employee import Employee


employee_bp = Blueprint("employee", __name__)

@employee_bp.route("/dashboard", methods=["GET"], strict_slashes=False)
@role_required(["employee", "admin"])
def employee_dashboard():
    """ Employee Dashboard """
    user = get_logged_in_user()
    if not user:
        flash("User needs to login to continue")
        return redirect(url_for('login_page'))
    
    employee_id = user.employee_id
    employee = storage.get(Employee, employee_id)

    if not employee:
        flash("Employee not found")
        return redirect(url_for('login_page'))

    # Calculate total hours worked
    attendance_records = employee.attendance_records
    total_hours = sum(
        (record.check_out_time - record.check_in_time).seconds / 3600
        for record in attendance_records if record.check_in_time and record.check_out_time
    )

    # Calculate remaining leave days
    approved_leaves = [
        request for request in employee.leave_requests if request.status == "approved"
    ]
    leave_days_remaining = sum((req.end_date - req.start_date).days for req in approved_leaves)

    # Get last payroll record
    last_payroll = employee.payroll_records[-1] if employee.payroll_records else None

    payroll_data = {
        "basic_salary": last_payroll.basic_salary if last_payroll else 0.0,
        "deductions": last_payroll.deductions if last_payroll else 0.0,
        "net_pay": last_payroll.net_pay if last_payroll else 0.0,
        "payment_date": last_payroll.payment_date.strftime("%Y-%m-%d") if last_payroll else "N/A",
        "payment_status": last_payroll.payment_status if last_payroll else "N/A",
    }

    # Get last performance review
    performance_rating = employee.performance_reviews[-1].score if employee.performance_reviews else 0

    # Recent notifications
    notifications = []
    for request in employee.leave_requests[-3:]:
        notifications.append(
            {
                "message": f"Leave request {request.status}: {request.start_date} to {request.end_date}",
                "time": request.updated_at.strftime("%Y-%m-%d %H:%M"),
            }
        )

    for payroll in employee.payroll_records[-3:]:
        notifications.append(
            {
                "message": f"Salary payment of ${payroll.net_pay:.2f} received",
                "time": payroll.payment_date.strftime("%Y-%m-%d %H:%M"),
            }
        )

    return render_template(
        "employeeDashboard.html",
        employee=employee,
        attendance_data={
            "total_hours": round(total_hours, 2),
            "leave_days_remaining": leave_days_remaining,
            "payroll": payroll_data,
            "performance_rating": performance_rating,  # Updated key
        },
        notifications=notifications,
    )


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
