from flask_admin import Admin, expose
from flask_admin.contrib.sqla import ModelView
from flask import session, render_template, flash, request
from flask_login import current_user
from .models import Role, User, Enrollment, Course
from sqlalchemy.exc import IntegrityError
from project.main import db
import uuid


class AdminView(ModelView):
    column_hide_backrefs = False
    column_list = ('user_id', 'email', 'name', 'role',
                   'enrollment')

    inline_models = (Enrollment,)

    form_excluded_columns = ('user_id')

    form_create_rules = ('email', 'name', 'password', 'role',
                         'enrollment')

    form_edit_rules = ('email', 'name', 'password', 'role',
                       'enrollment')

    form_widget_args = {
        'user_id': {
            "visible": False
        }
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.static_folder = 'static'

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin()

    def inaccessible_callback(self, name, **kwargs):
        if not self.is_accessible():
            return render_template("error/403.html"), 403

    def on_model_change(self, form, model, is_created):
        for e in model.enrollment:
            e.course.set_enroll_count()

        if is_created:
            user_id = uuid.uuid4().hex[:8]
            exists = db.session.query(User.user_id).filter_by(
                user_id=user_id).first() is not None

            while exists:
                user_id = uuid.uuid4().hex[:8]

            model.user_id = user_id

        db.session.commit()


class CourseView(ModelView):
    column_hide_backrefs = False
    column_list = ('course_id', 'name', 'prof_name', 'time', 'enrolled',
                   'max_enroll', 'enrollment')

    inline_models = (Enrollment,)

    form_excluded_columns = ('course_id')

    form_create_rules = ('name', 'prof_name', 'time', 'enrolled',
                         'max_enroll', 'enrollment')
    form_edit_rules = ('name', 'prof_name', 'time', 'enrolled',
                       'max_enroll', 'enrollment')

    form_widget_args = {
        'enrolled': {
            'disabled': True
        },
        'prof_name': {
            'disabled': True
        }
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.static_folder = 'static'

    def on_model_change(self, form, model, is_created):
        if is_created:
            course_id = uuid.uuid4().hex[:8]
            exists = db.session.query(Course.course_id).filter_by(
                course_id=course_id).first() is not None

            while exists:
                course_id = uuid.uuid4().hex[:8]
            print(course_id)
            model.course_id = course_id
        model.update()
        try:
            if model.enrolled > model.max_enroll:
                raise ValueError(f"Class ({model.name}) above capacity")
            return True
        except Exception as e:
            if not self.handle_view_exception(e):
                raise
            db.session.rollback()
            return False

    def after_model_change(self, form, model, is_created):
        model.update()

    def handle_view_exception(self, exc):
        db.session.rollback()
        if isinstance(exc, ValueError):
            flash(f'{str(exc)}', 'error')
            return True
        return False
