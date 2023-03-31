from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import db

main = Blueprint('main', __name__)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    courseName = db.Column(db.String(100))
    prof = db.Column(db.String(100))
    time = db.Column(db.String(100))
    enrolled = db.Column(db.Integer)
    maxEnroll = db.Column(db.Integer)

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

@main.route('/coursetest' , methods=['GET'])
def get_grades():
    classes = Course.query.all()
    output = []
    for c in classes:
        course_data = {'courseName': c.courseName, 'prof': c.prof, 'time': c.time, 'enrolled': c.enrolled, 'maxEnroll': c.maxEnroll}
        output.append(course_data)
    return output
