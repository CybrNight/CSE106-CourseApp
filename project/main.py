from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import db
from .models import Course
from flask import jsonify

main = Blueprint('main', __name__)


@main.route('/')
def index():
    if(current_user.is_authenticated):
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
    return render_template('courses.html', name=current_user.name)


@main.route('/getCourses', methods=['GET'])
@login_required
def get_courses():
    classes = Course.query.all()

    output = []
    for c in classes:
        course_data = {'courseName': c.course_name, 'prof': c.prof,
                       'time': c.time, 'enrolled': c.enrolled, 'maxEnroll': c.max_enroll}
        output.append(course_data)
    return jsonify(output)

@main.route('/getEnrolled', methods=['GET'])
@login_required
def get_enrolled():
    classes = Course.query.all()

    output = []
    for c in classes:
        course_data = {'courseName': c.course_name, 'prof': c.prof,
                       'time': c.time, 'enrolled': c.enrolled, 'maxEnroll': c.max_enroll}
        output.append(course_data)
    return jsonify(output)
