from http.client import HTTPException
from flask import Blueprint, abort, redirect, render_template, request, session
from flask_login import login_required, fresh_login_required, current_user
from . import db
from .models import Course, User, Enrollment
from flask import jsonify
from .role import Role

main = Blueprint('main', __name__)


@ main.route('/')
def index():
    if (current_user.is_authenticated):
        return render_template('index.html')
    else:

        return render_template('index.html')


@ main.app_errorhandler(404)
def page_not_found(e):
    print(e)
    return render_template('error/404.html'), 404


@ main.app_errorhandler(403)
def forbidden(e):
    print(e)
    return render_template('error/403.html'), 403


@ main.route('/courses', methods=['GET'])
@login_required
def courses():
    if current_user.is_admin():
        return redirect("/admin")

    if current_user.role == Role.PROFESSOR:
        return render_template('teacher.html')
    elif current_user.role == Role.STUDENT:
        return render_template('courses.html')
    return render_template('index.html')


@ main.route('/courses/<c_id>', methods=['GET'])
@login_required
def course(c_id):
    course = Course.query.filter_by(course_id=c_id).first()
    prof = User.query.join(Enrollment).join(Course).filter(
        (User.role == Role.PROFESSOR) & (Course.course_id == c_id)).first()

    if not prof.user_id == current_user.user_id:
        abort(403)

    if course:
        return render_template('courseGrades.html', c_id=c_id, course=course.name)
    abort(404)


@ main.route('/courses/<c_id>/students', methods=['GET'])
@login_required
def get_course_students(c_id):
    enrollments = Enrollment.query.join(User).join(Course).filter(
        (User.role == Role.STUDENT) & (Course.course_id == c_id)).all()

    if len(enrollments) == 0:
        abort(404)

    output = []
    for e in enrollments:
        if e.user is None:
            continue

        user = {"id": e.user_id, "name": e.user.name, "grade": e.grade}
        output.append(user)
    return jsonify(output)


@ main.route('/getCourses', methods=['GET'])
@ login_required
def get_courses():
    classes = Course.query.all()

    output = []

    for c in classes:
        in_class = False

        for e in current_user.enrollment:
            if c == e.course:
                in_class = True

        course_data = {'courseId': c.course_id, 'courseName': c.name, 'prof': c.prof_name,
                       'time': c.time, 'enrolled': c.enrolled, 'maxEnroll': c.max_enroll, "in_class": in_class}
        output.append(course_data)

    return jsonify(output)


@ main.route('/getEnrolled', methods=['GET'])
@ login_required
def get_enrolled():
    output = []

    if len(current_user.enrollment) == 0:
        return {}, 200

    for e in current_user.enrollment:
        c = e.course

        course_data = {'courseId': c.course_id, 'courseName': c.name, 'prof': c.prof_name,
                       'time': c.time, 'enrolled': c.enrolled, 'maxEnroll': c.max_enroll}
        output.append(course_data)
    return jsonify(output)


@ main.route('/courses/add', methods=['POST'])
@ login_required
def add_course():
    data = request.json
    c_id = data['courseId']
    course = Course.query.filter_by(course_id=c_id).first()

    try:
        if course:
            course.add_user(current_user)
    except Exception as e:
        return "Course full", 409

    return "Enrolled student in course", 205


@ main.route('/courses/remove/<c_id>', methods=['DELETE'])
@ login_required
def remove_course(c_id):
    enrollment = Enrollment.query.join(Course).join(User).filter(
        ((Course.course_id == c_id) & (User.user_id == current_user.user_id)))
    enrollment = enrollment.first()
    if enrollment:
        enrollment.course.remove_user(current_user)
        print(f"De-Enrolled student from {c_id}")
        return "Success!", 205
    return "Student not enrolled in course", 404


@ main.route('/courses/<c_id>/students', methods=['PUT'])
@ login_required
def update_grades(c_id):
    data = request.json

    for user in data:
        for key, value in user.items():
            user = Enrollment.query.join(Course).join(User).filter(
                (User.role == Role.STUDENT) & (User.user_id == key) & (Course.course_id == c_id)).first()

            if not user:
                abort(404)

            user.grade = value
    db.session.commit()
    return "Success!", 205
