#!/usr/bin/env bash
# Stop the ATOM learning portal app and its Cloudflare tunnel.
set -uo pipefail

echo "==> Stopping Cloudflare tunnel..."
pkill -f "cloudflared tunnel --url" 2>/dev/null && echo "    tunnel stopped." || echo "    no tunnel running."

echo "==> Stopping Waitress app server..."
pkill -f "serve.py" 2>/dev/null && echo "    app stopped." || echo "    no app running."

echo "Done."
