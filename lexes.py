### Program: Lexes
### Author: Alexander Ho (ho-0084@mhs.vic.edu.au)
### Date Created: 25/06/2025
### Date Finished: TBA  
### Description: Personal dictionary and flashcard creation solution for students. Created for VCE Software Development 3&4 SAT.

import sqlite3
import customtkinter as ctk
from tkinter import messagebox
import datetime
import os

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
            
    def add():
        pass

    def edit():
        pass

    def delete():
        pass

    def autoGenerate():
        pass

    def select():
        pass

    def unselect():
        pass

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

        conn.close()
    
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


App(dbPath=r"assets\lexes.db")
        