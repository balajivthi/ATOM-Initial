# routes/enrollments.py
from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from extensions import db
from models.models import Course, CourseEnrollment
from utils import load_course_structure, course_progress

enrollments_bp = Blueprint('enrollments', __name__)

@enrollments_bp.route('/course/<course_slug>/enroll', methods=['POST'])
@login_required
def enroll(course_slug):
    course = Course.query.filter_by(slug=course_slug).first()
    if not course:
        flash('Course not found.')
        return redirect(url_for('courses.home'))
    existing = CourseEnrollment.query.filter_by(user_id=current_user.id, course_id=course.id).first()
    if not existing:
        db.session.add(CourseEnrollment(user_id=current_user.id, course_id=course.id))
        db.session.commit()
        flash(f'Enrolled in "{course.title}". Happy learning!', 'success')
    return redirect(url_for('courses.course_detail', course_slug=course_slug))

@enrollments_bp.route('/course/<course_slug>/unenroll', methods=['POST'])
@login_required
def unenroll(course_slug):
    course = Course.query.filter_by(slug=course_slug).first()
    if course:
        enrollment = CourseEnrollment.query.filter_by(user_id=current_user.id, course_id=course.id).first()
        if enrollment:
            db.session.delete(enrollment)
            db.session.commit()
            flash(f'Unenrolled from "{course.title}".')
    return redirect(url_for('enrollments.my_courses'))

@enrollments_bp.route('/my-courses')
@login_required
def my_courses():
    enrollments = (CourseEnrollment.query
                   .filter_by(user_id=current_user.id)
                   .order_by(CourseEnrollment.enrolled_at.desc())
                   .all())
    items = []
    for enrollment in enrollments:
        modules = load_course_structure(enrollment.course.slug)
        done, completed, total, percent = course_progress(current_user.id, enrollment.course, modules)
        items.append({'enrollment': enrollment, 'percent': percent, 'completed': completed, 'total': total})
    return render_template('my_courses.html', items=items)