#!/bin/bash
# Installs the LaunchAgent: copies the plist with paths from .env and this clone, then reloads it.
# Usage: ./install.sh (run again after changing .env or moving the project folder).
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
LABEL="com.project.organize_downloads"
TARGET="$HOME/Library/LaunchAgents/$LABEL.plist"

if [ ! -f "$PROJECT_DIR/.env" ]; then
    echo "Missing .env: copy .env.example to .env and adjust it." >&2
    exit 1
fi

set -a
source "$PROJECT_DIR/.env"
set +a
: "${DOWNLOADS_PATH:?DOWNLOADS_PATH must be set in .env}"

cp "$PROJECT_DIR/$LABEL.plist" "$TARGET"
# plutil -replace on an array index inserts instead of replacing, so remove the placeholder first.
plutil -remove ProgramArguments.1 "$TARGET"
plutil -insert ProgramArguments.1 -string "$PROJECT_DIR/launch_organizer.sh" "$TARGET"
plutil -remove WatchPaths.0 "$TARGET"
plutil -insert WatchPaths.0 -string "$DOWNLOADS_PATH" "$TARGET"
plutil -replace EnvironmentVariables.HOME -string "$HOME" "$TARGET"
plutil -lint "$TARGET"

launchctl unload "$TARGET" 2>/dev/null || true
launchctl load "$TARGET"
echo "Installed and loaded $TARGET"
