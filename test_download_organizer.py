import os
import tempfile
import unittest
from unittest import mock

import download_organizer
from config import CATEGORIES
from download_organizer import SCREENSHOT_RE


# Run with: python3 -m unittest
class ScreenshotNameTest(unittest.TestCase):
    def test_matches_spanish_macos_screenshot(self):
        self.assertIsNotNone(
            SCREENSHOT_RE.match("Captura de pantalla 2026-11-12 a la(s) 07.59.34.png")
        )

    def test_matches_english_macos_screenshot(self):
        self.assertIsNotNone(SCREENSHOT_RE.match("Screenshot 2026-10-26 at 19.15.08.png"))

    # Times as macOS formats them on a 12-hour clock (en_US, en_GB, es_419, es_ES).
    def test_matches_12_hour_clock_screenshots(self):
        for name in (
            "Screenshot 2026-11-12 at 7.05.03\u202fPM.png",
            "Screenshot 2026-11-12 at 7.05.03\u202fpm.png",
            "Captura de pantalla 2026-11-12 a la(s) 7.05.03\u202fp.m..png",
            "Captura de pantalla 2026-11-12 a la(s) 7.05.03\u202fp.\u202fm. 2.png",
        ):
            with self.subTest(name=name):
                self.assertIsNotNone(SCREENSHOT_RE.match(name))


# Each test runs organize_files against an empty temp folder, never the real Downloads.
class OrganizeFilesTest(unittest.TestCase):
    def setUp(self):
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        self.downloads = temp_dir.name
        patcher = mock.patch.object(download_organizer, "DOWNLOADS_PATH", self.downloads)
        patcher.start()
        self.addCleanup(patcher.stop)

    def path(self, *parts):
        return os.path.join(self.downloads, *parts)

    def organize(self, *filenames):
        for filename in filenames:
            open(self.path(filename), "w").close()
        download_organizer.create_folders()
        download_organizer.organize_files()

    def test_each_configured_extension_lands_in_its_folder(self):
        expected = {
            f"sample{extension.lower()}": folder
            for folder, extensions in CATEGORIES.items()
            for extension in extensions
        }
        self.organize(*expected)
        for filename, folder in expected.items():
            with self.subTest(filename=filename, folder=folder):
                self.assertTrue(os.path.exists(self.path(folder, filename)))

    def test_macos_screenshot_goes_to_screenshots(self):
        name = "Captura de pantalla 2026-11-12 a la(s) 07.59.34.png"
        self.organize(name)
        self.assertTrue(os.path.exists(self.path("Screenshots", name)))

    def test_png_that_only_resembles_a_screenshot_goes_to_images(self):
        name = "Screenshot of my app.png"
        self.organize(name)
        self.assertTrue(os.path.exists(self.path("Images", name)))

    def test_name_collision_gets_numeric_suffix(self):
        os.makedirs(self.path("Documents/PDFs"))
        with open(self.path("Documents/PDFs", "report.pdf"), "w") as existing:
            existing.write("old")
        self.organize("report.pdf")
        self.assertTrue(os.path.exists(self.path("Documents/PDFs", "report (1).pdf")))
        with open(self.path("Documents/PDFs", "report.pdf")) as existing:
            self.assertEqual(existing.read(), "old")

    def test_ignored_entries_stay_in_root(self):
        os.makedirs(self.path("backup.zip"))
        self.organize(".hidden.pdf", "notes.xyz")
        for name in (".hidden.pdf", "notes.xyz", "backup.zip"):
            with self.subTest(name=name):
                self.assertTrue(os.path.exists(self.path(name)))


if __name__ == "__main__":
    unittest.main()
