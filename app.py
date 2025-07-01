# Class Imports
from config.database import dbPath
from classes.helper import Helper
from classes.entry import Entry
from classes.display_list import DisplayList
from classes.selected_list import SelectedList
from classes.import_list import ImportList

# Imports
import sqlite3

class App:

    def __init__(self):
        conn = sqlite3.connect(dbPath)
        self.setupDB()

        ####3
        newEntry = Entry(term="Last test", definition="final test to see importing module functionality", tags="code_in_app run_in_main")
        newEntry.add()

        conn = sqlite3.connect(dbPath)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM master")
        print(cursor.fetchall())
        conn.commit()
        conn.close()
        
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