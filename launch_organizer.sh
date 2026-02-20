#!/bin/bash
set -e

cd /Users/nacho/Projects/Download_Organizer || { echo "Failed to cd into project directory" >&2; exit 1; }

python3 download_organizer.py
