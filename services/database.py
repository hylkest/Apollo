import mysql.connector
from services.logger import Logger

class Database:
    def __init__(self, config):
        self.config = config
        self.logger = Logger()

    def add_link_with_category(self, url, category):
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**self.config)
            cursor = conn.cursor()
            sql = (
                "INSERT INTO links (url, category) "
                "VALUES (%s, %s) "
                "ON DUPLICATE KEY UPDATE category = VALUES(category), id = LAST_INSERT_ID(id)"
            )
            cursor.execute(sql, (url, category))
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            self.logger.log(f"DB error in add_link_with_category: {e}", log_level=3)
            return None
        finally:
            try:
                cursor.close()
            except Exception:
                pass
            try:
                conn.close()
            except Exception:
                pass

    def get_all_categories(self):
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**self.config)
            cursor = conn.cursor(dictionary=True)
            sql = "SELECT * FROM categories"
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            self.logger.log(f"DB error in get_all_categories: {e}", log_level=3)
            return []
        finally:
            try:
                cursor.close()
            except Exception:
                pass
            try:
                conn.close()
            except Exception:
                pass

    def get_all_links_by_category(self, category):
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**self.config)
            cursor = conn.cursor(dictionary=True)
            sql = "SELECT * FROM links WHERE category = %s"
            cursor.execute(sql, (category,))
            return cursor.fetchall()
        except Exception as e:
            self.logger.log(f"DB error in get_all_links_by_category: {e}", log_level=3)
            return []
        finally:
            try:
                cursor.close()
            except Exception:
                pass
            try:
                conn.close()
            except Exception:
                pass

    def add_category(self, category):
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**self.config)
            cursor = conn.cursor()
            sql = "INSERT INTO categories (category_name) VALUES (%s)"
            cursor.execute(sql, (category,))
            conn.commit()
        except Exception as e:
            self.logger.log(f"DB error in add_category: {e}", log_level=3)
        finally:
            try:
                cursor.close()
            except Exception:
                pass
            try:
                conn.close()
            except Exception:
                pass
        
    def save_url_title(self, url_id, title):
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**self.config)
            cursor = conn.cursor()
            sql = "INSERT INTO url_title (url_id, url_title) VALUES (%s, %s)"
            cursor.execute(sql, (url_id, title))
            conn.commit()
        except Exception as e:
            self.logger.log(f"DB error in save_url_title: {e}", log_level=3)
        finally:
            try:
                cursor.close()
            except Exception:
                pass
            try:
                conn.close()
            except Exception:
                pass

    def save_email(self, email, category):
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**self.config)
            cursor = conn.cursor()
            sql = "INSERT INTO url_email_address (email_address, category) VALUES (%s, %s)"
            cursor.execute(sql, (email, category))
            conn.commit()
        except Exception as e:
            self.logger.log(f"DB error in save_email: {e}", log_level=3)
        finally:
            try:
                cursor.close()
            except Exception:
                pass
            try:
                conn.close()
            except Exception:
                pass
