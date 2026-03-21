#!/usr/bin/env bash
# Angehlang Launcher — run.sh
# Usage: ./run.sh              → opens the interactive REPL
#        ./run.sh myfile.angeh → runs a file

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

if [ -z "$1" ]; then
    echo "Starting Angehlang REPL (type .help for commands)..."
    python3 "$SCRIPT_DIR/core/interpreter.py"
else
    python3 "$SCRIPT_DIR/core/interpreter.py" "$1"
fi
