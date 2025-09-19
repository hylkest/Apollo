import mysql.connector

class Database:
    def __init__(self, config):
        self.config = config

    def add_link_with_category(self, url, category):
        conn = mysql.connector.connect(**self.config)
        cursor = conn.cursor()
        sql = f"INSERT IGNORE INTO links (url, category) VALUES ({url}, {category})"
        cursor.execute(sql)
        link_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        return link_id

    def get_all_categories(self):
        conn = mysql.connector.connect(**self.config)
        cursor = conn.cursor(dictionary=True)
        sql = "SELECT * FROM categories"
        cursor.execute(sql)
        categories = cursor.fetchall()
        return categories

    def get_all_links_by_category(self, category):
        conn = mysql.connector.connect(**self.config)
        cursor = conn.cursor(dictionary=True)
        sql = f"SELECT * FROM links WHERE category = '{category}'"
        cursor.execute(sql)
        all_categories = cursor.fetchall()
        return all_categories

    def add_category(self, category):
        conn = mysql.connector.connect(**self.config)
        cursor = conn.cursor()
        sql = f"INSERT INTO categories (category_name) VALUES ({category})"
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
        
    def save_url_title(self, url_id, title):
        conn = mysql.connector.connect(**self.config)
        cursor = conn.cursor()
        sql = f"INSERT INTO url_title (url_id, url_title) VALUES ({url_id}, {title})"
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
