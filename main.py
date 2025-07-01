### Program: Lexes
### Author: Alexander Ho (ho-0084@mhs.vic.edu.au)
### Date Created: 25/06/2025
### Date Finished: TBA  
### Description: Personal dictionary and flashcard creation solution for students. Created for VCE Software Development 3&4 SAT.

# Temporary Imports
import sqlite3
from config.database import dbPath

# Class Imports
from app.app import App

# Testing
if __name__ == "__main__":
    app = App()
    
    # entry4 = Entry(term="Entry 4", definition="Test entry number 4", tags="test a")
    # entry4.add()
    # time.sleep(5)
    # entry5 = Entry(term="Entry 5", definition="Test entry number 5", tags="test a")
    # entry5.add()
    conn = sqlite3.connect(dbPath)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM master")
    print(cursor.fetchall())
    conn.close()
