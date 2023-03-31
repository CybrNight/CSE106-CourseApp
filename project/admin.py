from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask import redirect, url_for, render_template, session
from .models import User
from . import db


class AdminView(ModelView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.static_folder = 'static'

    def is_accessible(self):
        return session.get('user') == "Administrator"

    def inaccessible_callback(self, name, **kwargs):
        if not self.is_accessible():
            return render_template("error/403.html"), 403
