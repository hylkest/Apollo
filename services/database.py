import mysql.connector

class Database:
    def __init__(self, config):
        self.config = config

    def add_link_with_category(self, url, category):
        conn = mysql.connector.connect(**self.config)
        cursor = conn.cursor()
        sql = "INSERT IGNORE INTO links (url, category) VALUES (%s, %s)"
        cursor.execute(sql, (url, category))
        conn.commit()
        cursor.close()
        conn.close()

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
        cursor.execute(sql, category)
        all_categories = cursor.fetchall()
        return all_categories

    def add_category(self, category):
        conn = mysql.connector.connect(**self.config)
        cursor = conn.cursor()
        sql = "INSERT INTO categories (category_name) VALUES (%s)"
        cursor.execute(sql, category)
        conn.commit()
        cursor.close()
        conn.close()
