from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from project.role import Role

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()


def create_default_accounts():
    from .models import User, Course, Enrollment

    db.session.add(User(role=Role.ADMIN, name="ADMIN",
                        email="admin@me.com", password="123"))
    for i in range(0, 8):
        course = Course(course_name=f"CSE{100+(i*5)}", time="MWF 10:00-10:50AM",
                        enrolled=0, max_enroll=8)
        prof = User(
            name=f"Professor{i}", email=f"prof{i}@me.com", password="123", role=Role.PROFESSOR)
        user = User(
            name=f"Student{i}", email=f"student{i}@me.com", password="123", role=Role.STUDENT)
        db.session.add(course)
        db.session.add(prof)
        db.session.add(user)
        db.session.add(Enrollment(user=user, course=course, grade=90))
        db.session.add(Enrollment(user=prof, course=course, grade=85))
        db.session.commit()


def create_app():
    app = Flask(__name__,  static_url_path="/static", static_folder="static")

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User, Course
    from .admin import AdminView

    admin = Admin(app, name="Dashboard", index_view=AdminView(
        User, db.session, url='/admin', endpoint='admin'))
    admin.add_view(ModelView(Course, db.session))

    @ login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app


def rebuild():
    app = create_app()
    app.app_context().push()
    db.drop_all()
    db.create_all()
    create_default_accounts()
