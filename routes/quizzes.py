# routes/quizzes.py
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from extensions import db
from models.models import Course, QuizAttempt
from utils import load_module_quiz, grade_quiz, display_title, quiz_summary

quizzes_bp = Blueprint('quizzes', __name__)

PASS_PERCENT = 60


@quizzes_bp.route('/course/<course_slug>/<module_slug>/quiz', methods=['GET'])
@login_required
def quiz_page(course_slug, module_slug):
    course = Course.query.filter_by(slug=course_slug).first()
    course_title = course.title if course else course_slug.replace('-', ' ').title()
    quiz = load_module_quiz(course_slug, module_slug)
    if not quiz or not quiz['questions']:
        return render_template('error.html', code=404,
                               message="No quiz found for this module."), 404
    meta = quiz_summary(current_user.id, course, module_slug)
    return render_template('quiz.html', title=quiz['title'], quiz=quiz,
                           module_title=display_title(module_slug), module_slug=module_slug,
                           course_slug=course_slug, course_title=course_title,
                           course=course, meta=meta, pass_percent=PASS_PERCENT)


@quizzes_bp.route('/course/<course_slug>/<module_slug>/quiz', methods=['POST'])
@login_required
def quiz_submit(course_slug, module_slug):
    course = Course.query.filter_by(slug=course_slug).first()
    if not course:
        return "Course not found!", 404
    course_title = course.title if course else course_slug.replace('-', ' ').title()
    quiz = load_module_quiz(course_slug, module_slug)
    if not quiz or not quiz['questions']:
        return render_template('error.html', code=404,
                               message="No quiz found for this module."), 404

    answers = {str(q['id']): (request.form.get(f'answer_{q["id"]}') or '')
               for q in quiz['questions']}
    results, score = grade_quiz(quiz, answers)
    total = len(results)
    percent = round((score / total) * 100) if total else 0
    passed = percent >= PASS_PERCENT

    attempt = QuizAttempt(user_id=current_user.id, course_id=course.id,
                          module_slug=module_slug, score=score, total=total, passed=passed)
    db.session.add(attempt)
    db.session.commit()

    return render_template('quiz_result.html', title=quiz['title'], quiz=quiz,
                           results=results, score=score, total=total, percent=percent,
                           passed=passed, pass_percent=PASS_PERCENT,
                           module_title=display_title(module_slug), module_slug=module_slug,
                           course_slug=course_slug, course_title=course_title,
                           course=course, meta=quiz_summary(current_user.id, course, module_slug))
