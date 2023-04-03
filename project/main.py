from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from . import db
from .models import Course
import json

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


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


@main.route('/coursetest')
@login_required
def yourgrades():
    return render_template('yourcourse.html', name=current_user.name)


@main.route('/getcourses', methods=['GET'])
@login_required
def get_grades():
    classes = Course.query.all()

    classList = []
    for c in classes:
        classJson = {'courseName': c.course_name, 'prof': c.prof,
                     'time': c.time, 'enrolled': c.enrolled, 'maxEnroll': c.max_enroll}
        classList.append(classJson)
    return jsonify(classList)
