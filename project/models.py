from . import db
from flask_login import UserMixin
from sqlalchemy import event
from werkzeug.security import generate_password_hash
import uuid
from .role import Role

'''enrollment = db.Table("enrollment",
                      db.Column("user_id", db.Integer,
                                db.ForeignKey('user.id')),
                      db.Column("course_id", db.Integer,
                                db.ForeignKey('course.id')),
                      db.Column('course_grade', db.ForeignKey('course_grade.id')))'''


class Enrollment(db.Model):
    __tablename__ = "enrollment"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey(
        "course.id"), nullable=False)

    __table_args__ = (db.UniqueConstraint(user_id, course_id),)

    user = db.relationship("User", back_populates="enrollment")
    course = db.relationship(
        "Course", back_populates="enrollment")
    grade = db.Column(db.Integer)


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

    def add_course(self, course):
        db.session.add(Enrollment(user=self, course=course, grade=100))
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
    enrollment = db.relationship(
        "Enrollment", back_populates="course", lazy="joined")

    def __repr__(self):
        return self.course_name


@ event.listens_for(User.password, 'set', retval=True)
def hash_user_password(target, value, oldvalue, initiator):
    if value != oldvalue:
        return generate_password_hash(value, method="sha256")
    return value


@ event.listens_for(User.user_id, 'set', retval=True)
def set_user_id(target, value, oldvalue, initiator):
    user_id = uuid.uuid4().hex[:8]
    exists = db.session.query(User.user_id).filter_by(
        user_id=user_id).first() is not None

    while exists:
        user_id = uuid.uuid4().hex[:8]
    return user_id
