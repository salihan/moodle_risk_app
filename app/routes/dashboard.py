from flask import Blueprint, render_template
from flask_login import login_required
from ..moodle_queries import get_active_students
from ..risk_engine import compute_risk_for_student

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
@login_required
def index():
    students = get_active_students()
    data = []
    for s in students:
        info = compute_risk_for_student(s.id)
        if info:
            data.append(info)
    data.sort(key=lambda x: x["risk_score"], reverse=True)
    return render_template("dashboard.html", students=data)

@dashboard_bp.route("/students/<int:user_id>")
@login_required
def student_detail(user_id):
    info = compute_risk_for_student(user_id)
    if not info:
        return "Student not found", 404
    return render_template("student_detail.html", student=info)
