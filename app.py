import os
import markdown
import yaml
from flask import Flask, render_template, request, flash, redirect, url_for # type: ignore
from werkzeug.security import generate_password_hash, check_password_hash # type: ignore
from flask_login import login_user, logout_user, login_required, current_user # type: ignore
from extensions import db, login_manager, markdown_converter # <-- Add markdown_converter here

# Import extensions and models
from extensions import db, login_manager
from models.models import User, Course

def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'a-strong-and-unique-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///learning_portal.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions with the app instance
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    # Define the user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # --- ROUTES ---
    @app.route('/')
    def home():
        courses = Course.query.all()
        return render_template('home.html', courses=courses)

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            user = User.query.filter_by(username=username).first()
            if user:
                flash('Username already exists.')
                return redirect(url_for('register'))
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('home'))
        return render_template('register.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            user = User.query.filter_by(username=username).first()
            if not user or not check_password_hash(user.password, password):
                flash('Please check your login details and try again.')
                return redirect(url_for('login'))
            login_user(user, remember=True)
            return redirect(url_for('home'))
        return render_template('login.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('home'))
    
    @app.route('/course/<course_slug>')
    @login_required
    def course_detail(course_slug):
        course_title = course_slug.replace('-', ' ').title()
        modules = []
        base_path = os.path.join(app.root_path, 'content', course_slug)

        if os.path.exists(base_path):
            for module_name in sorted(os.listdir(base_path)):
                module_path = os.path.join(base_path, module_name)
                if os.path.isdir(module_path):
                    lessons = []
                    for lesson_file in sorted(os.listdir(module_path)):
                        if lesson_file.endswith('.md'):
                            lesson_slug = lesson_file.replace('.md', '')
                            # Correct title slicing for lessons
                            lesson_title = ' '.join(lesson_slug.split('-')[1:]).title()
                            lessons.append({'title': lesson_title, 'slug': lesson_slug})
                
                    # Correct title slicing for modules
                    module_title = ' '.join(module_name.split('-')[1:]).title()
                    modules.append({'title': module_title, 'lessons': lessons, 'slug': module_name})
        return render_template('course_detail.html', title=course_title, modules=modules, course_slug=course_slug)

    @app.route('/course/<course_slug>/<module_slug>/<lesson_slug>')
    @login_required
    def lesson_detail(course_slug, module_slug, lesson_slug):
        # --- Part 1: Load the specific lesson content ---
        lesson_path = os.path.join(app.root_path, 'content', course_slug, module_slug, f"{lesson_slug}.md")
        html_content = ""
        if os.path.exists(lesson_path):
            with open(lesson_path, 'r', encoding='utf-8') as f:
                content_md = f.read()
                # This uses the markdown_converter instance from extensions.py
                html_content = markdown_converter.convert(content_md)
        else:
            return "Lesson content not found!", 404

        # --- Part 2: Load the ENTIRE course structure for the sidebar ---
        course_title = course_slug.replace('-', ' ').title()
        modules = []
        base_path = os.path.join(app.root_path, 'content', course_slug)
        if os.path.exists(base_path):
            for module_item_name in sorted(os.listdir(base_path)):
                module_path = os.path.join(base_path, module_item_name)
                if os.path.isdir(module_path):
                    lessons = []
                    for lesson_file in sorted(os.listdir(module_path)):
                        if lesson_file.endswith('.md'):
                            current_lesson_slug = lesson_file.replace('.md', '')
                            lesson_title = ' '.join(current_lesson_slug.split('-')[1:]).title()
                            lessons.append({'title': lesson_title, 'slug': current_lesson_slug})

                    module_title = ' '.join(module_item_name.split('-')[1:]).title()
                    modules.append({'title': module_title, 'lessons': lessons, 'slug': module_item_name})

        current_lesson_title = ' '.join(lesson_slug.split('-')[1:]).title()

        return render_template('lesson_detail.html',
                            title=current_lesson_title,
                            content=html_content,
                            course_title=course_title,
                            modules=modules,
                            course_slug=course_slug,
                            current_lesson_slug=lesson_slug)
    return app

def create_database(app):
    with app.app_context():
        db.create_all()
        if not Course.query.first():
            course1 = Course(title='Introduction to Python', description='Learn the basics of Python programming.')
            course2 = Course(title='Web Development with Flask', description='Build your first web application with Flask.')
            course3 = Course(title='Understanding Databases with SQLAlchemy', description='Master data management in your apps.')
            db.session.add_all([course1, course2, course3])
            db.session.commit()
            print("Database created and sample courses added.")