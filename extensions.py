# extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from markdown import Markdown # <-- Add this import

# Initialize extensions here
db = SQLAlchemy()
login_manager = LoginManager()
markdown_converter = Markdown() # <-- Create an instance