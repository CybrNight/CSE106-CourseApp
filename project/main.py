from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from . import db
from .models import Course
from flask import jsonify

main = Blueprint('main', __name__)


@main.route('/')
def index():
    if (current_user.is_authenticated):
        return render_template('index.html', name=current_user.name)
    else:
        return render_template('index.html', name='Guest')


@main.app_errorhandler(404)
def page_not_found(e):
    print(e)
    return render_template('error/404.html'), 404


@main.app_errorhandler(403)
def forbidden(e):
    print(e)
    return render_template('error/403.html'), 403


@main.route('/profile')
@login_required
def profile():
    return render_template('grades.html', name=current_user.name)


@main.route('/courses', methods=['GET'])
@login_required
def courses():
    # should be if user.type == 'teacher' once implemented
    if(current_user.name == 'Ammon Hepworth' or current_user.name == 'Ralph Jenkins'):
        return render_template('teacher.html', name=current_user.name)
    else:
        return render_template('courses.html', name=current_user.name)

@main.route('/courses/<course_name>', methods=['GET'])
@login_required
def course(course_name):
    return render_template('courseGrades.html', name=current_user.name, course=course_name)


@main.route('/getCourses', methods=['GET'])
@login_required
def get_courses():
    classes = Course.query.all()

    output = []
    for c in classes:
        in_class = False
        if c in current_user.courses:
            in_class = True
        course_data = {'courseName': c.course_name, 'prof': c.prof,
                       'time': c.time, 'enrolled': c.enrolled, 'maxEnroll': c.max_enroll, "in_class": in_class}
        output.append(course_data)
    return jsonify(output)


@main.route('/getEnrolled', methods=['GET'])
@login_required
def get_enrolled():
    classes = current_user.courses

    output = []
    for c in classes:
        course_data = {'courseName': c.course_name, 'prof': c.prof,
                       'time': c.time, 'enrolled': c.enrolled, 'maxEnroll': c.max_enroll}
        output.append(course_data)
    print(output)
    return jsonify(output)


@main.route('/courses/add', methods=['POST'])
@login_required
def add_course():
    data = request.json

    c_name = data["courseName"]
    course = Course.query.filter_by(course_name=c_name).first()

    if course:
        if course.enrolled < course.max_enroll and not course in current_user.courses:
            course.enrolled += 1
            current_user.courses.append(course)
            db.session.commit()
    return "Enrolled student in course", 205


@main.route('/courses/remove/<c_name>', methods=['DELETE'])
@login_required
def remove_course(c_name):

    course = Course.query.filter_by(course_name=c_name).first()

    if course:
        course.enrolled -= 1
        current_user.courses.remove(course)
        db.session.commit()
    print(f"De-Enrolled student from {c_name}")
    return "Success!", 205
