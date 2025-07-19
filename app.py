from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///learning_portal.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)

@app.route('/')
def home():
    return 'Welcome to the Learning Portal! This is the home page.'

if __name__ == '__main__':
    app.run(debug=True)
