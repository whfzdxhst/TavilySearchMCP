#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${APP_DIR:-$(pwd)}"
ENV_DIR="$APP_DIR/.conda"
PORT="${MCP_SERVER_PORT:-21029}"

cd "$APP_DIR"

if ! command -v conda >/dev/null 2>&1; then
  MINICONDA_DIR="$HOME/miniconda3"
  if [ ! -x "$MINICONDA_DIR/bin/conda" ]; then
    curl -fsSL -o /tmp/miniconda.sh \
      https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
    bash /tmp/miniconda.sh -b -p "$MINICONDA_DIR"
  fi
  export PATH="$MINICONDA_DIR/bin:$PATH"
fi

if conda tos --help >/dev/null 2>&1; then
  conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main || true
  conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r || true
fi

if [ ! -x "$ENV_DIR/bin/python" ]; then
  conda create -y -p "$ENV_DIR" python=3.11
fi

"$ENV_DIR/bin/python" -m pip install -r requirements.txt
"$ENV_DIR/bin/python" -m pip install -e .

if [ ! -f .env ]; then
  cp .env.example .env
fi

python_bin="$ENV_DIR/bin/python"
pkill -f "tavily_search_mcp.server" || true
nohup "$python_bin" -m tavily_search_mcp.server > server.log 2>&1 &

sleep 2
curl -fsS "http://127.0.0.1:${PORT}/health"
echo
