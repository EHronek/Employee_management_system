from flask import Blueprint, render_template, jsonify, session, redirect, url_for, request, flash, send_from_directory
from web_dynamic.auth import role_required
from web_dynamic.helper_function import get_logged_in_user, get_user_data
from models import storage
from models.employee import Employee
from models.attendance import Attendance
from datetime import datetime, date
from models.leave_request import LeaveRequest
from models.position import Position
from models.department import Department
import os

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


@employee_bp.route("/attendance", methods=["GET", "POST"], strict_slashes=False)
@role_required(["employee", "admin"])
def employee_attendance():
    """ Employee Attendance """
    current_user = get_logged_in_user()
    employee_id = current_user.employee_id

    now = datetime.utcnow()
    today = now.date()

    # Retrieve attendance record for today
    attendance = next(
        (record for record in storage.all(Attendance).values()
         if record.employee_id == employee_id and record.date.date() == today),
        None
    )

    if request.method == "POST":
        action = request.form.get("action")
        response = {"success": False, "message": ""}

        if action == "checkin":
            if attendance and attendance.check_in_time:
                response["message"] = "You have already checked in today!"
            else:
                attendance = Attendance(
                    employee_id=employee_id,
                    date=now,
                    check_in_time=now,
                    status="present"
                )
                storage.new(attendance)
                storage.save()
                response["success"] = True
                response["message"] = "Check-in successful!"

        elif action == "checkout":
            if not attendance or not attendance.check_in_time:
                response["message"] = "You must check in first!"
            elif attendance.check_out_time:
                response["message"] = "You have already checked out today!"
            else:
                attendance.check_out_time = now
                storage.save()
                response["success"] = True
                response["message"] = "Check-out successful!"

        return jsonify(response)

    # Fetch attendance history
    attendance_records = [
        {
            "date": record.date.strftime("%Y-%m-%d"),
            "check_in_time": record.check_in_time.strftime("%H:%M:%S") if record.check_in_time else "-",
            "check_out_time": record.check_out_time.strftime("%H:%M:%S") if record.check_out_time else "-",
            "status": record.status
        }
        for record in storage.all(Attendance).values() if record.employee_id == employee_id
    ]

    checked_in = attendance and attendance.check_in_time and not attendance.check_out_time

    employee = storage.get(Employee, current_user.employee_id)
    department = storage.get(Department, employee.department_id)
    position = storage.get(Position, employee.position_id)
    return render_template(
        "employeeAttendance.html",
        attendance_records=attendance_records,
        current_user=current_user,
        checked_in=checked_in,
        employee=employee,
        position=position,
        department=department
    )

@employee_bp.route("/leave", methods=["GET", "POST"], strict_slashes=False)
@role_required(["employee", "admin"])
def employee_leave_request():
    """Handles leave request creation and retrieval"""
    sess = storage.get_session()
    # Ensure employee is logged in
    employee_id = session.get("employee_id")
    if not employee_id:
        flash("Please log in to request leave.", "error")
        return redirect(url_for("auth.login"))  # Adjust based on your auth system

    # Fetch the logged-in employee
    employee = storage.get(Employee, employee_id)
    if not employee:
        flash("Invalid employee session!", "error")
        return redirect(url_for("auth.login"))
    
    last_leave = (
        sess.query(LeaveRequest)
        .filter_by(employee_id=employee_id)
        .order_by(LeaveRequest.created_at.desc())
        .first()
    )
    leave_balance = last_leave.leave_balance if last_leave else 30

    if request.method == 'POST':
        # Retrieve form data
        leave_type = request.form.get("leaveType")
        start_date = request.form.get("startDate")
        end_date = request.form.get("endDate")
        reason = request.form.get("reason")
        document = request.files.get("document")  # Handle file upload (optional)

        # Validate input
        if not leave_type or not start_date or not end_date or not reason:
            flash("All fields except the document are required!", "error")
            return redirect(url_for("employee.employee_leave_request"))

        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            flash("Invalid date format!", "error")
            return redirect(url_for("employee.employee_leave_request"))

        if start_date > end_date:
            flash("End date cannot be before start date!", "error")
            return redirect(url_for("employee.employee_leave_request"))

        # Calculate leave days
        requested_days = (end_date - start_date).days + 1
        new_balance = leave_balance - requested_days

        if new_balance < 0:
            flash("Insuffiecient leave balance!", "error")
            return redirect(url_for("employee.employee_leave_request"))
        
        if requested_days > leave_balance:
            flash("Insufficient leave balance!", "error")
            return redirect(url_for("employee.employee_leave_request"))

        # Handle file upload (if a document is provided)
        upload_dir = "static/uploads"
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        document_path = f"uploads/{document.filename}"
        document.save(os.path.join(upload_dir, document.filename))  # Save file in static/uploads

        if document and document.filename:
            document_path = f"uploads/{document.filename}"
            document.save(f"static/{document_path}")  # Save file in static/uploads

        # Create new LeaveRequest object
        new_leave = LeaveRequest(
            employee_id=employee_id,
            leave_type=leave_type,
            start_date=start_date,
            end_date=end_date,
            reason=reason,
            document=document_path,
            status="pending",
            leave_balance=new_balance
        )
        storage.new(new_leave)
        storage.save()

        flash("Leave request submitted successfully!", "success")
        return redirect(url_for("employee.employee_leave_request"))

    # Fetch leave requests for the logged-in employee
    leave_requests = [req for req in storage.all(LeaveRequest).values() if req.employee_id == employee_id]

    return render_template("leaveRequest.html", leave_requests=leave_requests, employee=employee, leave_balance=leave_balance)


@employee_bp.route("/leave/cancel/<string:leave_id>", methods=["GET", "POST"], strict_slashes=False)
@role_required(["employee", "admin"])
def cancel_leave(leave_id):
    """Handles leave cancellation."""
    leave_request = storage.get(LeaveRequest, leave_id)
    if not leave_request:
        flash("Leave request not found!", "error")
        return redirect(url_for("employee.employee_leave_request"))

    # Ensure only the requesting employee or admin can cancel
    employee_id = session.get("employee_id")
    if leave_request.employee_id != employee_id:
        flash("Unauthorized action!", "error")
        return redirect(url_for("employee.employee_leave_request"))

    # Cancel the leave
    storage.delete(leave_request)
    storage.save()

    flash("Leave request cancelled successfully!", "success")
    return redirect(url_for("employee.employee_leave_request"))



@employee_bp.route('/leave/download/<filename>')
def download_file(filename):
    return send_from_directory("static/uploads", filename, as_attachment=True)



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
