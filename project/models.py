from . import db
from flask_login import UserMixin
from enum import Enum
from sqlalchemy import event
from werkzeug.security import generate_password_hash
import uuid
from .role import Role

enrollment = db.Table("enrollment",
                      db.Column("user_id", db.Integer,
                                db.ForeignKey('user.id')),
                      db.Column("course_id", db.Integer, db.ForeignKey('course.id')))


class User(UserMixin, db.Model):
    # primary keys are required by SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    user_id = db.Column(db.String, unique=True)
    role = db.Column(db.Enum(Role))
    courses = db.relationship(
        'Course', secondary=enrollment, backref=db.backref('users', lazy='dynamic'))

    def add_course(self, course):
        self.courses.append(course)
        course.enrolled += 1
        db.session.commit()

    def is_admin(self):
        return self.role == Role.ADMIN

    def __repr__(self):
        return self.name


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100), unique=True)
    time = db.Column(db.String(100))
    enrolled = db.Column(db.Integer)
    max_enroll = db.Column(db.Integer)

    def __repr__(self):
        return self.course_name


@event.listens_for(User.password, 'set', retval=True)
def hash_user_password(target, value, oldvalue, initiator):
    if value != oldvalue:
        return generate_password_hash(value, method="sha256")
    return value


@event.listens_for(User.user_id, 'set', retval=True)
def set_user_id(target, value, oldvalue, initiator):
    user_id = uuid.uuid4().hex[:8]
    exists = db.session.query(User.user_id).filter_by(
        user_id=user_id).first() is not None

    while exists:
        user_id = uuid.uuid4().hex[:8]
    return user_id
