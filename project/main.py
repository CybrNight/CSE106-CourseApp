from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import db

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.app_errorhandler(404)
def page_not_found(e):
    print(e)
    return render_template('404.html'), 404


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)
