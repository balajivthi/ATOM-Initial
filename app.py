from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

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