# routes/courses.py
import os
from flask import Blueprint, render_template, request, current_app
from flask_login import login_required, current_user
from sqlalchemy import or_
from extensions import markdown_converter
from models.models import Course, CourseEnrollment
from utils import load_course_structure, course_progress, display_title, module_quiz_summaries

courses_bp = Blueprint('courses', __name__)

@courses_bp.route('/')
def home():
    query = request.args.get('q', '').strip()
    sort = request.args.get('sort', 'title')

    course_query = Course.query
    if query:
        like = f"%{query}%"
        course_query = course_query.filter(or_(Course.title.ilike(like),
                                               Course.description.ilike(like)))
    if sort == 'newest':
        course_query = course_query.order_by(Course.id.desc())
    else:
        course_query = course_query.order_by(Course.title)

    courses = course_query.all()
    return render_template('home.html', courses=courses, query=query, sort=sort)

@courses_bp.route('/course/<course_slug>')
@login_required
def course_detail(course_slug):
    course = Course.query.filter_by(slug=course_slug).first()
    course_title = course.title if course else course_slug.replace('-', ' ').title()
    modules = load_course_structure(course_slug)

    is_enrolled = (course is not None and
                   CourseEnrollment.query.filter_by(user_id=current_user.id, course_id=course.id).first() is not None)

    done, completed, total, percent = course_progress(current_user.id, course, modules)
    quizzes = module_quiz_summaries(current_user.id, course, modules)
    return render_template('course_detail.html', title=course_title, modules=modules, course_slug=course_slug,
                           course=course, is_enrolled=is_enrolled, completed=completed, total=total, percent=percent,
                           done=done, quizzes=quizzes)

@courses_bp.route('/course/<course_slug>/<module_slug>/<lesson_slug>')
@login_required
def lesson_detail(course_slug, module_slug, lesson_slug):
    # --- Part 1: Load the specific lesson content ---
    lesson_path = os.path.join(current_app.root_path, 'content', course_slug, module_slug, f"{lesson_slug}.md")
    html_content = ""
    if os.path.exists(lesson_path):
        with open(lesson_path, 'r', encoding='utf-8') as f:
            content_md = f.read()
            html_content = markdown_converter.convert(content_md)
    else:
        return "Lesson content not found!", 404

    # --- Part 2: Load the ENTIRE course structure for the sidebar ---
    course = Course.query.filter_by(slug=course_slug).first()
    course_title = course.title if course else course_slug.replace('-', ' ').title()
    modules = load_course_structure(course_slug)

    done, _, _, percent = course_progress(current_user.id, course, modules)
    is_completed = lesson_slug in done
    current_lesson_title = display_title(lesson_slug)
    quizzes = module_quiz_summaries(current_user.id, course, modules)

    return render_template('lesson_detail.html',
                        title=current_lesson_title,
                        content=html_content,
                        course_title=course_title,
                        modules=modules,
                        course_slug=course_slug,
                        current_lesson_slug=lesson_slug,
                        module_slug=module_slug,
                        is_completed=is_completed,
                        done=done,
                        percent=percent,
                        quizzes=quizzes)