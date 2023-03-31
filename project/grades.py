from flask import Blueprint, session, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db
import warnings

grades = Blueprint('grades', __name__)


def get_student(name):
    student = User.query.filter_by(name=name).first()
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
        return student.email
    raise KeyError("User does not exist in database")


def add_student(name, grade):
    if student_exists(name):
        raise ValueError("User already exists in database")

    db.session.add(User(name=name, email=grade))
    db.session.commit()


def update_student(name, grade):
    student = get_student(name)
    if not student is None:
        student.email = grade
        db.session.commit()
    else:
        raise KeyError("User does not exist in database")


def remove_student(name):
    rows = User.query.filter_by(name=name).delete()
    if rows == 0:
        raise KeyError("User does not exist")
    else:
        db.session.commit()


def get_student_json():
    students = User.query.all()
    data = {}
    for s in students:
        data[s.name] = s.email

    return data


@ grades.app_errorhandler(404)
def page_not_found(e):
    print(e)
    return render_template('404.html'), 404


@ grades.route('/')
def static_file():
    return render_template("grades.html")


@ grades.route('/grades', methods=['POST', 'GET'])
def handle_grades():
    if request.method == 'POST':
        data = request.json

        s_name = data["name"]
        s_grade = data["grade"]

        # If student in grades dict set the grade value for entry
        # to value from json
        try:
            add_student(s_name, s_grade)
            return "Success!", 200
        except ValueError:
            return f"{s_name} already exists", 409
        except Exception as e:
            warnings.warn(e)
    elif request.method == 'GET':
        return get_student_json()
    return "Method not supported", 501


@ grades.route('/grades/<student_name>', methods=["GET", "PUT", "DELETE"])
def handle_grades_request(student_name):
    if request.method == 'GET':
        try:
            # Get the grade value for student
            grade = get_student_grade(student_name)
            return {student_name: grade}
        except KeyError:
            # Return that student not in dict
            return f"{student_name} does not exist", 404
        except Exception as e:
            warnings.warn(e)

    elif request.method == "PUT":
        data = request.json
        s_grade = data['grade']

        try:
            update_student(student_name, s_grade)
            return "Success!", 200
        except KeyError:
            # Return that student not in db
            return f"{student_name} does not exist", 404
        except Exception as e:
            warnings.warn(e)
    elif request.method == "DELETE":
        try:
            remove_student(student_name)
            return "Success!", 200
        except KeyError:
            # Return status that student not in db
            return f"{student_name} does not exist", 404
        except Exception as e:
            warnings.warn(e)
    return "Method not supported", 501


if __name__ == '__main__':
    app.run(debug=True)
