from services.scraper import Scraper

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "selfmade"
}

if __name__ == "__main__":
    url = "https://google.nl/"
    scraper = Scraper(url, db_config)
    scraper.scrape()
