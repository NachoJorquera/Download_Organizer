#!/bin/bash
set -e

cd "$(dirname "$0")" || { echo "Failed to cd into project directory" >&2; exit 1; }

# Export the variables in .env (DOWNLOADS_PATH) to the organizer when the file exists.
if [ -f .env ]; then
    set -a
    source .env
    set +a
fi

python3 download_organizer.py
