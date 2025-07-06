### Selected List Class
### Used to store a list of selected Entry objects. Can perform actions on selected Entry objects such as deleting or exporting.

import os
import sqlite3
from .helper import Helper

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
    # NOTE: CSV FORMAT: is term;definition;tags\n and each exported file will have a unique name.
    def exportToAnki(self,
                     filePath: str,
                     fileName: str = None):
        if fileName is None:
            fullPathCheck = os.path.join(filePath, "Lexes-Anki.csv")
            if os.path.exists(fullPathCheck): # "Lexes-Anki.csv" exists
                copy = 2
                while os.path.exists(os.path.join(filePath, f"Lexes-Anki-{copy}.csv")): # iterates through potential duplicate file names until one is free
                    copy += 1
                fileName = f"Lexes-Anki-{copy}.csv" # ensures unique file names
            else:
                fileName = "Lexes-Anki.csv" # if no copies exist

        elif os.path.exists(os.path.join(filePath, fileName)): # "fileName(.csv)" exists
            baseFileName = fileName[:-4] if fileName.endswith(".csv") else fileName # removes .csv if present
            copy = 2
            while os.path.exists(os.path.join(filePath, f"{baseFileName}-{copy}.csv")): # iterates through potential duplicate file names until one is free
                copy += 1
            fileName = f"{baseFileName}-{copy}.csv"

        fullPath = os.path.join(filePath, fileName)

        entriesToExport = self.entries.copy() # mutable argument solution
        entriesToExport = Helper.quickSort(entriesToExport, "dateAscending")
        
        with open(fullPath, mode="w", encoding="utf-8") as csvFile:
            csvFile.write("term;definition;tags\n")

            for entry in entriesToExport:
                term = entry.term.replace(";", ",") # replaces semi-colons with commas to avoid breakign the CSV delimiter
                definition = entry.definition.replace(";", ",")
                tags = entry.tags.replace(";", ",")
                row = f"{term};{definition};{tags}\n"
                csvFile.write(row)

    # Creates a new DB at location and writes entry info to rows.
    # NOTE: exported .db table has same format as original .db table, but uid and createdAt columns are left blank for re-creation upon import.
    def exportToDB(self,
                   filePath: str,
                   fileName: str = None):
        if fileName is None:
            fullPathCheck = os.path.join(filePath, "Lexes-Export.db")
            if os.path.exists(fullPathCheck):
                copy = 2
                while os.path.exists(os.path.join(filePath, f"Lexes-Export-{copy}.db")):
                    copy += 1
                fileName = f"Lexes-Export-{copy}.db"
            else:
                fileName = "Lexes-Export.db"

        elif os.path.exists(os.path.join(filePath, fileName)):
            baseFileName = fileName[:-3] if fileName.endswith(".db") else fileName
            copy = 2
            while os.path.exists(os.path.join(filePath, f"{baseFileName}-{copy}.db")):
                copy += 1
            fileName = f"{baseFileName}-{copy}.db"

        fullPath = os.path.join(filePath, fileName)

        entriesToExport = self.entries.copy() # mutable argument solution
        entriesToExport = Helper.quickSort(entriesToExport, "dateAscending")

        conn = sqlite3.connect(fullPath)
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
            cursor.execute("INSERT INTO master (term, definition, tags) VALUES (?, ?, ?)",
                           (entry.term, entry.definition, entry.tags.strip()))

        conn.commit()
        conn.close()
