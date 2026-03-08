import os
import pymysql
from contextlib import contextmanager


class Database:
    def __init__(self):
        self.host = os.getenv("MYSQL_HOST", "mysql")
        self.port = int(os.getenv("MYSQL_PORT", 3306))
        self.user = os.getenv("MYSQL_USER", "registro")
        self.password = os.getenv("MYSQL_PASSWORD", "registro123")
        self.database = os.getenv("MYSQL_DB", "registro")

    @contextmanager
    def connection(self):
        conn = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True,
        )
        try:
            yield conn
        finally:
            conn.close()

    def init_schema(self):
        query = """
        CREATE TABLE IF NOT EXISTS grades (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_username VARCHAR(100) NOT NULL,
            student_name VARCHAR(100) NOT NULL,
            subject VARCHAR(100) NOT NULL,
            grade DECIMAL(4,2) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        with self.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)

    def add_grade(self, student_username: str, student_name: str, subject: str, grade: float):
        query = """
        INSERT INTO grades (student_username, student_name, subject, grade)
        VALUES (%s, %s, %s, %s)
        """
        with self.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (student_username, student_name, subject, grade))

    def get_all_grades(self):
        query = "SELECT id, student_username, student_name, subject, grade, created_at FROM grades ORDER BY created_at DESC"
        with self.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                return cur.fetchall()

    def get_grades_for_student(self, student_username: str):
        query = """
        SELECT id, student_username, student_name, subject, grade, created_at
        FROM grades
        WHERE student_username = %s
        ORDER BY created_at DESC
        """
        with self.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (student_username,))
                return cur.fetchall()
