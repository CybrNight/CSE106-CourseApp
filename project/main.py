from flask import Blueprint, redirect, render_template, request, session
from flask_login import login_required, current_user
from . import db
from .models import Course, User, Enrollment
from flask import jsonify
from .role import Role

main = Blueprint('main', __name__)


def get_prof_name(course):
    prof = User.query.join(Enrollment).join(Course).filter(
        (User.role == Role.PROFESSOR) & (Course.course_name == course.course_name)).all()
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


@main.route('/courses/<course_name>', methods=['GET'])
@login_required
def course(course_name):
    return render_template('courseGrades.html', name=current_user.name, course=course_name)


@main.route('/courses/<c_name>/students', methods=['GET'])
def get_course_students(c_name):
    enrollments = Enrollment.query.join(User).join(Course).filter(
        (User.role == Role.STUDENT) & (Course.course_name == c_name)).all()

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

        for e in current_user.enrollment:
            if c == e.course:
                in_class = True

        prof_name = get_prof_name(c)

        course_data = {'courseName': c.course_name, 'prof': prof_name,
                       'time': c.time, 'enrolled': c.enrolled, 'maxEnroll': c.max_enroll, "in_class": in_class}
        output.append(course_data)

    return jsonify(output)


@ main.route('/getEnrolled', methods=['GET'])
@ login_required
def get_enrolled():
    output = []
    for e in current_user.enrollment:
        c = e.course
        prof_name = "TEST"
        course_data = {'courseName': c.course_name, 'prof': prof_name,
                       'time': c.time, 'enrolled': c.enrolled, 'maxEnroll': c.max_enroll}
        output.append(course_data)
    return jsonify(output)


@ main.route('/courses/add', methods=['POST'])
@ login_required
def add_course():
    data = request.json

    c_name = data["courseName"]
    course = Course.query.filter_by(course_name=c_name).first()

    if course:
        if course.enrolled < course.max_enroll:
            course.enrolled += 1
            db.session.add(Enrollment(
                user=current_user, course=course, grade=100))
            db.session.commit()
    return "Enrolled student in course", 205


@ main.route('/courses/remove/<c_name>', methods=['DELETE'])
@ login_required
def remove_course(c_name):

    enrollment = Enrollment.query.join(Course).join(User).filter(
        ((Course.course_name == c_name) & (User.name == current_user.name)))
    course = enrollment.one().course
    if course:
        course.enrolled -= 1
        Enrollment.query.filter_by(course=course).delete()
        db.session.commit()
    print(f"De-Enrolled student from {c_name}")
    return "Success!", 205

@ main.route('/courses/<c_name>/students', methods=['PUT'])
@ login_required
def update_grades(c_name):
    data = request.json
    enrollment = Enrollment.query.join(User).join(Course).filter(
        (User.role == Role.STUDENT) & (Course.course_name == c_name)).all()
    print(data)
    for e in enrollment:
        e.grade = data["grades"][enrollment.index(e)]

    db.session.commit()
    return "Success!", 205
