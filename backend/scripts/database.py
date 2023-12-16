import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

class Database:
    def __init__(self, db_name):
        # self.host = os.environ.get("DB_HOST")
        # self.user = os.environ.get("DB_USER")
        # self.password = os.environ.get("DB_PASSWORD")
        self.host = "187.16.255.78"
        self.user = "thiagoj"
        self.password = "DokBr4JjjA!"
        self.db = db_name

    def connect(self):
        return mysql.connector.connect(
            host=self.host, user=self.user, password=self.password, database=self.db
        )

    def fetch(self, sql):
        conn = self.connect()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result

    def execute(self, sql):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
        return "SQL Executada com sucesso"