"""
File: classes/selected_list.py

Purpose:
    Defines the SelectedList class, which is used to manage a list of selected Entry objects.
    Can perform actions on selected Entry objects such as unselecting, deleting, and exporting to CSV or database files.

Contains:
    - SelectedList class with methods for managing selected entries.
    - Methods:
        - unselectAll: Unselects all entries in the selected list.
        - deleteAll: Deletes all selected entries from the database and clears the selected list.
        - exportToAnki: Exports selected entries to an Anki-compatible CSV file.
        - exportToDB: Exports selected entries to a new SQLite database file.

Naming Conventions:
    - Class names: PascalCase (SelectedList).
    - Method names: camelCase (unselectAll, deleteAll, exportToAnki, exportToDB).
    - Attributes: camelCase (entries).
    - General code: camelCase.
"""

### Module Imports ###
import sqlite3
import csv

### Local Class Imports ###
from .helper import Helper

class SelectedList:
    def __init__(self,
                 entries: list = None):
        self.entries = entries if entries is not None else [] # mutable argument solution
    
    # NOTE: Takes selectedList object as parameter.
    def unselectAll(self,
                    selectedList: 'SelectedList') -> None:
        for entry in self.entries:
            entry.unselect(selectedList)

    # Deletes all selected entries from DB and clears self.entries.
    def deleteAll(self) -> None:
        for entry in self.entries:
            entry.delete()
        self.entries.clear()
    
    # Creates a new CSV at location and writes entry info to rows.
    # NOTE: ANKI FORMAT: term;definition;tags
    def exportToAnki(self,
                     filePath: str,
                     includeTags: bool = True) -> None:
        fullPath = filePath

        entriesToExport = self.entries.copy() # mutable argument solution
        entriesToExport = Helper.quickSort(entriesToExport, "dateDescending")
        
        with open(fullPath, mode="w", encoding="utf-8", newline="") as csvFile:
            writer = csv.writer(csvFile, delimiter=';', quoting=csv.QUOTE_MINIMAL) # uses csv library to write

            for entry in entriesToExport:
                term = entry.term.replace(";", ",") # replaces semi-colons with commas to avoid breaking the CSV delimiter
                definition = entry.definition.replace(";", ",")
                
                if includeTags:
                    tags = entry.tags.replace(";", ",")
                else:
                    tags = ""
                
                writer.writerow([term, definition, tags])

    # Creates a new DB at location and writes entry info to rows.
    # NOTE: exported .db table has same format as original .db table, but uid and createdAt columns are left blank for re-creation upon import.
    def exportToDB(self,
                   filePath: str,
                   includeTags: bool = True) -> None:
        fullPath = filePath

        entriesToExport = self.entries.copy() # mutable argument solution
        entriesToExport = Helper.quickSort(entriesToExport, "dateAscending")

        with sqlite3.connect(fullPath) as conn:
            cursor = conn.cursor()
            cursor.execute("DROP TABLE IF EXISTS master")  # Always recreate table with correct schema
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS master (
                uid INTEGER PRIMARY KEY AUTOINCREMENT,
                term TEXT NOT NULL,
                definition TEXT NOT NULL,
                tags TEXT)
            """)

            for entry in entriesToExport: # exclude uid and createdAt, uses values straight from entry object, not from DB
                if includeTags:
                    tags = entry.tags.strip()
                else:
                    tags = ""

                cursor.execute("INSERT INTO master (term, definition, tags) VALUES (?, ?, ?)",
                            (entry.term, entry.definition, tags))

            conn.commit()