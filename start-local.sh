#!/usr/bin/env bash
# Start the ATOM learning portal (Waitress) + a Cloudflare quick tunnel,
# then print the public URL to share with testers. Safe to re-run.
#
# Usage:  ./start-local.sh
# Stop:   ./stop-local.sh
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

# Prefer the Anaconda interpreter that has the project's dependencies.
PYTHON_BIN="${PYTHON_BIN:-/opt/anaconda3/bin/python3.12}"
if [ ! -x "$PYTHON_BIN" ]; then
  PYTHON_BIN="$(command -v python3)"
fi

PORT="$(grep -E '^PORT=' .env 2>/dev/null | cut -d= -f2- | tr -d ' ' || true)"
PORT="${PORT:-5001}"

mkdir -p logs

echo "==> Stopping any previous instance..."
pkill -f "serve.py" 2>/dev/null || true
pkill -f "cloudflared tunnel --url" 2>/dev/null || true
sleep 1

echo "==> Starting app with Waitress on port $PORT..."
nohup "$PYTHON_BIN" serve.py > logs/app.log 2>&1 &
echo "    app pid $! (logs/app.log)"

for _ in $(seq 1 30); do
  if curl -s -o /dev/null "http://127.0.0.1:$PORT/"; then
    echo "    app is up."
    break
  fi
  sleep 0.5
done

echo "==> Starting Cloudflare quick tunnel..."
nohup cloudflared tunnel --url "http://localhost:$PORT" --no-autoupdate > logs/tunnel.log 2>&1 &
echo "    tunnel pid $! (logs/tunnel.log)"

echo "==> Waiting for the public URL..."
URL=""
for _ in $(seq 1 40); do
  URL="$(grep -Eo 'https://[a-zA-Z0-9.-]+\.trycloudflare\.com' logs/tunnel.log | head -1 || true)"
  [ -n "$URL" ] && break
  sleep 0.5
done

echo
if [ -n "$URL" ]; then
  echo "=========================================================="
  echo "  PUBLIC URL:  $URL"
  echo "=========================================================="
else
  echo "Public URL not ready yet — check logs/tunnel.log in a few seconds."
fi
echo
echo "Local:   http://127.0.0.1:$PORT"
echo "Logs:    logs/app.log  |  logs/tunnel.log"
echo "Stop:    ./stop-local.sh"
