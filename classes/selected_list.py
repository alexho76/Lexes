### Selected List Class
### Used to store a list of selected Entry objects. Can perform actions on selected Entry objects such as deleting or exporting.

import os
import sqlite3
from .helper import Helper
import csv

class SelectedList:
    def __init__(self,
                 entries: list = None):
        self.entries = entries if entries is not None else [] # mutable argument solution
    
    # NOTE: Takes selectedList object as parameter.
    def unselectAll(self,
                    selectedList: 'SelectedList'):
        for entry in self.entries:
            entry.unselect(selectedList)

    # Deletes all selected entries from DB. Clears selectedList.entries afterwards as delete() doesn't 'remove' object itself. 
    def deleteAll(self):
        for entry in self.entries:
            entry.delete()
        self.entries.clear()
    
    # Creates a new CSV at location and writes entry info to rows.
    # NOTE: CSV FORMAT: is term;definition;tags\n
    def exportToAnki(self,
                     filePath: str,
                     includeTags: bool = True):
        fullPath = filePath

        entriesToExport = self.entries.copy() # mutable argument solution
        entriesToExport = Helper.quickSort(entriesToExport, "dateDescending")
        
        with open(fullPath, mode="w", encoding="utf-8", newline="") as csvFile:
            writer = csv.writer(csvFile, delimiter=';', quoting=csv.QUOTE_MINIMAL) # uses csv library to write

            for entry in entriesToExport:
                term = entry.term.replace(";", ",") # replaces semi-colons with commas to avoid breakign the CSV delimiter
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
                   includeTags: bool = True):
        fullPath = filePath

        entriesToExport = self.entries.copy() # mutable argument solution
        entriesToExport = Helper.quickSort(entriesToExport, "dateAscending")

        with sqlite3.connect(fullPath) as conn:
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS master (
                uid INTEGER PRIMARY KEY AUTOINCREMENT,
                term TEXT NOT NULL,
                definition TEXT NOT NULL,
                tags TEXT,
                createdAt TEXT NOT NULL)
            """)

            for entry in entriesToExport: # exclude uid and createdAt, uses values straight from entry object, not from DB
                if includeTags:
                    tags = entry.tags.strip()
                else:
                    tags = ""
                createdAt = ""
                
                cursor.execute("INSERT INTO master (term, definition, tags, createdAt) VALUES (?, ?, ?, ?)",
                            (entry.term, entry.definition, tags, createdAt))

            conn.commit()
