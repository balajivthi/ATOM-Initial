# routes/feedback.py — collect in-app feedback from testers + an admin inbox.
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from extensions import db
from models.models import Feedback
from routes.admin import admin_required

feedback_bp = Blueprint('feedback', __name__)

# value -> label, used by the form and the admin table
CATEGORIES = [
    ('general', 'General'),
    ('bug', 'Bug'),
    ('idea', 'Idea'),
    ('content', 'Content'),
]
CATEGORY_LABELS = dict(CATEGORIES)


@feedback_bp.route('/feedback', methods=['GET', 'POST'])
@login_required
def submit():
    """Let a testers submit feedback and see what they've already sent."""
    if request.method == 'POST':
        category = request.form.get('category', 'general').strip()
        message = request.form.get('message', '').strip()
        page = request.form.get('page', '').strip()[:300]

        if category not in CATEGORY_LABELS:
            category = 'general'

        errors = []
        if not message:
            errors.append('Please write a message.')
        elif len(message) > 4000:
            errors.append('Message must be 4000 characters or fewer.')

        if errors:
            [flash(e) for e in errors]
        else:
            db.session.add(Feedback(user_id=current_user.id, category=category,
                                    message=message, page=page))
            db.session.commit()
            flash('Thanks! Your feedback was recorded.', 'success')
            return redirect(url_for('feedback.submit'))

    mine = (Feedback.query.filter_by(user_id=current_user.id)
            .order_by(Feedback.created_at.desc()).all())
    return render_template('feedback.html', categories=CATEGORIES, mine=mine,
                           category_labels=CATEGORY_LABELS)


@feedback_bp.route('/admin/feedback')
@admin_required
def inbox():
    """Admin view of every piece of feedback, newest first."""
    items = Feedback.query.order_by(Feedback.created_at.desc()).all()
    new_count = sum(1 for i in items if i.status == 'new')
    return render_template('admin/feedback.html', items=items, new_count=new_count,
                           category_labels=CATEGORY_LABELS)


@feedback_bp.route('/admin/feedback/<int:feedback_id>/toggle', methods=['POST'])
@admin_required
def toggle(feedback_id):
    item = Feedback.query.get_or_404(feedback_id)
    item.status = 'new' if item.status == 'read' else 'read'
    db.session.commit()
    return redirect(url_for('feedback.inbox'))


@feedback_bp.route('/admin/feedback/<int:feedback_id>/delete', methods=['POST'])
@admin_required
def delete(feedback_id):
    item = Feedback.query.get_or_404(feedback_id)
    db.session.delete(item)
    db.session.commit()
    flash('Feedback deleted.')
    return redirect(url_for('feedback.inbox'))
