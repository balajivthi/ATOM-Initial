# routes/progress.py
from flask import Blueprint, redirect, url_for
from flask_login import login_required, current_user
from extensions import db
from models.models import Course, LessonProgress

progress_bp = Blueprint('progress', __name__)

@progress_bp.route('/course/<course_slug>/<module_slug>/<lesson_slug>/complete', methods=['POST'])
@login_required
def complete_lesson(course_slug, module_slug, lesson_slug):
    course = Course.query.filter_by(slug=course_slug).first()
    if not course:
        return "Course not found!", 404
    existing = LessonProgress.query.filter_by(
        user_id=current_user.id, course_id=course.id,
        module_slug=module_slug, lesson_slug=lesson_slug).first()
    if not existing:
        db.session.add(LessonProgress(user_id=current_user.id, course_id=course.id,
                                      module_slug=module_slug, lesson_slug=lesson_slug))
        db.session.commit()
    return redirect(url_for('courses.lesson_detail', course_slug=course_slug,
                            module_slug=module_slug, lesson_slug=lesson_slug))

@progress_bp.route('/course/<course_slug>/<module_slug>/<lesson_slug>/reset', methods=['POST'])
@login_required
def reset_lesson(course_slug, module_slug, lesson_slug):
    course = Course.query.filter_by(slug=course_slug).first()
    if course:
        progress = LessonProgress.query.filter_by(
            user_id=current_user.id, course_id=course.id,
            module_slug=module_slug, lesson_slug=lesson_slug).first()
        if progress:
            db.session.delete(progress)
            db.session.commit()
    return redirect(url_for('courses.lesson_detail', course_slug=course_slug,
                            module_slug=module_slug, lesson_slug=lesson_slug))