import time
import requests
import re
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

    def extract_emails_from_soup(self, soup):
        """Extraheert email adressen uit BeautifulSoup object"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        text = soup.get_text()
        emails = re.findall(email_pattern, text)
        
        # Ook zoeken in href attributes van mailto links
        mailto_links = soup.find_all('a', href=re.compile(r'^mailto:', re.I))
        for link in mailto_links:
            href = link.get('href', '')
            if href.startswith('mailto:'):
                email = href[7:].split('?')[0]  # Remove mailto: prefix and query parameters
                if re.match(email_pattern, email):
                    emails.append(email)
        
        # Duplicaten verwijderen en lijst terugsturen
        return list(set(emails))


    def define_category_for_link(self, url):
        try:
            res = requests.get(url, timeout=5)
            if res.status_code != 200:
                self.logger.log(f"Error getting page to define a category {url}", log_level=3)
                return "ERROR", None, []
            soup = BeautifulSoup(res.content, "html.parser")
            title = str(soup.title.string) if soup.title else "No Title"
            category = self.categorize_from_soup(soup)
            emails = self.extract_emails_from_soup(soup)
            
            self.logger.log(f"Found category: {category} in {url}", log_level=2)
            if emails:
                self.logger.log(f"Found {len(emails)} emails in {url}", log_level=2)
            
            return category, title, emails

        except Exception as e:
            self.logger.log(f"Failed to fetch {url} ({e})", log_level=3)
            return "ERROR", None, []

    def is_external(self, url):
        domain = urlparse(url).netloc
        return domain and domain != self.base_domain

    def scrape(self):
        res = requests.get(self.start_url)
        if res.status_code != 200:
            # self.logger.log(f"Error code: {res.status_code}", log_level=3)
            # return
            if res.status_code == 404:
                self.logger.log(f"Error 404: {res.status_code}", log_level=3)
            elif res.status_code == 500:
                self.logger.log(f"Error 500: {res.status_code}", log_level=3)

        self.logger.log(f"Request successful (Status Code {res.status_code})")
        soup = BeautifulSoup(res.content, "html.parser")
        self.logger.log(f"Succesfully scraped HTML of {self.start_url}")

        main_title = str(soup.title.string) if soup.title else "No Title"
        self.logger.log(f"Page title: {main_title}")

        main_category = self.categorize_from_soup(soup)
        self.logger.log(f"Main category: {main_category}")

        # Email adressen extraheren van de hoofdpagina
        main_emails = self.extract_emails_from_soup(soup)
        self.logger.log(f"Found {len(main_emails)} emails on main page")
        
        # Emails opslaan met category
        for email in main_emails:
            self.db.save_email(email, main_category)
            self.logger.log(f"Saved email: {email} with category: {main_category}")

        unique_links = {a["href"] for a in soup.find_all("a", href=True)}
        self.logger.log(f"Found {len(unique_links)} unique links")

        main_url_id = self.db.add_link_with_category(self.start_url, main_category)
        if main_url_id:
            self.db.save_url_title(main_url_id, main_title)

        for l in unique_links:
            abs_link = urljoin(self.start_url, l)
            if self.is_external(abs_link):
                category, title, emails = self.define_category_for_link(abs_link)
                
                # Emails opslaan voor externe links
                for email in emails:
                    self.db.save_email(email, category)
                    self.logger.log(f"Saved email: {email} with category: {category}")
                
                time.sleep(1)
            else:
                category = main_category
                title = "Internal Link - No Title"

            link_id = self.db.add_link_with_category(abs_link, category)
            if link_id and title:
                self.db.save_url_title(link_id, title)



