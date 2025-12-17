from .moodle_queries import get_student_overview

def compute_risk_for_student(user_id):
    overview = get_student_overview(user_id)
    if not overview:
        return None

    total_logs = sum(c["log_count"] for c in overview["courses"])
    attempts = sum(c["quiz_attempts"] for c in overview["courses"])

    scores = [c["avg_quiz_score"] for c in overview["courses"] if c["avg_quiz_score"] is not None]
    avg_grade = sum(scores)/len(scores) if scores else None

    risk = 0
    if total_logs < 10: risk += 0.4
    if attempts == 0: risk += 0.4
    elif attempts < 3: risk += 0.2
    if avg_grade is not None and avg_grade < 6: risk += 0.2

    risk = min(risk, 1.0)
    label = "high" if risk >= 0.7 else "medium" if risk >= 0.4 else "low"

    overview["risk_score"] = risk
    overview["risk_label"] = label
    overview["avg_grade"] = avg_grade

    return overview
