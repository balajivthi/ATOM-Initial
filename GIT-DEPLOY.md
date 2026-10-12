# Git Deploy to PythonAnywhere

The public site (**https://vtbalaji94.pythonanywhere.com**) runs from `~/ATOM` on PythonAnywhere, which was first uploaded as a **zip** — so it started with **no `.git`**. This file covers the one-time conversion, then the routine.

**Two constraints of the free plan:**
- **SSH is blocked** → always use the `https://…` remote (never `git@github.com:`).
- The repo (`balajivthi/ATOM-Initial`) is **private** → you need a token.

---

## Step 0 — Create a read-only GitHub token (once)

1. GitHub → **Settings → Developer settings → Personal access tokens → Fine-grained tokens → Generate new token**.
2. **Repository access:** only `balajivthi/ATOM-Initial`.
3. **Permissions → Repository permissions → Contents: Read-only** (read is all `git pull` needs).
4. Copy it (`github_pat_…`). Treat it like a password.

---

## Step 1 — One-time: make `~/ATOM` a git repo

In a PythonAnywhere **Bash console** (replace `<GITHUB_PAT>` with your token):

```bash
cd ~/ATOM

git init
git remote add origin https://balajivthi:<GITHUB_PAT>@github.com/balajivthi/ATOM-Initial.git

git fetch origin
git checkout -f -B Initial-Dev origin/Initial-Dev
git branch --set-upstream-to=origin/Initial-Dev Initial-Dev

git log --oneline -3   # should show the latest commit
git status              # should be clean
```

`.env`, `instance/learning_portal.db`, and `logs/` are **git-ignored**, so they are left untouched (checkout does not delete untracked files). No `git config user.email` is needed — the server only pulls, never commits.

## Step 2 — Activate

**Web tab → Reload.** (Reload re-runs `wsgi.py` → `create_database`, which auto-seeds new content.)

---

## Routine from now on

```bash
# On your Mac
git add -A && git commit -m "…" && git push

# On PythonAnywhere (Bash console)
cd ~/ATOM && git pull

# In the PythonAnywhere Web tab
Reload
```

---

## Gotchas

- **SSH won't work** on the free plan — keep the `https://` remote.
- **`git pull` alone is not enough** — you must also click **Reload**, or templates/WSGI code stay stale. (Lesson `.md` content is read per request, so content changes can appear before a reload, but code/template changes need it.)
- **New dependencies are not installed by a pull.** Run `pip install -r requirements.txt` in the venv (`workon atom-env`).
- **Token in the URL** sits in plaintext in `~/ATOM/.git/config`; it is read-only and scoped to one repo, but revoke it if it leaks. Alternative: `git config --global credential.helper store` and let the first pull prompt (stores to `~/.git-credentials`).
- **If `git pull` refuses** due to local changes: `git status` on the server. Edit locally and push — never edit server files directly.
