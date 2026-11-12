import logging
import os
import re
import sys
from shutil import move
from config import CATEGORIES, TEMP_EXTENSIONS

DOWNLOADS_PATH = os.path.expanduser(os.environ.get("DOWNLOADS_PATH", "~/Downloads"))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger(__name__)

# Pre-compiled regex for macOS screenshot filenames in English and Spanish.
# Covers: "Screenshot 2024-01-15 at 10.30.00.png",
# "Captura de pantalla 2024-01-15 a la(s) 10.30.00.png"
# and duplicates of both: "... 10.30.00 2.png"
SCREENSHOT_RE = re.compile(
    r"^(?:Screenshot|Captura de pantalla) \d{4}-\d{2}-\d{2} (?:at|a la\(s\)) "
    r"\d{2}\.\d{2}\.\d{2}(?: \d+)?\.png$"
)

# Build a lookup dict {".pdf": "Documents", ".zip": "Archives", ...}
# so extension matching is O(1) instead of O(categories × extensions).
EXTENSION_MAP: dict[str, str] = {}
for _folder, _extensions in CATEGORIES.items():
    for _ext in _extensions:
        EXTENSION_MAP.setdefault(_ext.lower(), _folder)


def create_folders():
    """Create a subfolder for each category and Screenshots if it doesn't exist."""
    for folder in list(CATEGORIES.keys()) + ["Screenshots"]:
        folder_path = os.path.join(DOWNLOADS_PATH, folder)
        try:
            os.makedirs(folder_path, exist_ok=True)
        except PermissionError:
            log.error("Permission denied creating folder: %s", folder_path)
        except Exception:
            log.exception("Unexpected error creating folder: %s", folder_path)


def resolve_destination(directory: str, filename: str) -> str:
    """Return a path in *directory* for *filename*, adding a numeric suffix on collision."""
    destination = os.path.join(directory, filename)
    if not os.path.exists(destination):
        return destination

    name, ext = os.path.splitext(filename)
    counter = 1
    while True:
        destination = os.path.join(directory, f"{name} ({counter}){ext}")
        if not os.path.exists(destination):
            return destination
        counter += 1


def organize_files():
    """Scan Downloads and move each file into its matching category folder."""
    try:
        entries = os.listdir(DOWNLOADS_PATH)
    except (PermissionError, FileNotFoundError):
        log.exception("Cannot list downloads directory: %s", DOWNLOADS_PATH)
        sys.exit(1)

    for filename in entries:
        # Skip dotfiles (.DS_Store, .localized, etc.)
        if filename.startswith("."):
            continue

        source = os.path.join(DOWNLOADS_PATH, filename)

        if os.path.isdir(source):
            continue

        # Skip incomplete browser downloads
        ext_lower = os.path.splitext(filename)[1].lower()
        if ext_lower in TEMP_EXTENSIONS:
            continue

        # Determine destination folder
        if filename.endswith(".png") and SCREENSHOT_RE.match(filename):
            destination_folder = "Screenshots"
        else:
            destination_folder = EXTENSION_MAP.get(ext_lower)

        if destination_folder is None:
            continue

        destination = resolve_destination(
            os.path.join(DOWNLOADS_PATH, destination_folder), filename
        )
        try:
            move(source, destination)
            log.info("Moved: %s -> %s/", filename, destination_folder)
        except PermissionError:
            log.error("Permission denied moving: %s", filename)
        except Exception:
            log.exception("Failed to move: %s", filename)


if __name__ == "__main__":
    create_folders()
    organize_files()
