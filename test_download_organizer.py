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

    # Times as macOS formats them on a 12-hour clock (en_US, en_GB, es_419, es_ES).
    def test_matches_12_hour_clock_screenshots(self):
        for name in (
            "Screenshot 2026-11-12 at 7.05.03 PM.png",
            "Screenshot 2026-11-12 at 7.05.03 pm.png",
            "Captura de pantalla 2026-11-12 a la(s) 7.05.03 p.m..png",
            "Captura de pantalla 2026-11-12 a la(s) 7.05.03 p. m. 2.png",
        ):
            with self.subTest(name=name):
                self.assertIsNotNone(SCREENSHOT_RE.match(name))


if __name__ == "__main__":
    unittest.main()
