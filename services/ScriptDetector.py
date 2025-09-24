from services.logger import Logger
from bs4 import BeautifulSoup


class CategoryDetector:
    def __init__(self, db):
        self.db = db
        self.logger = Logger()

    def detect_scripts(self, soup: BeautifulSoup):
        scripts = soup.find_all("script", src=True)

        for script in scripts:
            src = script["src"]

            if "google-analytics.com" in src:
                self.logger.log("Google Analytics (analytics.js) detected", log_level=2)
                return True

            if "googletagmanager.com/gtag/js" in src:
                self.logger.log("Google Analytics (gtag.js / GA4) detected", log_level=2)
                return True

        inline_scripts = soup.find_all("script", src=False)
        for script in inline_scripts:
            if script.string and "gtag(" in script.string:
                self.logger.log("Google Analytics inline gtag detected", log_level=2)
                return True
            if script.string and "ga(" in script.string:
                self.logger.log("Google Analytics inline ga detected", log_level=2)
                return True

        return False

