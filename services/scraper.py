import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from services.logger import Logger
from services.database import Database
from services.CategoryDetector import CategoryDetector

class Scraper:
    def __init__(self, start_url, db_config):
        self.start_url = start_url
        self.base_domain = urlparse(start_url).netloc
        self.logger = Logger()
        self.db = Database(db_config)
        self.detector = CategoryDetector(self.db)

    def categorize_from_soup(self, soup):
        return self.detector.detect(soup)


    def define_category_for_link(self, url):
        try:
            res = requests.get(url, timeout=5)
            if res.status_code != 200:
                self.logger.log(f"Error getting page to define a category {url}", log_level=3)
                return "ERROR", None
            soup = BeautifulSoup(res.content, "html.parser")
            title = str(soup.title.string) if soup.title else "No Title"
            self.logger.log(f"Found category: {self.categorize_from_soup(soup)} in {url}", log_level=2)
            return self.categorize_from_soup(soup), title


        except Exception as e:
            self.logger.log(f"Failed to fetch {url} ({e})", log_level=3)
            return "ERROR", None

    def is_external(self, url):
        domain = urlparse(url).netloc
        return domain and domain != self.base_domain

    def scrape(self):
        res = requests.get(self.start_url)
        if res.status_code != 200:
            self.logger.log(f"Error code: {res.status_code}", log_level=3)
            return

        self.logger.log(f"Request successful (Status Code {res.status_code})")
        soup = BeautifulSoup(res.content, "html.parser")
        self.logger.log(f"Succesfully scraped HTML of {self.start_url}")

        main_title = str(soup.title.string) if soup.title else "No Title"
        self.logger.log(f"Page title: {main_title}")

        main_category = self.categorize_from_soup(soup)
        self.logger.log(f"Main category: {main_category}")

        unique_links = {a["href"] for a in soup.find_all("a", href=True)}
        self.logger.log(f"Found {len(unique_links)} unique links")

        main_url_id = self.db.add_link_with_category(self.start_url, main_category)
        if main_url_id:
            self.db.save_url_title(main_url_id, main_title)

        for l in unique_links:
            abs_link = urljoin(self.start_url, l)
            if self.is_external(abs_link):
                category, title = self.define_category_for_link(abs_link)
                time.sleep(1)
            else:
                category = main_category
                title = "Internal Link - No Title"

            link_id = self.db.add_link_with_category(abs_link, category)
            if link_id and title:
                self.db.save_url_title(link_id, title)

