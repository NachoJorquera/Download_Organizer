import os
import re
from shutil import move
from config import CATEGORIES

DOWNLOADS_PATH = "/Users/ignaciojorquera/Downloads"

def create_folders():
    # Crea una carpeta para cada categoría si no existe.
    for folder in CATEGORIES.keys():
        folder_path = os.path.join(DOWNLOADS_PATH, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

def is_screenshot(filename):
    # Revisa si el archivo .png es un screenshot basado en el patrón de nombre de macOS.
    pattern = r"^Screenshot \d{4}-\d{2}-\d{2} at \d{2}\.\d{2}\.\d{2}\.png$"
    return re.match(pattern, filename) is not None

def organize_files():
    # Revisa y organiza los archivos en la carpeta Descargas.
    for filename in os.listdir(DOWNLOADS_PATH):
        source = os.path.join(DOWNLOADS_PATH, filename)

        if os.path.isdir(source):
            continue

        # Determina la carpeta dependiendo de la extensión o si es un screenshot
        destination_folder = None
        # Revisión si es un screenshot o no
        if filename.endswith(".png") and is_screenshot(filename):
            destination_folder = "Screenshots"
        else:
            for folder, extensions in CATEGORIES.items():
                if any(filename.lower().endswith(ext.lower()) for ext in extensions):
                    destination_folder = folder
                    break

        # Mueve el archivo a la carpeta correspondiente
        if destination_folder:
            destination = os.path.join(DOWNLOADS_PATH, destination_folder, filename)
            move(source, destination)

if __name__ == "__main__":
    create_folders()
    organize_files()