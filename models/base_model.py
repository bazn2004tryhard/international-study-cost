# models/base_model.py
import mysql.connector
from mysql.connector import Error
from config.db_config import DB_CONFIG


class BaseModel:
    def __init__(self):
        self.connection = None

    def connect(self):
        if self.connection is None or not self.connection.is_connected():
            self.connection = mysql.connector.connect(**DB_CONFIG)
        return self.connection

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            self.connection = None

    def execute_query(self, query, params=None, fetchone=False, fetchall=False):
        """
        Dùng cho SELECT. Trả về dict hoặc list[dict]
        """
        conn = self.connect()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        result = None

        if fetchone:
            result = cursor.fetchone()
        elif fetchall:
            result = cursor.fetchall()

        cursor.close()
        return result

    def execute_non_query(self, query, params=None):
        """
        Dùng cho INSERT / UPDATE / DELETE.
        Trả về số dòng bị ảnh hưởng.
        """
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        conn.commit()
        affected = cursor.rowcount
        cursor.close()
        return affected

    def execute_insert(self, query, params=None):
        """
        Dùng cho INSERT cần lấy lastrowid.
        """
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        conn.commit()
        last_id = cursor.lastrowid
        cursor.close()
        return last_id
