from sqlalchemy import func
from .extensions import db
from .models import User, Course, Enrol, UserEnrolment, Quiz, QuizAttempt, GradeItem, GradeGrade, LogEntry
from datetime import datetime

def format_ts(ts):
    if ts is None or ts == 0:
        return None
    return datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d %H:%M")

def get_active_students():
    sub = db.session.query(UserEnrolment.userid).distinct().subquery()
    return db.session.query(User).filter(User.id.in_(sub)).all()

def get_student_course_features(user_id, course_id):
    log_count = db.session.query(func.count(LogEntry.id)).filter_by(userid=user_id, courseid=course_id).scalar() or 0

    quiz_ids = db.session.query(Quiz.id).filter(Quiz.courseid == course_id).subquery()
    attempts = db.session.query(QuizAttempt).filter(
        QuizAttempt.userid == user_id,
        QuizAttempt.quizid.in_(quiz_ids),
        QuizAttempt.state == "finished"
    ).all()

    total_attempts = len(attempts)
    avg_grade = None
    if attempts:
        avg_grade = float(sum(a.sumgrades for a in attempts) / len(attempts))

    return {
        "log_count": log_count,
        "quiz_attempts": total_attempts,
        "avg_quiz_score": avg_grade,
    }

def get_student_overview(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return None

    course_ids = (
        db.session.query(Course.id)
        .join(Enrol, Enrol.courseid == Course.id)
        .join(UserEnrolment, UserEnrolment.enrolid == Enrol.id)
        .filter(UserEnrolment.userid == user_id)
        .all()
    )

    overview = {
        "user_id": user.id,
        "name": user.fullname,
        "email": user.email,
        "lastaccess": format_ts(user.lastaccess),
        "courses": []
    }

    for (cid,) in course_ids:
        course = db.session.get(Course, cid)
        features = get_student_course_features(user_id, cid)
        overview["courses"].append({
            "course_id": cid,
            "course_name": course.fullname,
            **features
        })

    return overview
