# Class Imports
from classes import Helper, Entry, DisplayList, SelectedList, ImportList
import sqlite3
from config.database import dbPath

class App:

    def __init__(self):
        conn = sqlite3.connect(dbPath)
        self.setupDB()
    
    # Ensures DB connection closes upon App closing.
    def __del__(self):
        conn = sqlite3.connect(dbPath)
        conn.close()
    
    def setupDB(self):
        conn = sqlite3.connect(dbPath)
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS master (
            uid INTEGER PRIMARY KEY AUTOINCREMENT,
            term TEXT NOT NULL,
            definition TEXT NOT NULL,
            tags TEXT,
            createdAt TEXT NOT NULL)
        """)
        conn.commit()
        conn.close()