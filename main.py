### Program: Lexes
### Author: Alexander Ho (ho-0084@mhs.vic.edu.au)
### Date Created: 25/06/2025
### Date Finished: TBA  
### Description: Personal dictionary and flashcard creation solution for students. Created for VCE Software Development 3&4 SAT.

import sqlite3
import customtkinter as ctk
from tkinter import messagebox
import datetime
import requests
import re
import os

class Helper:
    @staticmethod
    # Static method to call Wikipedia API, parse response, and return definition (if found).
    def wikipediaAPI(query: str) -> str:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"
        response = requests.get(url, verify = False)
        if response.status_code == 200: # successful request
            data = response.json()
            extract = data.get("extract")
            return str(extract) if extract is not None else None
        else:
            return None
    
    @staticmethod
    # Performs quicksort on entry objects based on various attributes: alphabeticalAscending, alphabeticalDescending, dateAscending, dateDescending
    # NOTE: Modified pseudocode naming to be more general.
    # Checked: I
    def quickSort(entries,attribute):
        if len(entries) <= 1:
            return entries
        pivot = entries[0]
        lesser = []
        greater = []

        for entry in entries[1:]:
            if attribute == "alphabeticalAscending":
                if entry.term < pivot.term:
                    lesser.append(entry)
                else:
                    greater.append(entry)

            elif attribute == "alphabeticalDescending":
                if entry.term > pivot.term:
                    lesser.append(entry)
                else:
                    greater.append(entry)

            elif attribute == "dateAscending":
                if entry.createdAt < pivot.createdAt:
                    lesser.append(entry)
                else:
                    greater.append(entry)

            elif attribute == "dateDescending":
                if entry.createdAt > pivot.createdAt:
                    lesser.append(entry)
                else:
                    greater.append(entry)
        
        sortedLesser = Helper.quickSort(lesser,attribute)
        sortedGreater = Helper.quickSort(greater,attribute)
        return sortedLesser + [pivot] + sortedGreater


class Entry:
    # Initiates the Entry with its attributes: uid and createdAt are optional parameters. Auto-generates timestamp.
    def __init__(self,
                 term: str,
                 definition: str,
                 tags: str = "",
                 createdAt: str = None,
                 uid: int = None):
        self.uid = uid
        self.term = term
        self.definition = definition
        self.tags = tags
        if createdAt is None: # mutable argument solution
            self.createdAt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            self.createdAt = createdAt
    
    # Custom representation of what the entry object looks like when printed.
    def __repr__(self):
        return f"Entry(uid={self.uid}, term={self.term}, definition={self.definition}, tags={self.tags}, createdAt={self.createdAt})"

    # Pushes entry into DB.
    def add(self):
        conn = sqlite3.connect(App.dbPath)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO master (term, definition, tags, createdAt) VALUES (?, ?, ?, ?)",
                       (self.term, self.definition, self.tags, self.createdAt))
        conn.commit()
        conn.close()

    # Updates entry attributes then updates row in DB where uid matches.
    def edit(self, newTerm: str, newDefinition: str, newTags: str):
        self.term = newTerm
        self.definition = newDefinition
        self.tags = newTags
        uid = self.uid

        conn = sqlite3.connect(App.dbPath)
        cursor = conn.cursor()
        cursor.execute("UPDATE master SET term = ?, definition = ?, tags = ? WHERE uid = ?",
                       (self.term, self.definition, self.tags, uid))
        conn.commit()
        conn.close()
    
    # Deletes row in DB with matching uid.
    # NOTE: Does not need to remove from displayList and selectedList to separate functionality from UI. (Button functions will manage this.)
    # NOTE: Only removes from DB, not object.
    def delete(self):
        uid = self.uid

        conn = sqlite3.connect(App.dbPath)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM master WHERE uid = ?",
                       (uid,))
        conn.commit()
        conn.close()
    
    # Retrieves definition from Wikipedia API using helper function, then returns string as string.
    def autoGenerate(self) -> str:
        retrievedDefinition = Helper.wikipediaAPI(self.term)
        return retrievedDefinition if retrievedDefinition is not None else ""

    # Adds entry to selectedList if not in it.
    # NOTE: SelectedList object must be passed as parameter.
    # Checked: I
    def select(self, selectedList: 'SelectedList'):
        if self not in selectedList.entries:
            selectedList.entries.append(self)

    # Deletes entry from selectedList if in it.
    # NOTE: SelectedList object must be passed as parameter.
    def unselect(self, selectedList: 'SelectedList'):
        if self in selectedList.entries:
            selectedList.entries.remove(self)

class DisplayList:
    # Initiation with default parameters for their respective data types and uses.
    def __init__(self,
                 entries: list = None,
                 filterTags: str = "",
                 requireAllTags: bool = False,
                 searchKeyword: str = "",
                 sortAttribute: str = "dateDescending"):
        self.entries = entries if entries is not None else [] # mutable argument solution
        self.filterTags = filterTags
        self.requireAllTags = requireAllTags
        self.searchKeyword = searchKeyword
        self.sortAttribute = sortAttribute
    
    # Out of all database entries, adds entry to displayList.entries based on filter settings (requireAllTags).
    # Checked: III
    def filter(self):
        self.entries = []
        conn = sqlite3.connect(App.dbPath)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM master")
        rows = cursor.fetchall() # all rows in db

        filterTags = [tag for tag in re.split(r"\s+", self.filterTags.strip())
                      if tag != ""] # filter tags from " a  b  c " to ["a", "b", "c"]
        
        if len(filterTags) == 0: # no tags, appends all
            for row in rows:
                entry = Entry(uid=row[0],term=row[1], definition=row[2], tags=row[3], createdAt=row[4])
                self.entries.append(entry)

        elif self.requireAllTags == True: # require all tags, appends if filterTags in row tags
            for row in rows:
                rowTags = re.split(r"\s+", row[3].strip())
                rowTags = [rowTag.lower() for rowTag in rowTags]
                if all(tag.lower() in rowTags for tag in filterTags):
                    entry = Entry(uid=row[0],term=row[1], definition=row[2], tags=row[3], createdAt=row[4])
                    self.entries.append(entry)

        elif self.requireAllTags == False: # require any tag, appends if any filterTags in row tags
            for row in rows:
                rowTags = re.split(r"\s+", row[3].strip())
                rowTags = [rowTag.lower() for rowTag in rowTags]
                if any(tag.lower() in rowTags for tag in filterTags):
                    entry = Entry(uid=row[0],term=row[1], definition=row[2], tags=row[3], createdAt=row[4])
                    self.entries.append(entry)
            
    # Removes entries from displayList.entries that do not contain searchKeyword in term or definition.
    # Checked: I
    def search(self):
        if self.searchKeyword == "":
            return

        # had to change from removing entries without keyword to rebuilding displayList.entries, due to issues with removing entries while iterating
        self.entries = [entry for entry in self.entries
                        if self.searchKeyword.lower() in entry.term.lower() or self.searchKeyword.lower() in entry.definition.lower()]

    # Uses Helper.quickSort(), assumes sortAttribute is among alphabeticalAscending, alphabeticalDescending, dateAscending, dateDescending.
    # Checked: I
    def sort(self):
        self.entries = Helper.quickSort(self.entries, self.sortAttribute)

    # NOTE: IMPORTANT ORDER: filter -> search -> sort, and self.entries is cleared in filter() not build() itself.
    # Checked: I
    def build(self):
        self.filter()
        self.search()
        self.sort()

    # NOTE: Takes selectedList object as parameter.
    # Checked: I
    def selectAll(self,
                  selectedList: 'SelectedList'):
        for entry in self.entries:
            entry.select(selectedList)

class SelectedList:
    def __init__(self,
                 entries: list = None):
        self.entries = entries if entries is not None else [] # mutable argument solution
    
    # NOTE: Takes selectedList object as parameter.
    # Checked: I
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
    # Checked: II
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

    def exportToDB(self):
        pass



class ImportList:
    def __init__(self,
                 filePath: str,
                 rawText: str = "",
                 entryDelimiter: str = "\n",
                 termDefinitionDelimiter: str = ":",
                 massTags: str = "",
                 parsedEntries: list = None):
        self.rawText = rawText
        self.entryDelimiter = entryDelimiter
        self.termDefinitionDelimiter = termDefinitionDelimiter
        self.massTags = massTags
        self.parsedEntries = parsedEntries if parsedEntries is not None else [] # mutable argument solution
        self.filePath = filePath

class App:
    dbPath = r"database\lexes.db" # default database path

    def __init__(self):
        conn = sqlite3.connect(App.dbPath)
        self.setupDB()
    
    # Ensures DB connection closes upon App closing.
    def __del__(self):
        conn = sqlite3.connect(App.dbPath)
        conn.close()
    
    def setupDB(self):
        conn = sqlite3.connect(App.dbPath)
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

# Testing
if __name__ == "__main__":
    app = App()
    
    # entry4 = Entry(term="Entry 4", definition="Test entry number 4", tags="test a")
    # entry4.add()
    # time.sleep(5)
    # entry5 = Entry(term="Entry 5", definition="Test entry number 5", tags="test a")
    # entry5.add()
    conn = sqlite3.connect(App.dbPath)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM master")
    print(cursor.fetchall())
    conn.close()
