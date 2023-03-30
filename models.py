
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Student(db.Model):
    __tablename__ = "Students"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    grade = db.Column(db.REAL)
    date_created = db.Column(db.DateTime, default=datetime.now)


def get_student(name):
    student = Student.query.filter_by(name=name).first()
    if not student is None:
        return student
    return None


def student_exists(name):
    student = get_student(name)
    if not student is None:
        return True
    return False


def get_student_grade(name):
    student = get_student(name)
    if not student is None:
        return student.grade
    raise KeyError("Student does not exist in database")


def add_student(name, grade):
    if student_exists(name):
        raise ValueError("Student already exists in database")

    db.session.add(Student(name=name, grade=grade))
    db.session.commit()


def update_student(name, grade):
    student = get_student(name)
    if not student is None:
        student.grade = grade
        db.session.commit()
    else:
        raise KeyError("Student does not exist in database")


def remove_student(name):
    rows = Student.query.filter_by(name=name).delete()
    if rows == 0:
        raise KeyError("Student does not exist")
    else:
        db.session.commit()


def get_student_json():
    students = Student.query.all()
    data = {}
    for s in students:
        data[s.name] = s.grade

    return data
