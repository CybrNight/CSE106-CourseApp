from . import db
from flask_login import UserMixin
from enum import Enum
from sqlalchemy import event
from werkzeug.security import generate_password_hash
import uuid

enrollment = db.Table("enrollment",
                      db.Column("user_id", db.Integer,
                                db.ForeignKey('user.id')),
                      db.Column("course_id", db.Integer, db.ForeignKey('course.id')))


class UserRole(Enum):
    STUDENT = "STUDENT"
    PROFESSOR = "PROFESSOR"
    ADMIN = "ADMIN"


class User(UserMixin, db.Model):
    # primary keys are required by SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    user_id = db.Column(db.String, unique=True)
    role = db.Column(db.Enum(UserRole))
    courses = db.relationship(
        'Course', secondary=enrollment, backref="courses")


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100), unique=True)
    prof = db.Column(db.String(100))
    prof_id = db.Column(db.String(100))
    time = db.Column(db.String(100))
    enrolled = db.Column(db.Integer)
    max_enroll = db.Column(db.Integer)


@event.listens_for(User.password, 'set', retval=True)
def hash_user_password(target, value, oldvalue, initiator):
    if value != oldvalue:
        return generate_password_hash(value)
    return value


@event.listens_for(User.user_id, 'set', retval=True)
def set_user_id(target, value, oldvalue, initiator):
    user_id = uuid.uuid4().hex[:8]
    exists = db.session.query(User.user_id).filter_by(
        user_id=user_id).first() is not None

    while exists:
        user_id = uuid.uuid4().hex[:8]
    return user_id
