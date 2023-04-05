from . import db
from flask_login import UserMixin


enrollment = db.Table("enrollment",
                      db.Column("user_id", db.Integer,
                                db.ForeignKey('user.id')),
                      db.Column("course_id", db.Integer, db.ForeignKey('course.id')))


class User(UserMixin, db.Model):
    # primary keys are required by SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    courses = db.relationship(
        'Course', secondary=enrollment, backref="courses")


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100), unique=True)
    prof = db.Column(db.String(100))
    time = db.Column(db.String(100))
    enrolled = db.Column(db.Integer)
    max_enroll = db.Column(db.Integer)
