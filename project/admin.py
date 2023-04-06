from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask import redirect, url_for, render_template, session
from flask_login import current_user
from .models import Role
from . import db


class AdminView(ModelView):
    column_hide_backrefs = False
    column_list = ('email', 'courses', 'role', 'user_id')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.static_folder = 'static'

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == Role.ADMIN

    def inaccessible_callback(self, name, **kwargs):
        if not self.is_accessible():
            return render_template("error/403.html"), 403
