from . import db
from flask_login import UserMixin
from enum import Enum
from sqlalchemy import event
from werkzeug.security import generate_password_hash
import uuid
from .role import Role


class Enrollment(db.Model):
    __tablename__ = "enrollment"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        "user.user_id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        "user.user_id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey(
        "course.id"), nullable=False)

    __table_args__ = (db.UniqueConstraint(user_id, course_id),)

    user = db.relationship("User", back_populates="enrollment")
    course = db.relationship(
        "Course", back_populates="enrollment")
    grade = db.Column(db.Integer)

    def __repr__(self):
        return self.course.name + " " + self.user.name
        return self.course.name + " " + self.user.name


class User(UserMixin, db.Model):
    # primary keys are required by SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    user_id = db.Column(db.String, unique=True)
    role = db.Column(db.Enum(Role))
    enrollment = db.relationship(
        "Enrollment", back_populates="user", lazy="joined")

    def is_admin(self):
        return self.role == Role.ADMIN

    def __repr__(self):
        return self.name


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    time = db.Column(db.String(100))
    enrolled = db.Column(db.Integer)
    max_enroll = db.Column(db.Integer)

    def __repr__(self):
        return self.name

    def set_enroll_count(self):
        enrollment = Enrollment.query.join(Course).join(User).filter(
            (User.role == Role.STUDENT) & (Course.name == self.name)).all()
        self.enrolled = len(enrollment)
        return self.enrolled

    def add_user(self, user):
        if self.enrolled < self.max_enroll:
            db.session.add(Enrollment(user=user, course=self, grade=100))
            self.set_enroll_count()
            db.session.commit()

    def remove_user(self, user):
        Enrollment.query.filter_by(course=self, user=user).delete()
        self.set_enroll_count()
        db.session.commit()
        return self.name

    def set_enroll_count(self):
        enrollment = Enrollment.query.join(Course).join(User).filter(
            (User.role == Role.STUDENT) & (Course.name == self.name)).all()
        self.enrolled = len(enrollment)
        return self.enrolled

    def add_user(self, user):
        if self.enrolled < self.max_enroll:
            db.session.add(Enrollment(user=user, course=self, grade=100))
            self.set_enroll_count()
            db.session.commit()

    def remove_user(self, user):
        Enrollment.query.filter_by(course=self, user=user).delete()
        self.set_enroll_count()
        db.session.commit()


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
