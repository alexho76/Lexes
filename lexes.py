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

class Helper:
    @staticmethod
    # Static method to call Wikipedia API, parse response, and return definition (if found).
    def wikipediaAPI(query: str) -> str:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"
        response = requests.get(url)
        if response.status_code == 200: # successful request
            data = response.json()
            extract = data.get("extract")
            return str(extract) if extract is not None else None
        else:
            return None


class Entry:
    # Initiates the Entry with its attributes: uid and createdAt are optional parameters.
    def __init__(self, term: str,
                 definition: str,
                 tags: str,
                 createdAt: datetime.datetime | None = None,
                 uid: int | None = None):
        self.uid = uid
        self.term = term
        self.definition = definition
        self.tags = tags
        self.createdAt = createdAt
    
    # Custom representation of what the entry object looks like when printed.
    def __repr__(self):
        return f"Entry(uid={self.uid}, term={self.term}, definition={self.definition}, tags={self.tags}, createdAt={self.createdAt})"

    # Creates timestamp of YYYY:MM:DD HH:MM:SS and pushes entry into DB
    def add(self):
        self.createdAt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        conn = sqlite3.connect(app.dbPath)
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

        conn = sqlite3.connect(app.dbPath)
        cursor = conn.cursor()
        cursor.execute("UPDATE master SET term = ?, definition = ?, tags = ? WHERE uid = ?",
                       (self.term, self.definition, self.tags, uid))
        conn.commit()
        conn.close()
    
    # Deletes row with matching uid.
    # NOTE: Does not need to remove from displayList and selectedList to separate functionality from UI. (Button functions will manage this.)
    def delete(self):
        uid = self.uid

        conn = sqlite3.connect(app.dbPath)
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
    def select(self, selectedList: 'SelectedList'):
        if self not in selectedList.entries:
            selectedList.entries.append(self)

    # Removes entry from selectedList if in it.
    # NOTE: SelectedList object must be passed as parameter.
    def unselect(self, selectedList: 'SelectedList'):
        if self in selectedList.entries:
            selectedList.entries.remove(self)

class DisplayList:
    def __init__(self, entries: list | None = None,
                 filterTags: str | None = None,
                 requireAllTags: bool | None = None,
                 searchKeyword: str | None = None,
                 sortAttribute: str | None = None):
        self.entries = entries
        self.filterTags = filterTags
        self.requireAllTags = requireAllTags
        self.searchKeyword = searchKeyword
        self.sortAttribute = sortAttribute

class SelectedList:
    def __init__(self, entries: list | None = None):
        self.entries = entries

class ImportList:
    def __init__(self, rawText: str | None = None,
                 entryDelimiter: str | None = None,
                 termDefinitionDelimiter: str | None = None,
                 massTags: str | None = None,
                 parsedEntries: list | None = None,
                 filePath: str | None = None):
        self.rawText = rawText
        self.entryDelimiter = entryDelimiter
        self.termDefinitionDelimiter = termDefinitionDelimiter
        self.massTags = massTags
        self.parsedEntries = parsedEntries
        self.filePath = filePath

class App:
    def __init__(self, dbPath: str):
        self.dbPath = dbPath
        conn = sqlite3.connect(dbPath)
        self.setupDB()
    
    def setupDB(self):
        conn = sqlite3.connect(self.dbPath)
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
    app = App(dbPath=r"assets\lexes.db")

    entry = Entry("testTerm", "testDefinition", "testTags")
    entry.add()
