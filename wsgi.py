"""WSGI entry point for production hosts (PythonAnywhere, gunicorn, etc.).

Local use:
    gunicorn -w 2 -b 0.0.0.0:5001 wsgi:application

PythonAnywhere:
    Point your web app's WSGI configuration file at this module (see DEPLOY.md).
"""
import os
import sys

# Ensure the project root is importable regardless of the caller's cwd.
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import create_app, create_database  # noqa: E402

application = create_app()
create_database(application)  # idempotent: creates tables / seeds courses

if __name__ == '__main__':
    application.run()
