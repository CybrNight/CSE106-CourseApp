from . import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    # primary keys are required by SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prof = db.Column(db.String(100))
    time = db.Column(db.String(100))
    enrolled = db.Column(db.Integer)
    maxEnroll = db.Column(db.Integer)
