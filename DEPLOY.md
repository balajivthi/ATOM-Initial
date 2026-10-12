# Deploying the ATOM Learning Portal

Three ways to let other people use the portal, from quickest to most permanent.

| Method | URL type | Free? | Stays up when your Mac is off? | Data persists? |
|---|---|---|---|---|
| **Quick tunnel** (`./start-local.sh`) | random `*.trycloudflare.com`, changes each run | Yes, no account | ❌ No — your Mac must be awake | ✅ Yes (local DB) |
| **PythonAnywhere** (recommended) | stable `https://<username>.pythonanywhere.com` | Yes, no card | ✅ Yes | ✅ Yes (SQLite on disk) |
| **Render** | stable `*.onrender.com` | Yes | ✅ Yes | ⚠️ **No** — free disk is wiped on restart |

> The app already includes an optional **shared-password gate** and an in-app **feedback
> inbox**. Both work identically on every host below — no code changes needed.

---

## 0. Environment variables

The app reads these from the environment (locally, from `.env`):

| Variable | Required | Purpose |
|---|---|---|
| `SECRET_KEY` | ✅ | Signs login sessions. Use a long random string. |
| `DATABASE_URL` | — | Defaults to `sqlite:///learning_portal.db`. |
| `HOST` / `PORT` | — | Server binding (used by `serve.py`). |
| `SITE_PASSWORD` | — | If set, locks the whole site behind one shared password. Leave empty to disable. |
| `ADMIN_USERNAMES` | — | Comma-separated usernames to auto-promote to admin on boot. |

Generate a secret with:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## 1. Quick tunnel (temporary — for a feedback round right now)

```bash
./start-local.sh      # starts the app + tunnel, prints the public URL
./stop-local.sh       # stops both
```

The URL changes every time you restart. Fine for "try this and tell me what you think",
not for a link that lives in a chat for weeks.

---

## 2. PythonAnywhere — stable, free, persistent (recommended)

No credit card. Your SQLite data (accounts, progress, feedback) survives restarts.

### A. Create the account
1. Go to <https://www.pythonanywhere.com> and sign up for the **Beginner (Free)** plan.
2. Pick a username — it becomes your URL: `https://<username>.pythonanywhere.com`.

### B. Get the code onto the server
Open a **Bash console** (Dashboard → *New console* → *Bash*), then either:

**Git clone** (if the repo is reachable):
```bash
git clone <your-repo-url> ATOM
cd ATOM
```
Private repo? Use a token in the URL, or upload a zip via the **Files** tab and unzip it.

**Or upload:** from your Mac, zip the project *without* `.env`, `instance/`, and `logs/`,
upload via the **Files** tab, then unzip in the console.

### C. Create a virtualenv and install dependencies
```bash
mkvirtualenv --python=/usr/bin/python3.10 atom-env
cd ~/ATOM
pip install -r requirements.txt
```

### D. Create the web app
1. **Web** tab → **Add a new web app** → **Manual configuration** → **Python 3.10**.
2. Set:
   - **Source code:** `/home/<username>/ATOM`
   - **Working directory:** `/home/<username>/ATOM`
   - **Virtualenv:** `/home/<username>/.virtualenvs/atom-env`

### E. Point the WSGI file at the app
In the **Web** tab, click the **WSGI configuration file** link and replace its contents with:

```python
import os, sys

project = '/home/<username>/ATOM'
if project not in sys.path:
    sys.path.insert(0, project)

# --- Environment for this app ---
os.environ['SECRET_KEY']    = 'paste-a-long-random-value-here'
os.environ['SITE_PASSWORD'] = 'the-shared-gate-password'   # delete this line to disable the gate
os.environ['DATABASE_URL']  = 'sqlite:///learning_portal.db'
os.environ['ADMIN_USERNAMES'] = 'admin'

os.chdir(project)

from wsgi import application  # noqa: E402  (runs create_app + DB setup)
```

### F. Reload and test
Click the green **Reload** button, then visit `https://<username>.pythonanywhere.com`.

### Updating later
```bash
cd ~/ATOM && git pull     # or re-upload changed files
```
…then click **Reload** in the Web tab. To change the gate password, edit the WSGI file and reload.

### Free-tier notes
- PythonAnywhere emails you periodically to click **"Run until 3 months from now"** on the
  Web tab — do it to keep the site alive.
- Free accounts restrict *outbound* internet. This app makes no outbound calls, so it's fine.
- Data lives in `~/ATOM/instance/learning_portal.db` and persists.

---

## 3. Render — stable URL, but ephemeral data (alternative)

Quick to set up from GitHub, **but the free instance's filesystem is wiped** on every deploy
and after it sleeps (~15 min idle), so users/progress/feedback reset. Only use it for a pure
demo, or switch `DATABASE_URL` to a managed Postgres to persist.

If you still want it:
1. Push the repo to GitHub.
2. Render → **New** → **Web Service** → connect the repo.
3. **Build command:** `pip install -r requirements.txt gunicorn`
4. **Start command:** `gunicorn wsgi:application --bind 0.0.0.0:$PORT`
5. Add the environment variables from section 0 in the Render dashboard.

---

## Security checklist before sharing publicly

- [x] Run the **production server** (`serve.py` / gunicorn), never `run.py` (debug mode = RCE risk).
- [x] Set a strong `SECRET_KEY`.
- [x] Change the default `admin` password away from anything guessable.
- [x] Set `SITE_PASSWORD` so only people you give the password to can get in.
- [ ] Remember registration is open to anyone who gets past the gate — delete stray accounts in the DB if needed.
