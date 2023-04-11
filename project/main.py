from flask import Blueprint, redirect, render_template, request, session
from flask_login import login_required, current_user
from . import db
from .models import Course, User
from flask import jsonify
from .role import Role

main = Blueprint('main', __name__)


def get_prof_name(course):
    prof = User.query.join(Enrollment).join(Course).filter(
        (User.role == Role.PROFESSOR) & (Course.name == course.name)).all()
    '''prof = enrollment.course.filter(User.role == Role.PROFESSOR).all()'''
    prof_name = ""
    for p in prof:
        prof_name += p.name + "\n"
    return prof_name


@main.route('/')
def index():
    if (current_user.is_authenticated):
        return render_template('index.html', name=current_user.name)
    else:

        return render_template('index.html')


@main.app_errorhandler(404)
def page_not_found(e):
    print(e)
    return render_template('error/404.html'), 404


@main.app_errorhandler(403)
def forbidden(e):
    print(e)
    return render_template('error/403.html'), 403


@main.route('/courses', methods=['GET'])
@login_required
def courses():
    if current_user.is_admin():
        return redirect("/admin")

    if current_user.role == Role.PROFESSOR:
        return render_template('teacher.html')
    elif current_user.role == Role.STUDENT:
        return render_template('courses.html')
    return render_template('index.html')


@main.route('/courses/<c_name>', methods=['GET'])
@login_required
def course(c_name):
    return render_template('courseGrades.html', name=current_user.name, course=c_name)


@main.route('/courses/<c_name>/students', methods=['GET'])
def get_course_students(c_name):
    enrollments = Enrollment.query.join(User).join(Course).filter(
        (User.role == Role.STUDENT) & (Course.name == c_name)).all()

    output = []

    for e in enrollments:
        grade = {"id": e.user_id, "name": e.user.name, "grade": e.grade}
        output.append(grade)
    return jsonify(output)


@main.route('/getCourses', methods=['GET'])
@login_required
def get_courses():
    classes = Course.query.all()

    output = []
    for c in classes:
        in_class = False
        if c in current_user.courses:
            in_class = True

        prof_name = get_prof_name(c)

        course_data = {'courseName': c.name, 'prof': prof_name,
                       'time': c.time, 'enrolled': c.enrolled, 'maxEnroll': c.max_enroll, "in_class": in_class}
        output.append(course_data)
    return jsonify(output)


@ main.route('/getEnrolled', methods=['GET'])
@ login_required
def get_enrolled():
    classes = current_user.courses

    output = []
    for e in current_user.enrollment:
        c = e.course
        prof_name = "TEST"
        course_data = {'courseName': c.name, 'prof': prof_name,
                       'time': c.time, 'enrolled': c.enrolled, 'maxEnroll': c.max_enroll}
        output.append(course_data)
    print(output)
    return jsonify(output)


@ main.route('/courses/add', methods=['POST'])
@ login_required
def add_course():
    data = request.json

    c_name = data["courseName"]
    course = Course.query.filter_by(name=c_name).first()

    try:
        if course:
            course.add_user(current_user)
    except Exception as e:
        return "Course full", 409
    return "Enrolled student in course", 205


@ main.route('/courses/remove/<c_name>', methods=['DELETE'])
@ login_required
def remove_course(c_name):

    enrollment = Enrollment.query.join(Course).join(User).filter(
        ((Course.name == c_name) & (User.name == current_user.name)))
    course = enrollment.one().course
    if course:
        course.remove_user(current_user)
    print(f"De-Enrolled student from {c_name}")
    return "Success!", 205


@ main.route('/courses/<c_name>/students', methods=['PUT'])
@ login_required
def update_grades(c_name):
    data = request.json

    for user in data:
        for key, value in user.items():
            user = Enrollment.query.join(Course).join(User).filter(
                (User.role == Role.STUDENT) & (User.user_id == key) & (Course.name == c_name)).first()
            user.grade = value
    db.session.commit()
    return "Success!", 205
