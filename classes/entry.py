"""
File: classes/entry.py

Purpose:
    Defines the Entry class, which represents a single entry (row) in the Lexes app.
    Entry objects hold uid, term, definition, tags, and creation datetime.
    A single Entry instance is responsible for managing the attributes of a single entry.
    Each Entry object has methods for database operations like add, edit, delete, select and automatic definition generation (retrieval).

Contains:
    - Entry class with methods to manage a single entry.
    - Methods for database interaction: adding, editing, deleting.
    - Methods for utility: selecting, unselecting, and automatic definition generation.

Naming Conventions:
    - Class names are in PascalCase (Entry).
    - Method names are in camelCase (add, edit, delete, select, unselect, autoGenerate).
    - Attributes are in camelCase (uid, term, definition, tags, createdAt).
    - Constants are in UPPERCASE (DBPATH).
    - General code follows camelCase.
"""

### Module Imports ###
import sqlite3
import datetime

### Local Class Imports ###
from .helper import Helper
from config.configurations import DBPATH # Constant path to the database file
from .selected_list import SelectedList

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
        if createdAt is None: # mutable argument solution, creates timestamp in __init__ instead of when object is constructed.
            self.createdAt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            self.createdAt = createdAt
    
    # Custom representation of what the entry object looks like when printed.
    def __repr__(self) -> str:
        return f"Entry(uid={self.uid}, term={self.term}, definition={self.definition}, tags={self.tags}, createdAt={self.createdAt})"

    # Pushes entry into DB.
    def add(self) -> None:
        with sqlite3.connect(DBPATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO master (term, definition, tags, createdAt) VALUES (?, ?, ?, ?)",
                (self.term, self.definition, self.tags.strip(), self.createdAt)
            )
            conn.commit()


    # Updates entry attributes then updates row in DB where uid matches.
    def edit(self, newTerm: str, newDefinition: str, newTags: str) -> None:
        self.term = newTerm
        self.definition = newDefinition
        self.tags = newTags
        uid = self.uid

        with sqlite3.connect(DBPATH) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE master SET term = ?, definition = ?, tags = ? WHERE uid = ?",
                        (self.term, self.definition, self.tags.strip(), uid))
            conn.commit()

    # Deletes row in DB with matching uid.
    # NOTE: Does not need to remove from displayList and selectedList to separate functionality from UI. (Button functions will manage this.)
    # NOTE: Only removes from DB, doesn't "delete" the object. Once object is no longer referenced, it will be garbage collected.
    def delete(self) -> None:
        uid = self.uid

        with sqlite3.connect(DBPATH) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM master WHERE uid = ?",
                        (uid,))
            conn.commit()
    
    # Retrieves definition from Wikipedia API using helper function, then returns string as string.
    def autoGenerate(self) -> str:
        retrievedDefinition = Helper.wikipediaAPI(self.term)
        return retrievedDefinition if retrievedDefinition is not None else ""

    # Adds entry to selectedList if not in it.
    # NOTE: SelectedList object must be passed as parameter.
    def select(self, selectedList: SelectedList) -> None:
        if self not in selectedList.entries:
            selectedList.entries.append(self)

    # Deletes entry from selectedList if in it.
    # NOTE: SelectedList object must be passed as parameter.
    def unselect(self, selectedList: SelectedList) -> None:
        if self in selectedList.entries:
            selectedList.entries.remove(self)
