from .extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class AppUser(UserMixin, db.Model):
    __tablename__ = "app_users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False, default="advisor")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == "admin"

class User(db.Model):
    __tablename__ = "mdl_user"
    id = db.Column(db.BigInteger, primary_key=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    email = db.Column(db.String(255))
    lastaccess = db.Column(db.Integer)

    @property
    def fullname(self):
        return f"{self.firstname} {self.lastname}"

class Course(db.Model):
    __tablename__ = "mdl_course"
    id = db.Column(db.BigInteger, primary_key=True)
    fullname = db.Column(db.String(254))
    shortname = db.Column(db.String(100))

class Enrol(db.Model):
    __tablename__ = "mdl_enrol"
    id = db.Column(db.BigInteger, primary_key=True)
    courseid = db.Column(db.BigInteger)

class UserEnrolment(db.Model):
    __tablename__ = "mdl_user_enrolments"
    id = db.Column(db.BigInteger, primary_key=True)
    enrolid = db.Column(db.BigInteger)
    userid = db.Column(db.BigInteger)

class Quiz(db.Model):
    __tablename__ = "mdl_quiz"
    id = db.Column(db.BigInteger, primary_key=True)
    courseid = db.Column(db.BigInteger)
    name = db.Column(db.String(255))
    grade = db.Column(db.Numeric(10, 2))

class QuizAttempt(db.Model):
    __tablename__ = "mdl_quiz_attempts"
    id = db.Column(db.BigInteger, primary_key=True)
    quizid = db.Column(db.BigInteger)
    userid = db.Column(db.BigInteger)
    attempt = db.Column(db.Integer)
    state = db.Column(db.String(20))
    sumgrades = db.Column(db.Numeric(10, 2))

class GradeItem(db.Model):
    __tablename__ = "mdl_grade_items"
    id = db.Column(db.BigInteger, primary_key=True)
    courseid = db.Column(db.BigInteger)
    itemmodule = db.Column(db.String(50))
    iteminstance = db.Column(db.BigInteger)

class GradeGrade(db.Model):
    __tablename__ = "mdl_grade_grades"
    id = db.Column(db.BigInteger, primary_key=True)
    itemid = db.Column(db.BigInteger)
    userid = db.Column(db.BigInteger)
    finalgrade = db.Column(db.Numeric(10, 2))

class LogEntry(db.Model):
    __tablename__ = "mdl_logstore_standard_log"
    id = db.Column(db.BigInteger, primary_key=True)
    userid = db.Column(db.BigInteger)
    courseid = db.Column(db.BigInteger)
    timecreated = db.Column(db.Integer)
    component = db.Column(db.String(100))
