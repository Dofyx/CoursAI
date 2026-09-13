#!/bin/bash

APPDIR="/opt/coursia"
VENV="$HOME/.local/share/coursia/.venv"

mkdir -p "$HOME/.local/share/coursia"

if [ ! -d "$VENV" ]; then
    python -m venv "$VENV"

    source "$VENV/bin/activate"

    python -m pip install --upgrade pip

    pip install -r "$APPDIR/requirements.txt"
else
    source "$VENV/bin/activate"
fi

cd "$APPDIR"

exec python main.py
