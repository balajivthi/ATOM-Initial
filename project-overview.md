# ATOM Project Overview

## Project Purpose
A Python-based **public learning portal** for user registration, course browsing, enrollment, and progress tracking. Built with Flask and SQLite.

---

## Tech Stack
- **Backend Framework**: Flask
- **Database**: SQLite (learning_portal.db)
- **Authentication**: Flask-Login + werkzeug (password hashing: pbkdf2:sha256)
- **Templating**: Jinja2 (HTML templates)
- **Markdown Processing**: Markdown library (for converting .md content to HTML)
- **Server**: Waitress (production-ready WSGI server)

---

## Architecture Overview

### Application Structure
```
app.py               # Main entry point (app factory + blueprint registration + error handlers)
extensions.py       # Centralized Flask extensions (db, login_manager, markdown_converter)
models/models.py    # Database models (User, Course, CourseEnrollment, LessonProgress, QuizAttempt, Feedback)
utils.py            # Shared helpers (slugify, load_course_structure, course_progress)
routes/             # Blueprint route files (auth, courses, enrollments, progress, quizzes, admin, profile, gate, feedback)
wsgi.py             # Production WSGI entry point (Waitress / gunicorn / PythonAnywhere)
serve.py            # Waitress production server (reads HOST/PORT)
start-local.sh      # Start app + Cloudflare quick tunnel, then print the public URL
stop-local.sh       # Stop the app + tunnel
DEPLOY.md           # Deployment guide (tunnel / PythonAnywhere / Render) + security checklist
requirements.txt    # Python dependencies
content/            # Markdown course content (course/module/lesson) + shared _lab-setup.md
templates/          # HTML templates (Jinja2)
static/             # CSS (main.css), JS, images
```

### Key Components

#### Database Models (models/models.py)
- **User**: UserMixin + db.Model
  - id (primary key)
  - username (unique)
  - password (hashed)
  - is_admin (boolean, used to gate admin/management UI)
  - created_at (datetime, member-since)
  - enrollments (relationship to CourseEnrollment)
  - progress (relationship to LessonProgress)
  - quiz_attempts (relationship to QuizAttempt)

- **Course**: db.Model
  - id (primary key)
  - title
  - description
  - slug (unique) — maps to content/ directory

- **CourseEnrollment**: db.Model
  - id (primary key)
  - user_id (FK -> user.id)
  - course_id (FK -> course.id)
  - enrolled_at (datetime, default now)
  - Unique constraint on (user_id, course_id) — no duplicate enrollments

- **LessonProgress**: db.Model
  - id (primary key)
  - user_id (FK -> user.id)
  - course_id (FK -> course.id)
  - module_slug (String)
  - lesson_slug (String)
  - completed_at (datetime, default now)
  - Unique constraint on (user_id, course_id, module_slug, lesson_slug)

- **QuizAttempt**: db.Model
  - id (primary key)
  - user_id (FK -> user.id)
  - course_id (FK -> course.id)
  - module_slug (String)
  - score / total (Integer)
  - passed (Boolean; pass mark 60%)
  - created_at (datetime, default now)

- **Feedback**: db.Model
  - id (primary key)
  - user_id (FK -> user.id, nullable)
  - category (String: general | bug | idea | content)
  - message (Text)
  - page (String; where the tester was when they wrote it)
  - status (String: new | read)
  - created_at (datetime, default now)

#### Flask Extensions (extensions.py)
- `db`: SQLAlchemy ORM instance
- `login_manager`: Flask-Login manager (user authentication)
- `markdown_converter`: Markdown processor (converts .md to HTML)

---

## Current Features & Routes

Routes are modularized into Flask blueprints under `routes/`:

- **routes/auth.py** (`auth`)
  - **GET/POST /register**: User registration with duplicate username check
  - **GET/POST /login**: Login with username/password + "remember me" option
  - **GET /logout**: Logout (requires login)
- **routes/courses.py** (`courses`)
  - **GET /**: Home page - displays all courses, with search (`?q=`) by title/description and sorting (`?sort=title|newest`)
  - **GET /lab-setup**: Shared, login-free reference page (renders `content/_lab-setup.md`) — PDI signup + the public sandbox endpoints every integration lab uses; linked from the top nav and a banner on every course page
  - **GET /course/<course_slug>**: Course detail page with modules & lessons, enroll/unenroll state, and per-user progress bar (requires login)
  - **GET /course/<course_slug>/<module_slug>/<lesson_slug>**: Individual lesson detail + content rendering + completion state (requires login)
- **routes/enrollments.py** (`enrollments`)
  - **POST /course/<course_slug>/enroll**: Enroll the user in a course (idempotent; requires login)
  - **POST /course/<course_slug>/unenroll**: Remove the user's enrollment (requires login)
  - **GET /my-courses**: Enrolled courses with progress %, continue/unenroll actions (requires login)
- **routes/progress.py** (`progress`)
  - **POST /course/<course_slug>/<module_slug>/<lesson_slug>/complete**: Mark a lesson complete (idempotent; requires login)
  - **POST /course/<course_slug>/<module_slug>/<lesson_slug>/reset**: Mark a lesson incomplete (requires login)
- **routes/admin.py** (`admin`) — all routes require login + `is_admin`
  - **GET /admin/courses**: Course management list (table with view/edit/delete)
  - **GET/POST /admin/courses/new**: Create course (title/description/slug + validation)
  - **GET/POST /admin/courses/<id>/edit**: Edit course
  - **POST /admin/courses/<id>/delete**: Delete course (cascades enrollments + progress)
  - **POST /admin/courses/seed**: Auto-register missing courses from `content/`
- **routes/profile.py** (`profile`)
  - **GET /profile**: User dashboard — avatar, member-since, admin badge, stat cards (courses / in progress / completed / lessons), overall progress bar, per-course progress with Continue/Review CTA
- **routes/quizzes.py** (`quizzes`)
  - **GET/POST /course/<course_slug>/<module_slug>/quiz**: Module quiz — renders questions, grades on submit, reveals answers + reasoning (pass mark 60%)
- **routes/gate.py** (`gate`)
  - **GET/POST /gate**: Optional shared-password gate (active only when `SITE_PASSWORD` is set)
- **routes/feedback.py** (`feedback`)
  - **GET/POST /feedback**: Tester feedback submission + their own history (requires login)
  - **GET /admin/feedback**: Admin inbox (read/unread toggle + delete)
  - **POST /admin/feedback/<id>/toggle**, **POST /admin/feedback/<id>/delete**

### Error Handlers (app.py)
- **403 / 404 / 500**: Styled error pages via `templates/error.html`

### Shared Helpers (utils.py)
- `slugify()` — URL-safe slug generation
- `display_title()` — brand-correct title casing (ServiceNow, UI, ACL, ChatGPT, …)
- `load_course_structure()` — discovers modules/lessons from `content/` filesystem
- `course_progress()` — computes a user's completed set + completion percentage
- `load_module_quiz()` / `grade_quiz()` — parse and grade a module's `quiz.md`
- `quiz_summary()` / `module_quiz_summaries()` — best-score summaries for quizzes

### Route Logic Details
- Course browsing loads courses from database + filesystem
- Modules/lessons are auto-discovered from `content/` directory structure (shared via `load_course_structure()`)
- Markdown files are converted to HTML for display
- Login required for all course content pages
- Course.slug (added via auto-migration) ties DB records to the content directory
- Enrollment is idempotent (unique user+course) and reflected in course detail badge + My Courses page
- Progress is tracked per lesson (`LessonProgress`), computed as % via `course_progress()`, and shown as bars on course detail, lesson sidebar, and My Courses

---

## Content Organization

### Directory Structure
```
content/
├── servicenow-basics/                        # Introduction to ServiceNow (10 modules / 18 lessons)
│   ├── module-1-introduction/                # What is ServiceNow? · How the Platform Functions
│   ├── module-2-ui-navigation/               # The ServiceNow Interface
│   ├── module-3-lists-and-forms/             # Working with Lists · Working with Forms
│   ├── module-4-users-groups-and-roles/      # Creating Users · Creating Groups and Roles
│   ├── module-5-tables-and-access-control/   # Working with Tables · Introduction to ACLs
│   ├── module-6-data-imports-and-transform-maps/  # Data Sources & Import Sets · Transform Maps
│   ├── module-7-scheduling-and-update-sets/  # Scheduling Data Imports · Working with Update Sets
│   ├── module-8-email-notifications/         # Configuring Email Notifications
│   ├── module-9-service-catalog-and-record-producers/  # Service Catalog · Record Producers
│   └── module-10-virtual-agent-and-ai/       # Virtual Agent · Integrating ChatGPT
├── make-the-platform-think/                  # Make the Platform Think (5 modules / 15 lessons) — formerly servicenow-scripting
│   ├── module-1-the-language-of-the-platform/  # Scripting 101 · Backstage Pass · The Platform Toolbox
│   ├── module-2-talk-to-the-database/          # Ask the Database · Find the Needle · Make It Remember
│   ├── module-3-rules-of-the-game/             # When the Platform Reacts · Your First Automaton · Rules That Think
│   ├── module-4-scripts-in-the-browser/        # Meet the Client Script · Your First Client Script · Client Script Patterns
│   └── module-5-self-service-catalog/          # Build a Catalog Item · Catalog Client Scripts · Catalog Client Script Lab
└── build-your-own-api/                       # Build Your Own API (2 modules / 6 lessons)
    ├── module-1-script-includes-and-ajax/    # Script Includes Unplugged · The AJAX Pattern · The AJAX Lab
    └── module-2-scripted-rest-endpoints/     # REST in 15 Minutes · Your First Endpoint · Lock It Down and Test
├── automate-the-delivery-line/               # Automate the Delivery Line (4 modules / 12 lessons)
    ├── module-1-the-assembly-line/           # Why Automate · Your First Flow · The Designer Toolbox
    ├── module-2-where-automations-begin/     # Every Way to Start · The Right Conditions · Run It Your Way
    ├── module-3-branching-and-data/          # Branch the Route · Pass the Data · Handle the Detours
    └── module-4-run-it-for-real/             # Reusable Blocks · When to Use What · Watch It Run
└── open-the-loading-dock/                    # Open the Loading Dock (4 modules / 12 lessons)
    ├── module-1-the-outbound-desk/           # Why Integrate · Your First Outbound Call · Reading the Response
    ├── module-2-who-are-you/                 # Keys and Passwords · The OAuth Handshake · Aliases, Not Hardcoded Secrets
    ├── module-3-the-inbound-dock/            # The Partner Calls In · Bring the Batch · Beyond Flat Files
    └── module-4-wiring-it-up/                # The Spoke and the Hub · Watch the Wires · The Integration Capstone
```

> **Naming rule:** courses never reuse ServiceNow-owned or market-standard names — every course/module/lesson uses a simple catchy phrase told through the GlidePort story.

### The Story — GlidePort Logistics 🚚
All courses follow one fictional logistics company. You join GlidePort's IT team and grow a platform; every course extends the **Delivery App** (Order & Tracking, Delivery Agents) built in ServiceNow Basics. Scripting makes it smart, future courses will automate it (Flows), integrate it (APIs), surface it (Portal), and measure it (Reporting).

### Quizzes
- One **quiz per module**, authored as `quiz.md` inside each module folder (simple Q/A format with a `CORRECT:` and `EXPLAIN:` line per question).
- Graded & self-paced: answered on `/course/<slug>/<module>/quiz`, scored immediately, pass mark **60%**, answers + reasoning revealed after submission.
- `QuizAttempt` model stores every attempt; the best score shows on the course curriculum and lesson sidebar.
- `utils.py` parses quizzes (`load_module_quiz`, `grade_quiz`) and exposes best-score summaries (`quiz_summary`, `module_quiz_summaries`); `routes/quizzes.py` + `templates/quiz.html` / `quiz_result.html` handle the flow.

### Content Notes
- Curriculum was rebuilt from the `Admin & Dev Aug-Sep/` training docs (Days 1–9 + Virtual Agent/ChatGPT lab) and updated for current platform terminology:
  - Next Experience UI / Unified Navigation (All menu, Favorites, filter navigator)
  - Current platform releases (Washington DC → Xanadu → Yokohama → Zurich → Australia) and free PDIs at developer.servicenow.com
  - OpenAI integration uses the current chat-completions API (`/v1/chat/completions`, `gpt-4o-mini`) instead of the legacy `/v1/completions` endpoint
  - Modern tooling notes: Flow Designer over legacy Workflow, AI Agent Studio / Now Assist alongside classic Virtual Agent topics, App Engine Studio / Source Control as update-set alternatives
- `utils.py` gained a `display_title()` helper so module/lesson titles render brand-correctly (ServiceNow, UI, ACL, ChatGPT, etc.)
- `extensions.py` markdown converter now enables `tables` and `fenced_code` for rich lesson rendering; `Markdown` added to `requirements.txt`
- `create_database` auto-seeds any `content/` folder as a course (story-aware titles/descriptions for known courses, generic otherwise)

### Lab Runnability & the Practice Ground (12 Oct 2026)
- **Every lab is runnable.** Platform courses need only a free **PDI** (`developer.servicenow.com`); the integration course needs a few **free public sandboxes**. No fictional endpoints remain.
- Shared guide: **`content/_lab-setup.md`** → route `GET /lab-setup` (`templates/lab_setup.html`), linked from the **top nav** and a **banner on every course page**.
- Sandboxes used by *Open the Loading Dock* (all verified live):
  - **Van partner** — `https://dummyjson.com` (`/carts/{id}`, `POST /carts/add`, `/users`)
  - **Request & auth** — `https://httpbin.org` (`/basic-auth/...`, `/bearer`, `/headers`, `/status/{code}`)
  - **OAuth server** — `https://demo.duendesoftware.com` (real `client_credentials`: client `m2m` / secret `secret` / scope `api` → `GET /api/test`)
  - **Live feed** — `https://api.open-meteo.com`
  - Fallbacks: `httpbingo.org` (httpbin mirror), `jsonplaceholder.typicode.com`.
- Inbound labs are simulated by the learner (a test client such as `curl`/Hoppscotch, **or** a second PDI).
- The ChatGPT lesson (`servicenow-basics` M10L2) gained a **no-key mock path** (`https://httpbin.org/post`, read `body.json.prompt`) plus a free-tier note (Groq/OpenRouter).

## Content & Lab Authoring Playbook (read this before building the next course)

**Story first.** Every course continues the **GlidePort Logistics** arc and extends the Delivery App. Never reuse ServiceNow-owned or market-standard names — titles are catchy phrases. Register new course titles/descriptions in `app.py` `KNOWN_COURSES`.

**Folder shape.** `content/<course-slug>/module-N-name/NN-lesson.md`, plus exactly one `quiz.md` per module. Discovery is automatic (`utils.load_course_structure`); `create_database(app)` auto-seeds any new content folder as a course. Lesson titles come from the filename (the loader strips the `NN-` prefix).

**Lesson shape** (match the existing courses): `# Title` · a one-line **Story so far** · concept sections with tables/diagrams · a `## Lab: …` · `**Check your work:**` · `## Key Takeaways` · `## Best Practices`.

**The hard rule — every lab must actually run.**
- **Platform labs** (tables, forms, scripts, Business Rules, flows, Scripted REST, ACLs…) → run on a free **PDI**. That is the only prerequisite; point learners at **[`/lab-setup`]**.
- **Integration labs** → use the verified **public sandbox set** and **never invent an endpoint**:
  - `https://dummyjson.com` — data (`/carts/{id}`, `POST /carts/add`, `/users`)
  - `https://httpbin.org` — auth / status / echo (`/basic-auth/...`, `/bearer`, `/headers`, `/status/{code}`)
  - `https://demo.duendesoftware.com` — real OAuth `client_credentials` (client `m2m` / secret `secret` / scope `api`) → `GET /api/test`
  - `https://api.open-meteo.com` — genuinely live, changing data
- **Inbound** labs ("the partner calls you") → the learner *simulates* the partner with a test client (`curl`/Hoppscotch) **or a second PDI** (see `_lab-setup.md` Part 3).
- **No free public API for a concept?** Fall back to **two PDIs calling each other** — never ship a fictional URL.
- **Keep endpoints in one place:** add any new sandbox to `content/_lab-setup.md` and link labs to `/lab-setup`. Swapping a dead service is then a one-line change. Documented fallbacks: `httpbingo.org` (httpbin mirror), `jsonplaceholder.typicode.com` (simpler CRUD).

**Before writing a lab, verify the endpoint.** `curl` it and confirm the exact status/shape you will promise (e.g. `POST https://dummyjson.com/carts/add` → **201** with a new `id`). Bake the real expected result into `**Check your work:**`.

**Quizzes.** One `quiz.md` per module: `# Quiz: Title`, then `N. question`, `   A. …` options, `   CORRECT: B`, `   EXPLAIN: …` (parsed by `utils.py`). Pass mark **60%**. Keep answers consistent with whatever endpoint/field the lesson now uses.

**After adding content:** it auto-seeds on the next app start (or use **Admin → Seed from Content**). Render-test new pages with Flask's test client (`app.test_client()`, disabling `SITE_PASSWORD`) before committing.

### Naming Conventions
- **Courses**: kebab-case (e.g., `servicenow-basics`)
- **Modules**: `module-N-description` format
- **Lessons**: `NN-lesson-name.md` format (NN = sequential number)
- **Titles**: Extracted by slicing/title-casing directory/file names

---

## Templates
- **layout.html**: Base template — light sticky navbar (64px), Poppins/Inter fonts, shared stylesheet, footer
- **home.html**: Hero section + search/sort bar + Coursera-style course card grid (thumbnails, level badge, ratings, CTA)
- **course_detail.html**: Curriculum card layout with breadcrumbs and lesson lists per module
- **lesson_detail.html**: Lesson content panel (Q&A/Notes tabs) + collapsible course sidebar with active state
- **login.html**: Elevated centered auth card per spec
- **register.html**: Elevated centered auth card per spec
- **my_courses.html**: Enrolled courses dashboard — cards with enrolled date, progress bar, "Continue Learning", unenroll
- **profile.html**: User dashboard — stats, overall progress, per-course progress
- **error.html**: Styled 403/404/500 page
- **admin/courses.html**: Course management table (+ "Feedback Inbox" button)
- **admin/course_form.html**: Create/edit course form
- **admin/feedback.html**: Admin feedback inbox (status, type, message, source page, read/unread + delete)
- **quiz.html**: Module quiz form
- **quiz_result.html**: Graded score + revealed answers/reasoning
- **gate.html**: Standalone shared-password unlock screen (private preview)
- **feedback.html**: Tester feedback form + their recent submissions
- **lab_setup.html**: Renders the shared Lab Setup & Practice Ground guide (`content/_lab-setup.md`)

## Styling (static/css/main.css)
- **Design tokens**: CSS variables for palette, typography, spacing (8px grid), radii, shadows
- **Colors**: Primary `#2F5BE7` / dark `#1E3FA0`, success `#10B981`, warning `#F97316`, slate neutrals (`#0F172A`, `#475569`, `#94A3B8`), backgrounds `#F8FAFC` / `#F1F5F9`, border `#E2E8F0`
- **Light theme**: White/gray backgrounds, WCAG AA focus states, responsive breakpoints

---

## Dependencies (requirements.txt)
- Flask
- Flask-Login
- Flask-SQLAlchemy
- werkzeug (password hashing)
- waitress (production server)
- python-dotenv (environment config)
- Markdown (lesson content rendering)

---

## Configuration
- **SECRET_KEY**: Loaded from environment (`.env` file via `python-dotenv` or shell env); falls back to insecure default with a warning if missing. Compliant with production best practice.
  - Generate a strong key: `python -c "import secrets; print(secrets.token_hex(32))"`
- **DATABASE**: SQLite at `learning_portal.db` by default; override with `DATABASE_URL` (supports Postgres etc.)
- **HOST / PORT**: Read from env, used by `run.py` (dev) and `serve.py` (Waitress)
- **SITE_PASSWORD**: Optional shared-password gate for private previews. When set, every page except `/gate` and `/static/` requires it once per session; empty/unset disables the gate.
- **ADMIN_USERNAMES**: Comma-separated usernames auto-promoted to admin at boot (else the first user becomes admin).
- **SQLALCHEMY_TRACK_MODIFICATIONS**: False (performance optimization)
- **Login View**: Redirects unauthenticated users to `/login`
- **.env.example**: Documented template; real `.env` is git-ignored

---

## Running the Project
```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment (copy template, then fill in values)
cp .env.example .env

# Run development server
python run.py

# Or use production server (Waitress)
python serve.py

# Share a temporary public link (Waitress + Cloudflare quick tunnel; prints the URL)
./start-local.sh
./stop-local.sh
```

> The real interpreter here is `/opt/anaconda3/bin/python3.12` (the default `python3` lacks the deps). Locally, `run.py` uses the dev server (debug); for anything public, use `serve.py`/`wsgi.py` (Waitress), never `run.py`.

---

## Development Notes
- Routes are modularized into blueprints in `routes/` (previously defined in app.py)
- Markdown converter initialized and used in `routes/courses.py`
- Progress tracking implemented via `LessonProgress` model + `course_progress()` helper
- Course enrollment implemented via `CourseEnrollment` model + routes
- Admin management UI gated by `User.is_admin` (bootstrap: `ADMIN_USERNAMES` env var or first user)
- Styled error handlers for 403/404/500
- Form validation on auth + course management forms
- Session management includes "remember me" for login persistence

---

## TODO / Next Phase

### Roadmap — ALL 9 items COMPLETE ✅
- [x] UI redesign to market-standard light theme (roadmap #1)
- [x] Enrollment tracking: CourseEnrollment model + enroll/unenroll routes + My Courses page (roadmap #2)
- [x] Progress tracking: LessonProgress model + complete/reset routes + progress bars (roadmap #3)
- [x] Modular routes: blueprint-per-domain route files + utils.py (roadmap #4)
- [x] Environment variables: SECRET_KEY/DATABASE_URL/HOST/PORT via .env + docs (roadmap #5)
- [x] Course management interface: admin blueprint + is_admin flag + seed-from-content + admin templates (roadmap #6)
- [x] Error handling & validation: 403/404/500 handlers + form validation + categorized flash messages (roadmap #7)
- [x] User profile dashboard: /profile page with stats + overall progress (roadmap #8)
- [x] Course search/filtering: home search by title/description + sort + empty state (roadmap #9)

### Next Phase — Content Preparation
- [x] **Private-preview infrastructure** (12 Oct 2026): shared-password gate + in-app feedback + `wsgi.py` / `DEPLOY.md` production setup; commit `0fe730f` pushed
- [ ] **Stable public URL**: deploy to a free host (**PythonAnywhere** — see `DEPLOY.md`) so the link stops changing
- [x] Rebuilt the ServiceNow course as a 10-module / 18-lesson curriculum from the `Admin & Dev Aug-Sep/` training materials
- [x] Added **quizzes** — one per module, graded with reveal-answer + reasoning (QuizAttempt model + `/course/<slug>/<module>/quiz`)
- [x] Added **Make the Platform Think** (`make-the-platform-think`, formerly `servicenow-scripting`) as the second GlidePort course
- [x] **Trademark-safe naming**: renamed the scripting course/modules/lessons to catchy phrases (no ServiceNow-owned or market-standard names)
- [x] Expanded **Make the Platform Think** to 5 modules / 15 lessons + 5 quizzes (added Client Scripts + Service Catalog scripting labs)
- [x] Added **Build Your Own API** (`build-your-own-api`) — Script Includes & GlideAjax + Scripted REST endpoints (2 modules / 6 lessons + 2 quizzes)
- [x] Added **Automate the Delivery Line** (`automate-the-delivery-line`) — the Flow Designer & Automation course: 4 modules / 12 lessons + 4 quizzes (triggers, conditions/run modes, flow logic, data, error handling, subflows/custom actions, tool selection, monitoring)
- [x] Added **Open the Loading Dock** (`open-the-loading-dock`) — the REST APIs & Integrations course: 4 modules / 12 lessons + 4 quizzes (outbound REST, credentials/OAuth/aliases, inbound events & idempotency, import sets & data streams, spoke vs REST step, monitoring)
- [x] **Made every lab runnable (12 Oct 2026):** *Open the Loading Dock* rewired to live public sandboxes (DummyJSON / httpbin / Duende OAuth / Open-Meteo) with concrete expected results; shared **`/lab-setup`** page added (nav + course banner); ChatGPT lesson given a no-key mock path
- [ ] Review lesson wording/walkthroughs in-app and tune as needed
- [ ] Add content for pre-seeded courses (ITOM, Service Mapping) so they aren't empty
- [ ] Course thumbnails: current cards use gradient placeholders; replace with per-course `static/images/<slug>.jpg`
- [ ] Next course in queue: Service Portal & UX (GlidePort arc)

---

## Preview & Feedback Infrastructure

- **Shared-password gate** (`routes/gate.py`, `templates/gate.html`): when `SITE_PASSWORD` is set in the environment, an app-level `before_request` in `app.py` redirects every request (except `/static/` and `/gate`) to `/gate` until the visitor enters the shared password (`session['site_unlocked']`). Empty/unset = gate disabled (normal local dev).
- **In-app feedback** (`routes/feedback.py`): `Feedback` model (`models/models.py`); `GET/POST /feedback` lets logged-in testers submit (category + message + source page) and see their own history; `GET /admin/feedback` is the admin inbox with read/unread toggle and delete. "Feedback" nav link for authenticated users + "Feedback Inbox" button on the admin courses page.
- **Production WSGI entry** (`wsgi.py`): exposes `application` for gunicorn / PythonAnywhere; runs `create_app()` + `create_database()`.
- **Local share scripts**: `start-local.sh` (Waitress + Cloudflare quick tunnel, prints the public URL) and `stop-local.sh`. Logs go to `logs/` (git-ignored).
- **Deploy guide** (`DEPLOY.md`): quick tunnel vs. PythonAnywhere (free, persistent, recommended) vs. Render (free but ephemeral disk), plus the security checklist.

---

## Recent Work — 12 Oct 2026

**Goal:** let testers in different locations use the portal and send feedback while development continues.

**Public preview**
- Installed **cloudflared** (Homebrew) and exposed the local app through a **Cloudflare quick tunnel** → `https://skirt-glucose-weather-actively.trycloudflare.com` (temporary; the URL changes on every restart).
- Served the public face with **Waitress** (`serve.py`) instead of the Flask dev server, so the interactive debugger is never exposed.
- Confirmed `SECRET_KEY` is strong (65 chars, in `.env`); **rotated the `admin` password** to a strong random value (kept out of the repo).
- Verified the whole flow through the public URL: home → 302 to gate → unlock → login → browse → feedback submit → admin inbox.

**Private-preview features (built today)**
- Optional **shared-password gate** (`SITE_PASSWORD`).
- **Feedback**: testers submit; admins read at `/admin/feedback`.
- Production entry (`wsgi.py`) + local share scripts (`start-local.sh`, `stop-local.sh`) + `DEPLOY.md`.

**Version control**
- First large sync in a while: untracked generated files (`.DS_Store`, `__pycache__`, `instance/*.db`), git-ignored the source training docs (`Admin & Dev Aug-Sep/`), committed **`0fe730f`** (143 files) and pushed to **`origin/Initial-Dev`**.

**Still open:** a *stable* public URL (deploy to PythonAnywhere per `DEPLOY.md`); the account setup is the user's step.

---

## Recent Work — 12 Oct 2026 (Lab runnability pass)

**Goal:** make every hands-on lab actually executable.

- **Review finding:** *Open the Loading Dock* used fictional hosts (`api.shipping.example`, `auth.shipping.example`), so no integration lab could run; the ChatGPT lesson required a **paid** OpenAI key. The other four courses are PDI-only and were already runnable.
- **Fix:** rewrote the integration labs against verified free public sandboxes (DummyJSON, httpbin, Duende demo OAuth, Open-Meteo) with concrete expected results; added the shared **`/lab-setup`** page (top nav + banner on every course page); gave the ChatGPT lesson a **no-key mock path**.
- **Detail:** see the "Lab Runnability & the Practice Ground" section above.

---

## Environment & Tools
- Python 3.8+
- VS Code workspace at: `/Users/aswinipula/ATOM`
- Available tasks: "Run Learning Portal", "Install Requirements"

