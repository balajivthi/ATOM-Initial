## Roadmap Items

1. ~~**UI Enhancements**: Prioritize improving the UI design to match current market standards.~~ ✅ DONE
2. ~~**Enrollment Tracking**: Implement a `CourseEnrollment` model.~~ ✅ DONE
3. ~~**Progress Tracking**: Add progress tracking for users.~~ ✅ DONE
4. ~~**Modular Routes**: Create separate files for the routes.~~ ✅ DONE
5. ~~**Environment Variable**: Move the hardcoded `SECRET_KEY` to an environment variable.~~ ✅ DONE
6. ~~**Course Management Interface**: Develop a course seeding/management interface.~~ ✅ DONE
7. ~~**Error Handling and Validation**: Improve error handling and validation.~~ ✅ DONE
8. ~~**User Profile Dashboard**: Add a user profile/dashboard page.~~ ✅ DONE
9. ~~**Search/Filtering**: Implement course search/filtering.~~ ✅ DONE

**All 9 roadmap items are complete — the platform is feature-complete.**

## 📍 Session Memory — resume here

### 🗓️ 12 Oct 2026 — Made every lab actually runnable (real public sandboxes)
- **Problem found in the review:** *Open the Loading Dock* pointed every hands-on call at fictional hosts (`api.shipping.example`, `auth.shipping.example`), so **no lab could actually run**; the ChatGPT lesson required a **paid** OpenAI key. The other four courses are PDI-only and were already runnable.
- **Fix — free, no-install sandboxes (each verified live before adopting):**
  - **Van partner sandbox** `https://dummyjson.com` — `/carts/{id}` (manifest), `POST /carts/add` (201 + booking id), `/users`.
  - **Request & auth sandbox** `https://httpbin.org` — `/basic-auth/...` (401→200), `/bearer`, `/headers`, `/status/{code}`.
  - **OAuth server** `https://demo.duendesoftware.com` — real `client_credentials` (client `m2m` / secret `secret` / scope `api`) → protected `GET /api/test` (401 without token, 200 with).
  - **Live feed** `https://api.open-meteo.com` — genuinely changing data.
  - Fallbacks noted in the guide: `httpbingo.org` (httpbin mirror), `jsonplaceholder.typicode.com` (simpler CRUD).
- **New shared page:** `content/_lab-setup.md` → route `GET /lab-setup` (`templates/lab_setup.html`), linked from the **top nav** (“Lab Setup”) and an **info banner on every course page**. Holds PDI signup + all sandbox endpoints with copy-paste `curl` checks + “how to send an inbound test call” (test client **or** a second PDI — the two-instance trick).
- **Rewrote the labs** in Open the Loading Dock (M1L2/L3, M2L1/L2/L3, M3L1/L2/L3, M4L1/L2/L3) to run against the sandboxes, with concrete **expected results** (status codes, fields). Story kept (GlidePort + van partner); the sandbox is framed as the partner's stand-in — “only the URL and credentials change for a real partner.”
- **ChatGPT lesson** (`servicenow-basics` M10L2): added a **no-key mock path** (point at `https://httpbin.org/post`, read `body.json.prompt`) + free-tier note (Groq/OpenRouter) + why a local Ollama can’t work from a cloud PDI.
- **Housekeeping:** fixed the one fictional URL in *Automate* (M4L1 illustration); confirmed quizzes carry no fake endpoints.
- **Committed & pushed** `fdbdae6` (“Make every lab runnable: real public sandboxes + shared Lab Setup page”) to `origin/Initial-Dev`; also added the **Content & Lab Authoring Playbook** to `project-overview.md`.
- **Next: PythonAnywhere ↔ git.** Written up in **`GIT-DEPLOY.md`**. The **one-time server conversion is not yet run** (user will): in a PythonAnywhere Bash console, `cd ~/ATOM` → `git init` → add the `https://` remote with a **read-only GitHub PAT** → `git fetch` → `git checkout -f -B Initial-Dev origin/Initial-Dev`. After that the loop is: local `git push` → server `cd ~/ATOM && git pull` → Web tab **Reload**.

### 🗓️ 12 Oct 2026 — Public preview, gate, feedback, deploy prep, first big commit
- **Made the portal shareable for tester feedback.**
  - Installed **cloudflared** (Homebrew) and ran a **Cloudflare quick tunnel** to the local app → public URL `https://skirt-glucose-weather-actively.trycloudflare.com`.
    ⚠️ Temporary: the URL **changes on every restart** and only works while this Mac is awake — re-share the new URL each session.
  - Switched the public face from the **Flask dev server (debug ON)** to **Waitress** (`serve.py`) — debug mode must never be exposed.
  - Confirmed `SECRET_KEY` is strong (65 chars, lives in `.env`, git-ignored).
  - **Rotated the `admin` password** to a strong random value (shared with the user in chat — **not** stored in the repo).
- **Built private-preview infrastructure (all verified live):**
  - Optional **shared-password gate** — `routes/gate.py` + an `app.py` `before_request`, toggled by the `SITE_PASSWORD` env var; locks the whole site (except `/gate` + static) until unlocked. The gate password lives in `.env` — **never commit it**.
  - **In-app feedback** — `Feedback` model + `routes/feedback.py`: testers submit at `/feedback`; admin reads at **Admin → Feedback Inbox** (`/admin/feedback`, read/unread toggle + delete).
  - **Production entry** `wsgi.py`; **`start-local.sh`** (starts Waitress + tunnel and prints the public URL) / **`stop-local.sh`**; **`DEPLOY.md`** (quick tunnel vs **PythonAnywhere** — free + persistent + recommended — vs Render — free but ephemeral disk) plus a security checklist.
- **Committed & pushed** `0fe730f` (143 files) to `origin/Initial-Dev`, after untracking generated files (`.DS_Store`, `__pycache__`, `instance/*.db`) and git-ignoring `Admin & Dev Aug-Sep/`.
- **Remaining for sharing:** a **stable** public URL requires the PythonAnywhere deploy (the account is the user's to create). Code + `DEPLOY.md` are ready; the local quick-tunnel is the stopgap.

### Standing notes
- **Authoring playbook (for every future course):** see **`project-overview.md` → Content & Lab Authoring Playbook** — story-first, trademark-safe names, one quiz per module, and the hard rule that **every lab runs for real**: a free PDI for platform work, the verified public sandbox set (`dummyjson` / `httpbin` / Duende OAuth / Open-Meteo) for integrations, and **never** a fictional URL (fallback = two PDIs). New sandboxes go in `content/_lab-setup.md` only.
- **Deploying to PythonAnywhere:** see **`GIT-DEPLOY.md`** (one-time `git init` on the server + read-only PAT, then `push → pull → Reload`).
- **Courses live (all seeded, all verified):**
  - `servicenow-basics` — **Introduction to ServiceNow** (10 modules / 18 lessons + 10 quizzes)
  - `make-the-platform-think` — **Make the Platform Think** (5 modules / 15 lessons + 5 quizzes) — was `servicenow-scripting`, renamed to a catchy trademark-safe name
  - `build-your-own-api` — **Build Your Own API** (2 modules / 6 lessons + 2 quizzes)
  - `automate-the-delivery-line` — **Automate the Delivery Line** (4 modules / 12 lessons + 4 quizzes)
  - `open-the-loading-dock` — **Open the Loading Dock** (4 modules / 12 lessons + 4 quizzes)
  - `dive-deep-into-itom`, `what-is-service-mapping` — pre-seeded DB rows, **no content yet**
- **Naming rule (established):** never reuse ServiceNow-owned or market-standard course/module/lesson names in a course title — every title is a catchy phrase told through the GlidePort story. `app.py` `KNOWN_COURSES` holds the story titles/descriptions.
- **NEXT:** build **Service Portal & UX** (GlidePort arc step 3) — story hook: the customer-facing delivery tracking portal (place an order, track it live, manage notifications).
- **Open items:** ITOM + Service Mapping content; per-course thumbnails; stable deploy (PythonAnywhere).
- **Dev loop:** content is auto-seeded by `create_database(app)` (the dev server re-seeds on reload); verify new courses appear via home page; quiz format + parser live in `utils.py`.
  - **Start sharing after a reboot:** `cd /Users/aswinipula/ATOM && ./start-local.sh` (prints the public URL); `./stop-local.sh` to stop.
  - **Run locally (dev):** `/opt/anaconda3/bin/python3.12 run.py` (debug). **Run for sharing:** `/opt/anaconda3/bin/python3.12 serve.py` (Waitress).
  - **Keep DB Browser for SQLite closed** while the app runs, or writes fail with "database is locked".

## Next Phase: Content Preparation
The application shell is done. The main leverage now is real learning content.

**The story — GlidePort Logistics 🚚** (est. this phase): every course follows one fictional company. You join GlidePort's IT team and build a growing platform — the **Delivery App** (Order & Tracking, Delivery Agents) introduced in ServiceNow Basics gets smarter in every course. Courses connect the dots: scripting → automation → integration → portal → reporting.

- [x] Expand the ServiceNow course from 3 modules / 4 placeholder lessons into a full curriculum:
      **10 modules / 18 lessons** under `content/servicenow-basics/`, grounded in the
      `Admin & Dev Aug-Sep/` training docs (Days 1–9 + Virtual Agent/ChatGPT) and updated
      for current platform terminology (Next Experience UI, current releases, OpenAI chat-completions API).
- [x] Fine-tune the basics curriculum (terminology, walkthroughs, titles) during content pass.
- [x] Add **quizzes** — one per module, graded, self-paced with reveal-answer + reasoning. Implemented via `quiz.md` in each module folder, a `QuizAttempt` model, and `/course/<slug>/<module>/quiz` routes (score, pass/fail at 60%, retake).
- [x] **Make the Platform Think** (`make-the-platform-think`, formerly `servicenow-scripting`): JavaScript on the platform, GlideRecord, Business Rules, **Client Scripts, and Service Catalog scripting** — told through the Delivery App story.
- [x] **Trademark-safe naming**: renamed the scripting course and all its modules/lessons to simple catchy phrases so no name is owned by ServiceNow or generic market terminology (see naming table below).
- [x] Expanded **Make the Platform Think** to **5 modules / 15 lessons / 5 quizzes** — added *Scripts in the Browser* (Client Scripts 101, first Client Script lab, patterns) and *Self-Service Catalog* (build a catalog item, catalog client scripts, catalog client script lab).
- [x] **Build Your Own API** (`build-your-own-api`) — the advanced scripting course: **2 modules / 6 lessons + 2 quizzes** covering Script Includes & the AJAX pattern (client-callable Script Includes / GlideAjax) and Scripted REST endpoints (write, secure, test). Built and verified.
- [x] **Automate the Delivery Line** (`automate-the-delivery-line`) — the Flow Designer & Automation course: **4 modules / 12 lessons + 4 quizzes** (The Assembly Line · Where Automations Begin · Branching and Data · Run It for Real) covering triggers, conditions/run modes, flow logic, data pills & variables, error handling, subflows/custom actions, tool selection, and monitoring. Built and verified.
- [x] **Open the Loading Dock** (`open-the-loading-dock`) — the REST APIs & Integrations course: **4 modules / 12 lessons + 4 quizzes** (The Outbound Desk · Who Are You? · The Inbound Dock · Wiring It Up) covering outbound REST (RESTMessageV2), credentials & OAuth & aliases, inbound events/webhooks (auth, idempotency), Import Sets & Data Streams, IntegrationHub spokes vs REST steps, and integration observability. **Every lab now runs against live, free public sandboxes** (DummyJSON / httpbin / Duende demo OAuth / Open-Meteo) — see the shared **`/lab-setup`** page. Built and verified.
- [ ] Add content for pre-seeded course topics (ITOM, Service Mapping) so they aren't empty.
- [ ] Course thumbnails: current cards use gradient placeholders; replace with per-course `static/images/<slug>.jpg` (needs small template change if desired).

## Content Naming Rule (established)
Courses never reuse ServiceNow-owned or market-standard names. Every course/module/lesson gets a simple catchy phrase told through the GlidePort story:

| Course (slug) | Modules |
| --- | --- |
| **Make the Platform Think** (`make-the-platform-think`) | The Language of the Platform · Talk to the Database · Rules of the Game · Scripts in the Browser · Self-Service Catalog |
| **Build Your Own API** (`build-your-own-api`) | Script Includes & the AJAX Pattern · Scripted REST Endpoints |

## Next Course Queue (industry-standard path → GlidePort arc)
1. ~~**Build Your Own API**~~ ✅ built (advanced scripting — Scripted REST + client-callable Script Includes)
2. ~~**Flow Designer & Automation**~~ ✅ built as **Automate the Delivery Line** (`automate-the-delivery-line`, 4 modules / 12 lessons + 4 quizzes) — automate the delivery process end-to-end
3. ~~**REST APIs & Integrations**~~ ✅ built as **Open the Loading Dock** (`open-the-loading-dock`, 4 modules / 12 lessons + 4 quizzes) — outbound REST, credentials/OAuth/aliases, inbound events/webhooks, import sets, IntegrationHub spokes, monitoring. *(Scoped to integrations — Scripted REST authoring stays in Build Your Own API.)*
4. **Service Portal & UX** — customer-facing delivery tracking portal — *next build*
5. **Reporting & Performance Analytics** — SLA + fleet dashboards
6. **CMDB / Discovery / Service Mapping** — map the IT behind deliveries
7. **ITSM Process Design** — Incident/Change/Problem/SLA for the support side
8. **Security & Governance** — ACLs deep-dive, SSO, audit
9. **Now Assist / AI Agents** — GenAI customer assistant

Each new course keeps the story hook and ships one quiz per module (pass 60%, reveal-answer).

> After adding content folders, run the admin **"Seed from Content"** action (`/admin/courses`) to register new courses, or `python create_database(app)` -> it auto-seeds `servicenow-basics` (and any missing courses) if required.

## Completed Items
- [x] **UI Enhancements**: Full redesign to a light, market-standard theme per the UI Design Specification — design tokens (color palette `#2F5BE7` primary / `#10B981` success), Poppins + Inter typography, 8px spacing grid, sticky light navbar, gradient hero, Coursera-style course cards, modern curriculum & lesson layouts, spec-compliant buttons/inputs/badges/progress bars, responsive breakpoints, and WCAG AA focus states. Centralized in `static/css/main.css`.
- [x] **Enrollment Tracking**:
  - `CourseEnrollment` model (`user_id`→user, `course_id`→course, `enrolled_at`, unique on user+course).
  - Added `Course.slug` to link DB courses to `content/` directories, with a lightweight auto-migration in `create_database` (ALTER + backfill + sanitize via `slugify`).
  - Routes: `POST /course/<slug>/enroll` (idempotent), `POST /course/<slug>/unenroll`, and `GET /my-courses`.
  - UI: "My Courses" nav link, per-course enroll/unenroll buttons with "Enrolled" badge on `course_detail`, `my_courses.html` dashboard with enrolled date, continue + unenroll actions.
- [x] **Progress Tracking**:
  - `LessonProgress` model (`user_id`→user, `course_id`→course, `module_slug`, `lesson_slug`, `completed_at`, unique on user+course+lesson).
  - Routes: `POST /course/<slug>/<module>/<lesson>/complete` and `/reset` (toggle complete).
  - Refactored duplicate module/lesson discovery into `load_course_structure()`; added `course_progress()` helper computing completed set + percentage.
  - UI: "Mark as Complete"/"Mark as Incomplete" buttons + Completed badge on `lesson_detail`, per-lesson green check icons in curriculum + sidebar, progress bars (striped while in progress, green at 100%) on `course_detail`, `lesson_detail` sidebar, and `my_courses` (with "Review Course" + award badge when finished).
- [x] **Modular Routes**:
  - Moved routes out of `app.py` into Flask blueprints under `routes/`: `auth.py`, `courses.py`, `enrollments.py`, `progress.py`.
  - Moved shared helpers (`slugify`, `load_course_structure`, `course_progress`) into `utils.py`.
  - `app.py` is now just the app factory + extension init + blueprint registration, with all `url_for` references in templates updated to blueprint endpoints (e.g. `courses.home`, `auth.login`).
- [x] **Environment Variable**:
  - `create_app` now calls `load_dotenv()` and reads `SECRET_KEY`, `DATABASE_URL`, `HOST`, `PORT` from environment (`.env` file or shell env), with a fallback default + printed warning if `SECRET_KEY` is absent.
  - Added `.env.example` (documented template) and a real `.env` (git-ignored via `.gitignore`).
  - `run.py` and `serve.py` use the env-driven host/port; `python-dotenv` added to `requirements.txt`.
  - **Deployment note**: generate a strong secret with `python -c "import secrets; print(secrets.token_hex(32))"`.
- [x] **Course Management Interface**:
  - Added `User.is_admin` flag (migration in `create_database` + bootstrap: users in `ADMIN_USERNAMES` env var, else the first user, are promoted to admin).
  - New `routes/admin.py` blueprint with `admin_required` decorator: course list, create, edit, delete, and "seed from content/" (auto-registers missing courses from the filesystem).
  - Templates: `templates/admin/courses.html` (table with view/edit/delete) and `admin/course_form.html` (create/edit form with slug auto-generation + duplicate-slug validation).
  - "Admin" nav link shown only to admins; non-admins get a 403 page.
- [x] **Error Handling and Validation**:
  - Error handlers for 403/404/500 rendering a styled `templates/error.html` (code, message, home/My Courses buttons).
  - Form validation: register (username required + min 3 / max 150, password required + min 6, duplicate-username check), login (empty field check), course forms (required title/description, max title length, duplicate-slug check).
  - Flash messages now support categories (success → green, error → red, default → warning) in the layout.
- [x] **User Profile Dashboard**:
  - Added `User.created_at` (migration + backfill; template is defensive if None) for member-since display.
  - New `routes/profile.py` blueprint with `GET /profile` dashboard: avatar initial, member-since, admin badge, stat cards (courses / in progress / completed / lessons), overall progress bar, and per-course progress list with Continue/Review CTA.
  - "Profile" nav link for authenticated users.
- [x] **Search/Filtering**:
  - Home page search bar (`?q=`) filtering courses by title/description (case-insensitive), a clear-search button, live course count, sort options (A–Z / Newest), and an empty-state message when nothing matches.
- [x] **Preview & Feedback Infrastructure**:
  - Optional shared-password **gate** (`routes/gate.py` + `app.py` `before_request`) controlled by the `SITE_PASSWORD` env var — locks the whole site (except `/gate` and static) behind one password for private previews; disabled when unset.
  - **In-app feedback**: `Feedback` model + `routes/feedback.py` (`/feedback` for testers, `/admin/feedback` inbox with read/unread toggle + delete) + nav link and admin-inbox button.
  - `wsgi.py` production entry point; `start-local.sh` / `stop-local.sh` (Waitress + Cloudflare quick tunnel); `DEPLOY.md` guide (quick tunnel / PythonAnywhere / Render) + security checklist.
  - **Public preview (12 Oct 2026):** installed **cloudflared** (Homebrew); served the app publicly via **Waitress** (debug off) behind a **Cloudflare quick tunnel** (`https://skirt-glucose-weather-actively.trycloudflare.com`, ephemeral URL); **rotated the `admin` password**; confirmed `SECRET_KEY` strength; verified gate + feedback end-to-end through the public URL.
  - **Repo hygiene + first big sync (12 Oct 2026):** untracked generated files (`.DS_Store`, `__pycache__`, `instance/*.db`) and git-ignored `Admin & Dev Aug-Sep/`; committed `0fe730f` (143 files) and pushed to `origin/Initial-Dev`.

---

## Pointers
1. **Content**: Author real Markdown courses under `content/` and seed them via `/admin/courses` → "Seed from Content".