# routes/gate.py — optional shared-password gate for private previews.
from flask import (Blueprint, render_template, request, redirect, url_for,
                   session, current_app, flash)

gate_bp = Blueprint('gate', __name__)


@gate_bp.route('/gate', methods=['GET', 'POST'])
def gate():
    """A single shared password that unlocks the whole site for this browser."""
    configured = current_app.config.get('SITE_PASSWORD')
    if not configured:
        # Gate not enabled (e.g. local dev) — nothing to unlock.
        return redirect(url_for('courses.home'))

    if request.method == 'POST':
        password = request.form.get('password', '')
        if password and password == configured:
            session['site_unlocked'] = True
            nxt = request.args.get('next', '')
            # Only allow same-site relative redirects.
            if not nxt.startswith('/') or nxt.startswith('//'):
                nxt = url_for('courses.home')
            return redirect(nxt)
        flash('Incorrect password. Please try again.', 'error')

    return render_template('gate.html')
