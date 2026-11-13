# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A macOS LaunchAgent that monitors the folder in `DOWNLOADS_PATH` (default `~/Downloads`) and moves each file into a category folder based on its extension. No external dependencies: it uses only the Python 3 stdlib.

## Running and Testing

```bash
# Run manually (for testing); without .env exported it organizes ~/Downloads
python3 download_organizer.py

# Unit tests
python3 -m unittest

# Test a specific file type
touch ~/Downloads/test.pdf
# Verify it moved to ~/Downloads/Documents/PDFs/

# Check service logs (stdout has move operations, stderr has errors)
cat /tmp/com.project.organize_downloads.out
cat /tmp/com.project.organize_downloads.err
```

## LaunchAgent Management

```bash
# Install and start the service (rerun after changing .env or moving the project)
cp .env.example .env
./install.sh

# Stop/start
launchctl unload ~/Library/LaunchAgents/com.project.organize_downloads.plist
launchctl load ~/Library/LaunchAgents/com.project.organize_downloads.plist

# Check status
launchctl list | grep com.project.organize_downloads

# Validate plist syntax
plutil -lint ~/Library/LaunchAgents/com.project.organize_downloads.plist
```

## Architecture

- **`config.py`**: the `CATEGORIES` dict maps folder names to extension lists. Keys can be nested paths such as `"Codes/JSONs"`, and `create_folders` creates the parents. Each extension must appear in only one category: `EXTENSION_MAP` uses `setdefault`, so the first category listed wins and a later subfolder never receives the files. `TEMP_EXTENSIONS` lists the browser temporary file extensions to ignore. This is the only file that needs editing to add or remove categories or extensions.
- **`download_organizer.py`**: on startup, builds an `EXTENSION_MAP` (reverse lookup dict `{ext: folder}`) from `CATEGORIES` for O(1) extension matching. Creates destination folders, then iterates the files in the root of `DOWNLOADS_PATH` (never subfolders, so files already inside a category folder stay put) and moves each one. Extensions come from `os.path.splitext`, so `app.env.local` has extension `.local`. Skips dotfiles and incomplete browser downloads. Handles name collisions by appending `(1)`, `(2)`, etc. Logs all operations via Python `logging`.

**Key logic detail**: `Screenshots` is not in `CATEGORIES`; it's a special folder created alongside category folders. `.png` files are checked first against a compiled regex for macOS screenshot filenames in English (`Screenshot YYYY-MM-DD at HH.MM.SS.png`) and Spanish (`Captura de pantalla YYYY-MM-DD a la(s) HH.MM.SS.png`), on a 24h or 12h clock (`7.05.03 PM`, `7.05.03 p.m.`, with U+202F before the marker), including duplicates like `... 2.png`. Non-screenshot PNGs fall through to `Images` via the normal extension lookup.

**Trigger mechanism**: The `.plist` uses `WatchPaths` with a 5-second `ThrottleInterval` and `RunAtLoad: true`, so it organizes existing files at login and reacts to changes with debouncing.

`launch_organizer.sh` is a thin bash wrapper (with `set -e`) that changes to its own directory, exports the variables in `.env` when present, and calls `python3 download_organizer.py`.

**Configuration**: `.env` (git-ignored, created from `.env.example`) holds `DOWNLOADS_PATH`. The tracked `.plist` keeps placeholder paths (`/Users/your_user/...`); `install.sh` copies it to `~/Library/LaunchAgents/`, sets `ProgramArguments`, `WatchPaths` and `HOME` with `plutil` from `.env` and the clone's location, then reloads the agent.

## Customization

- **Add/modify categories**: Edit `CATEGORIES` in `config.py`. The extension lookup dict is built automatically.
- **Change monitored path**: Set `DOWNLOADS_PATH` in `.env`, then rerun `./install.sh`. `download_organizer.py` falls back to `~/Downloads` when the variable is unset.
- **macOS Full Disk Access required** for `/usr/bin/python3` and `/bin/bash` in System Settings → Privacy & Security.
