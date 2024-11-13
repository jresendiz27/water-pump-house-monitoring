import os
import sqlite3
from datetime import datetime


class DatabaseManager:
    def __init__(self):
        """Initialize the database connection."""
        self.db_path = os.getenv("DATABASE_PATH", "../water_pump_db.sqlite")
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        """Connect to the SQLite database."""
        if not self.connection:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row  # Allows fetching rows as dictionaries
            self.cursor = self.connection.cursor()

    def close(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None

    def execute_query(self, query, params=()):
        """Execute a query with optional parameters."""
        self.connect()
        self.cursor.execute(query, params)
        self.connection.commit()

    def fetch_one(self, query, params=()):
        """Fetch a single row from a query."""
        self.connect()
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def fetch_all(self, query, params=()):
        """Fetch all rows from a query."""
        self.connect()
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
