import unittest

from download_organizer import SCREENSHOT_RE


# Run with: python3 -m unittest
class ScreenshotNameTest(unittest.TestCase):
    def test_matches_spanish_macos_screenshot(self):
        self.assertIsNotNone(
            SCREENSHOT_RE.match("Captura de pantalla 2026-11-12 a la(s) 07.59.34.png")
        )

    def test_matches_english_macos_screenshot(self):
        self.assertIsNotNone(SCREENSHOT_RE.match("Screenshot 2026-10-26 at 19.15.08.png"))


if __name__ == "__main__":
    unittest.main()
