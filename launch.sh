#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")"
if [ ! -x .venv/bin/python ]; then
    python3 -m venv .venv
fi
if ! .venv/bin/python -c 'import PIL; from PIL import features; assert features.check_feature("raqm")' 2>/dev/null; then
    .venv/bin/python -m pip install --only-binary=:all: -r requirements.txt
fi
if [ "${1:-}" = "--smoke" ]; then
    exec .venv/bin/python tools/smoke.py
fi
exec .venv/bin/python server.py "$@"
