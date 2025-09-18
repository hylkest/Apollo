import re
from collections import Counter
from bs4 import BeautifulSoup
from services.logger import Logger

class CategoryDetector:
    def __init__(self, db):
        self.db = db
        self.logger = Logger()

    def detect(self, soup: BeautifulSoup) -> str:
        categories = self.db.get_all_categories()
        category_names = [c["category_name"] for c in categories]

        text = soup.get_text(separator=" ").lower()

        counts = Counter()

        for name in category_names:
            pattern = rf"\b{name.lower()}\b"
            matches = re.findall(pattern, text)
            counts[name] = len(matches)

        if not counts or counts.most_common(1)[0][1] == 0:
            return "No category"

        return counts.most_common(1)[0][0]
