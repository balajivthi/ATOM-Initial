# utils.py — shared helpers used across blueprints
import os
import re
from flask import current_app
from extensions import db
from models.models import LessonProgress, QuizAttempt

def slugify(text):
    """Turn arbitrary text into a URL-safe slug."""
    slug = text.lower().strip()
    slug = re.sub(r'[^a-z0-9-]+', '-', slug).strip('-')
    return slug or 'course'

BRAND_WORDS = {
    'servicenow': 'ServiceNow', 'itom': 'ITOM', 'itil': 'ITIL', 'acl': 'ACL',
    'acls': 'ACLs', 'ui': 'UI', 'api': 'API', 'cmdb': 'CMDB', 'sla': 'SLA',
    'chatgpt': 'ChatGPT', 'ai': 'AI', 'rest': 'REST', 'pa': 'Performance Analytics',
    'va': 'Virtual Agent', 'fa': 'Flow Designer', 'sso': 'SSO', 'ldap': 'LDAP',
    'javascript': 'JavaScript', 'gliderecord': 'GlideRecord', 'glidesystem': 'GlideSystem',
    'glideajax': 'GlideAjax', 'glideform': 'glideForm', 'glidedatetime': 'GlideDateTime',
}

def display_title(name):
    """Pretty-print a module/lesson name like 'module-2-ui-navigation' or
    '01-the-servicenow-interface' into a readable title."""
    parts = name.split('-')
    if parts and parts[0].isdigit():
        parts = parts[1:]
    words = []
    for part in parts:
        if not part:
            continue
        key = part.lower()
        words.append(BRAND_WORDS.get(key, part.capitalize()))
    return ' '.join(words)

def load_course_structure(course_slug):
    """Discover modules + lessons from the content/ directory for a course."""
    modules = []
    base_path = os.path.join(current_app.root_path, 'content', course_slug)
    if not os.path.isdir(base_path):
        return modules
    for module_name in sorted(os.listdir(base_path)):
        module_path = os.path.join(base_path, module_name)
        if not os.path.isdir(module_path):
            continue
        lessons = []
        for lesson_file in sorted(os.listdir(module_path)):
            if lesson_file.endswith('.md') and lesson_file.lower() != 'quiz.md':
                lesson_slug = lesson_file.replace('.md', '')
                lessons.append({'title': display_title(lesson_slug), 'slug': lesson_slug})
        has_quiz = os.path.isfile(os.path.join(module_path, 'quiz.md'))
        modules.append({'title': display_title(module_name), 'slug': module_name,
                        'lessons': lessons, 'has_quiz': has_quiz})
    return modules

def load_module_quiz(course_slug, module_slug):
    """Load a module quiz from content/<course>/<module>/quiz.md, or None.

    Quiz file format:
        # Quiz: Title
        1. Question text?
           A. Option A
           B. Option B
           C. Option C
           D. Option D
           CORRECT: B
           EXPLAIN: Reasoning shown after answering.
    """
    quiz_path = os.path.join(current_app.root_path, 'content', course_slug, module_slug, 'quiz.md')
    if not os.path.isfile(quiz_path):
        return None
    with open(quiz_path, 'r', encoding='utf-8') as f:
        text = f.read()

    title = ''
    lines = text.strip().splitlines()
    if lines and lines[0].lstrip().startswith('#'):
        title = lines[0].lstrip('#').strip()

    questions = []
    blocks = re.split(r'(?m)^\s*(\d+)\.\s+', text)
    for i in range(1, len(blocks), 2):
        question = _parse_quiz_question(int(blocks[i]), blocks[i + 1])
        if question:
            questions.append(question)

    return {'title': title or 'Quiz', 'questions': questions}

def _parse_quiz_question(num, body):
    """Parse a single quiz question block into a dict, or None if invalid."""
    lines = [ln.strip() for ln in body.splitlines() if ln.strip()]
    if not lines:
        return None
    question_text = lines[0].strip()
    options = {}
    correct = None
    explain = ''
    explain_open = False
    for ln in lines[1:]:
        opt = re.match(r'^([A-F])\.\s+(.+)$', ln, re.IGNORECASE)
        if opt:
            options[opt.group(1).upper()] = opt.group(2).strip()
            explain_open = False
            continue
        ans = re.match(r'^CORRECT:\s*([A-F])$', ln, re.IGNORECASE)
        if ans:
            correct = ans.group(1).upper()
            explain_open = False
            continue
        exp = re.match(r'^EXPLAIN:\s*(.*)$', ln, re.IGNORECASE)
        if exp:
            explain = exp.group(1).strip()
            explain_open = True
            continue
        if explain_open:
            explain = f'{explain} {ln}'.strip()
    if not options or not correct or correct not in options:
        return None
    return {'id': num, 'text': question_text, 'options': options,
            'correct': correct, 'explain': explain}

def grade_quiz(quiz, answers):
    """Grade submitted answers (dict of qid->letter) against a quiz.

    Returns (results, score) where each result enriches the question with
    the user's chosen letter and a correctness flag.
    """
    score = 0
    results = []
    for q in quiz['questions']:
        chosen = (answers.get(str(q['id'])) or '').strip().upper()
        is_correct = bool(chosen) and chosen == q['correct']
        if is_correct:
            score += 1
        results.append({**q, 'chosen': chosen, 'correct': is_correct})
    return results, score

def course_progress(user_id, course, modules):
    """Compute completed set + percentage for a user within a course."""
    if course is None:
        return set(), 0, 0, 0
    done = {p.lesson_slug for p in LessonProgress.query.filter_by(user_id=user_id, course_id=course.id).all()}
    total = sum(len(m['lessons']) for m in modules)
    completed = sum(1 for m in modules for l in m['lessons'] if l['slug'] in done)
    percent = round((completed / total) * 100) if total else 0
    return done, completed, total, percent

def quiz_summary(user_id, course, module_slug):
    """Best-attempt summary for a module quiz, for curriculum/sidebar display."""
    if course is None:
        return None
    attempt = (QuizAttempt.query.filter_by(user_id=user_id, course_id=course.id,
                                           module_slug=module_slug)
               .order_by(QuizAttempt.score.desc(), QuizAttempt.created_at.asc()).first())
    if not attempt:
        return {'attempted': False, 'score': None, 'percent': None, 'passed': False}
    percent = round((attempt.score / attempt.total) * 100) if attempt.total else 0
    return {'attempted': True, 'score': f'{attempt.score}/{attempt.total}',
            'percent': percent, 'passed': attempt.passed}

def module_quiz_summaries(user_id, course, modules):
    """Map module_slug -> quiz summary for every module that has a quiz."""
    if course is None:
        return {}
    return {m['slug']: quiz_summary(user_id, course, m['slug']) for m in modules if m.get('has_quiz')}