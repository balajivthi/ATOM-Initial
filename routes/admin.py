# routes/admin.py
import os
from functools import wraps
from flask import Blueprint, render_template, request, flash, redirect, url_for, abort, current_app
from flask_login import login_required, current_user
from extensions import db, markdown_converter
from models.models import Course
from utils import slugify, load_course_structure

admin_bp = Blueprint('admin', __name__)

def admin_required(view):
    @wraps(view)
    @login_required
    def wrapped(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return view(*args, **kwargs)
    return wrapped


@admin_bp.route('/admin/courses')
@admin_required
def manage_courses():
    """Admin dashboard listing all courses with actions."""
    courses = Course.query.order_by(Course.title).all()
    return render_template('admin/courses.html', courses=courses)


@admin_bp.route('/admin/courses/new', methods=['GET', 'POST'])
@admin_required
def create_course():
    course = None
    preview = None
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        slug = request.form.get('slug', '').strip() or slugify(title)

        errors = []
        if not title:
            errors.append('Title is required.')
        if not description:
            errors.append('Description is required.')
        if len(title) > 100:
            errors.append('Title must be 100 characters or fewer.')
        if Course.query.filter_by(slug=slug).first():
            errors.append(f'A course with slug "{slug}" already exists.')

        if errors:
            [flash(e) for e in errors]
        else:
            course = Course(title=title, description=description, slug=slug)
            db.session.add(course)
            db.session.commit()
            flash(f'Course "{title}" created.')
            return redirect(url_for('admin.manage_courses'))

    return render_template('admin/course_form.html', course=course, mode='create')


@admin_bp.route('/admin/courses/<int:course_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_course(course_id):
    course = Course.query.get_or_404(course_id)
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        slug = request.form.get('slug', '').strip() or slugify(title)

        errors = []
        if not title:
            errors.append('Title is required.')
        if not description:
            errors.append('Description is required.')
        if len(title) > 100:
            errors.append('Title must be 100 characters or fewer.')
        clash = Course.query.filter(Course.slug == slug, Course.id != course.id).first()
        if clash:
            errors.append(f'A course with slug "{slug}" already exists.')

        if errors:
            [flash(e) for e in errors]
        else:
            course.title = title
            course.description = description
            course.slug = slug
            db.session.commit()
            flash(f'Course "{title}" updated.')
            return redirect(url_for('admin.manage_courses'))

    return render_template('admin/course_form.html', course=course, mode='edit')


@admin_bp.route('/admin/courses/<int:course_id>/delete', methods=['POST'])
@admin_required
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    title = course.title
    db.session.delete(course)
    db.session.commit()
    flash(f'Course "{title}" deleted.')
    return redirect(url_for('admin.manage_courses'))


@admin_bp.route('/admin/courses/seed', methods=['POST'])
@admin_required
def seed_courses():
    """Auto-discover content/ directories and register any missing courses."""
    content_root = os.path.join(current_app.root_path, 'content')
    added = 0
    if os.path.isdir(content_root):
        for folder in sorted(os.listdir(content_root)):
            folder_path = os.path.join(content_root, folder)
            if not os.path.isdir(folder_path) or folder.startswith('.'):
                continue
            slug = slugify(folder)
            if Course.query.filter_by(slug=slug).first():
                continue
            title = ' '.join(folder.replace('-', ' ').split()).title()
            # Count modules to build a friendly description.
            modules = load_course_structure(slug)
            lessons = sum(len(m['lessons']) for m in modules)
            description = f"{len(modules)} module(s), {lessons} lessons."
            db.session.add(Course(title=title, description=description, slug=slug))
            added += 1
    db.session.commit()
    flash(f'Seeded {added} new course(s) from the content directory.' if added else 'No new courses to seed.')
    return redirect(url_for('admin.manage_courses'))