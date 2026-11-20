#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")"
if [ "$(uname -s)" = Darwin ] && command -v brew >/dev/null 2>&1; then
    fribidi_prefix=$(brew --prefix fribidi)
    if [ -d "$fribidi_prefix/lib" ]; then
        DYLD_FALLBACK_LIBRARY_PATH="$fribidi_prefix/lib:${DYLD_FALLBACK_LIBRARY_PATH:-/usr/local/lib:/usr/lib}"
        export DYLD_FALLBACK_LIBRARY_PATH
    fi
fi
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
