import sqlite3

from db import CURSOR

connection = sqlite3.connect('your_database.db')
CURSOR = connection.cursor()

class Review:
    CURSOR = CURSOR  # Assign the actual cursor here
  # Set your database cursor here

    @classmethod
    def create_table(cls):
        cls.CURSOR.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY,
                year INTEGER,
                summary TEXT,
                employee_id INTEGER,
                FOREIGN KEY (employee_id) REFERENCES employees(id)
            )
        """)
        cls.CURSOR.connection.commit()


    @classmethod
    def create(cls, year, summary, employee_id):
        """Insert a new review into the database."""
        cls.CURSOR.execute("""
            INSERT INTO reviews (year, summary, employee_id)
            VALUES (?, ?, ?)
        """, (year, summary, employee_id))
        cls.CURSOR.connection.commit()
