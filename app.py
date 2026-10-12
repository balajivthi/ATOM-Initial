import os
import re
from flask import Flask, render_template, request, session, redirect, url_for
from flask_login import current_user
from dotenv import load_dotenv
from extensions import db, login_manager
from models.models import User, Course
from routes.auth import auth_bp
from routes.courses import courses_bp
from routes.enrollments import enrollments_bp
from routes.progress import progress_bp
from routes.quizzes import quizzes_bp
from routes.admin import admin_bp
from routes.profile import profile_bp
from routes.gate import gate_bp
from routes.feedback import feedback_bp
from utils import slugify, load_course_structure

def create_app():
    """Create and configure an instance of the Flask application."""
    load_dotenv()

    secret_key = os.environ.get('SECRET_KEY')
    if not secret_key:
        secret_key = 'a-strong-and-unique-secret-key'
        print("WARNING: SECRET_KEY not set — using an insecure default. Set SECRET_KEY in a .env file or environment.")

    app = Flask(__name__)
    app.config['SECRET_KEY'] = secret_key
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///learning_portal.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['PORT'] = int(os.environ.get('PORT', 5000))
    app.config['HOST'] = os.environ.get('HOST', '0.0.0.0')

    # Optional shared-password gate. When set, every page (except the gate and
    # static assets) requires this password once per browser session.
    app.config['SITE_PASSWORD'] = os.environ.get('SITE_PASSWORD', '')

    # Initialize extensions with the app instance
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Define the user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprint routes
    app.register_blueprint(courses_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(enrollments_bp)
    app.register_blueprint(progress_bp)
    app.register_blueprint(quizzes_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(gate_bp)
    app.register_blueprint(feedback_bp)

    # --- Optional shared-password gate -------------------------------------
    # If SITE_PASSWORD is set, block everything until the visitor unlocks it.
    @app.before_request
    def require_site_password():
        configured = app.config.get('SITE_PASSWORD')
        if not configured:
            return None
        # Always allow static assets, the gate itself, and Flask-Login internals.
        if request.endpoint in ('static', 'gate.gate'):
            return None
        if request.path.startswith('/static/'):
            return None
        if session.get('site_unlocked'):
            return None
        return redirect(url_for('gate.gate', next=request.path))

    # Make current_user available in every template context
    @app.context_processor
    def inject_user():
        return {'current_user': current_user}

    # --- Error handlers ---
    @app.errorhandler(403)
    def forbidden(e):
        return render_template('error.html', code=403,
                               message="You don't have permission to access this page."), 403

    @app.errorhandler(404)
    def not_found(e):
        return render_template('error.html', code=404,
                               message="Sorry, the page you're looking for doesn't exist."), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template('error.html', code=500,
                               message="Something went wrong on our end. Please try again later."), 500

    return app

def create_database(app):
    with app.app_context():
        db.create_all()

        inspector = db.inspect(db.engine)
        course_cols = [c['name'] for c in inspector.get_columns('course')]

        # --- Lightweight migration: add Course.slug if missing ---
        if 'slug' not in course_cols:
            db.session.execute(db.text("ALTER TABLE course ADD COLUMN slug VARCHAR(120)"))
            db.session.commit()
            print("Added 'slug' column to course table.")

        # --- Lightweight migration: add User.is_admin + User.created_at if missing ---
        user_cols = [c['name'] for c in inspector.get_columns('user')]
        if 'is_admin' not in user_cols:
            db.session.execute(db.text("ALTER TABLE user ADD COLUMN is_admin BOOLEAN DEFAULT 0 NOT NULL"))
            print("Added 'is_admin' column to user table.")
        if 'created_at' not in user_cols:
            db.session.execute(db.text("ALTER TABLE user ADD COLUMN created_at DATETIME"))
            print("Added 'created_at' column to user table.")
        db.session.commit()

        # Backfill created_at for any users still missing it.
        from datetime import datetime
        for user in User.query.filter(User.created_at.is_(None)).all():
            user.created_at = datetime.utcnow()
            db.session.add(user)
        db.session.commit()

        # --- Admin bootstrapping: promote users named in ADMIN_USERNAMES (or the first user) ---
        admin_names = [n.strip() for n in os.environ.get('ADMIN_USERNAMES', '').split(',') if n.strip()]
        if not admin_names and not User.query.filter_by(is_admin=True).first():
            first = User.query.order_by(User.id).first()
            if first:
                admin_names = [first.username]
        if admin_names:
            for name in admin_names:
                user = User.query.filter_by(username=name).first()
                if user and not user.is_admin:
                    user.is_admin = True
                    db.session.add(user)
                    print(f"Promoted '{name}' to admin.")
            db.session.commit()

        # Backfill slugs for any courses still missing one.
        for course in Course.query.filter(Course.slug.is_(None)).all():
            course.slug = slugify(course.title)
            db.session.add(course)
        db.session.commit()

        # Auto-seed missing courses from the content/ directory (idempotent).
        KNOWN_COURSES = {
            'servicenow-basics': {
                'title': 'Introduction to ServiceNow',
                'description': ('Your first day at GlidePort Logistics. Understand the platform, set up users, '
                                'build the Delivery App, import agent data, send notifications, and launch '
                                'self-service with the catalog and Virtual Agent.'),
            },
            'make-the-platform-think': {
                'title': 'Make the Platform Think',
                'description': ('Give the GlidePort Delivery App some brains. Learn JavaScript on the platform, '
                                'read and write delivery records with GlideRecord, automate order processing '
                                'with Business Rules, then make the browser and the catalog react with Client '
                                'Scripts.'),
            },
            'build-your-own-api': {
                'title': 'Build Your Own API',
                'description': ('Open the GlidePort Delivery App to other systems. Package reusable logic in '
                                'Script Includes, answer live questions from the browser with the AJAX pattern, '
                                'and expose delivery data through your own secured Scripted REST endpoints.'),
            },
            'automate-the-delivery-line': {
                'title': 'Automate the Delivery Line',
                'description': ("Stop hand-holding the delivery journey. Build visual, logged automations that "
                                "react to records and the clock, fork and loop, wait for real-world events, reuse "
                                "subflows and custom actions, and fail gracefully — so the whole delivery line runs "
                                "itself from order to doorstep."),
            },
            'open-the-loading-dock': {
                'title': 'Open the Loading Dock',
                'description': ("Connect the Delivery App to the outside world. Call partner systems with secure "
                                "outbound requests, prove GlidePort's identity with credentials and OAuth, receive "
                                "real-time events and batch manifests, reuse prebuilt integration blocks, and watch "
                                "every wire so nothing fails silently."),
            },
        }
        content_root = os.path.join(app.root_path, 'content')
        if os.path.isdir(content_root):
            for folder in sorted(os.listdir(content_root)):
                folder_path = os.path.join(content_root, folder)
                if not os.path.isdir(folder_path) or folder.startswith('.'):
                    continue
                slug = slugify(folder)
                existing = Course.query.filter_by(slug=slug).first()
                if existing:
                    # One-time refresh: update known courses that still carry a legacy default description.
                    info = KNOWN_COURSES.get(slug)
                    legacy = 'Learn the ServiceNow platform from the ground up: navigation, forms, and more.'
                    if info and existing.description == legacy:
                        existing.description = info['description']
                        db.session.add(existing)
                    continue
                info = KNOWN_COURSES.get(slug)
                if info:
                    db.session.add(Course(title=info['title'], description=info['description'], slug=slug))
                else:
                    title = ' '.join(folder.replace('-', ' ').split()).title()
                    modules = load_course_structure(slug)
                    lessons = sum(len(m['lessons']) for m in modules)
                    db.session.add(Course(title=title,
                                          description=f"{len(modules)} module(s), {lessons} lessons.", slug=slug))
            db.session.commit()

        # Sanitize any invalid slugs left over from earlier seeds.
        for course in Course.query.all():
            cleaned = slugify(course.slug)
            if cleaned != course.slug:
                course.slug = cleaned
                db.session.add(course)
        db.session.commit()