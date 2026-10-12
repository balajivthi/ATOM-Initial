from flask_login import UserMixin
from datetime import datetime
from sqlalchemy import UniqueConstraint
from extensions import db # <-- CHANGE IS HERE

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    enrollments = db.relationship('CourseEnrollment', back_populates='user', cascade='all, delete-orphan')
    progress = db.relationship('LessonProgress', back_populates='user', cascade='all, delete-orphan')
    quiz_attempts = db.relationship('QuizAttempt', back_populates='user', cascade='all, delete-orphan')

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    slug = db.Column(db.String(120), unique=True, nullable=False)

    enrollments = db.relationship('CourseEnrollment', back_populates='course', cascade='all, delete-orphan')
    progress = db.relationship('LessonProgress', back_populates='course', cascade='all, delete-orphan')
    quiz_attempts = db.relationship('QuizAttempt', back_populates='course', cascade='all, delete-orphan')

class CourseEnrollment(db.Model):
    __tablename__ = 'course_enrollment'
    __table_args__ = (UniqueConstraint('user_id', 'course_id', name='uq_user_course'),)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship('User', back_populates='enrollments')
    course = db.relationship('Course', back_populates='enrollments')

class LessonProgress(db.Model):
    __tablename__ = 'lesson_progress'
    __table_args__ = (UniqueConstraint('user_id', 'course_id', 'module_slug', 'lesson_slug',
                                       name='uq_user_lesson'),)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    module_slug = db.Column(db.String(200), nullable=False)
    lesson_slug = db.Column(db.String(200), nullable=False)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship('User', back_populates='progress')
    course = db.relationship('Course', back_populates='progress')

class QuizAttempt(db.Model):
    """A single graded attempt at a module quiz."""
    __tablename__ = 'quiz_attempt'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    module_slug = db.Column(db.String(200), nullable=False)
    score = db.Column(db.Integer, nullable=False, default=0)
    total = db.Column(db.Integer, nullable=False, default=0)
    passed = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship('User', back_populates='quiz_attempts')
    course = db.relationship('Course', back_populates='quiz_attempts')

class Feedback(db.Model):
    """A single piece of feedback submitted by a tester."""
    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    category = db.Column(db.String(30), nullable=False, default='general')
    message = db.Column(db.Text, nullable=False)
    page = db.Column(db.String(300))          # where the tester was when they wrote it
    status = db.Column(db.String(20), nullable=False, default='new')  # new | read
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship('User', backref='feedback')