# routes/profile.py
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models.models import CourseEnrollment, LessonProgress
from utils import load_course_structure, course_progress

profile_bp = Blueprint('profile', __name__)


@profile_bp.route('/profile')
@login_required
def dashboard():
    user = current_user

    enrollments = (CourseEnrollment.query
                   .filter_by(user_id=user.id)
                   .order_by(CourseEnrollment.enrolled_at.desc())
                   .all())

    items = []
    total_completed = 0
    total_lessons = 0
    completed_courses = 0
    for enrollment in enrollments:
        modules = load_course_structure(enrollment.course.slug)
        done, completed, total, percent = course_progress(user.id, enrollment.course, modules)
        total_completed += completed
        total_lessons += total
        if percent == 100:
            completed_courses += 1
        items.append({'course': enrollment.course, 'enrolled_at': enrollment.enrolled_at,
                      'percent': percent, 'completed': completed, 'total': total})

    overall_percent = round((total_completed / total_lessons) * 100) if total_lessons else 0
    lessons_completed = LessonProgress.query.filter_by(user_id=user.id).count()

    stats = {
        'courses': len(enrollments),
        'in_progress': len(enrollments) - completed_courses,
        'completed_courses': completed_courses,
        'lessons_completed': lessons_completed,
        'total_lessons': total_lessons,
        'overall_percent': overall_percent,
    }

    return render_template('profile.html', user=user, items=items, stats=stats)