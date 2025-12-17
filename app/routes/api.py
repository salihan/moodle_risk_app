from flask import Blueprint, jsonify
from flask_login import login_required
from ..moodle_queries import get_active_students
from ..risk_engine import compute_risk_for_student

api_bp = Blueprint("api", __name__)

@api_bp.route("/students")
@login_required
def api_students():
    students = get_active_students()
    out = []
    for s in students:
        r = compute_risk_for_student(s.id)
        if r:
            out.append({
                "user_id": r["user_id"],
                "name": r["name"],
                "risk_score": r["risk_score"],
                "risk_label": r["risk_label"]
            })
    return jsonify(out)

@api_bp.route("/students/<int:user_id>")
@login_required
def api_student_detail(user_id):
    info = compute_risk_for_student(user_id)
    if not info:
        return jsonify({"error": "not found"}), 404
    return jsonify(info)
