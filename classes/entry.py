### Entry Class
### Object used to represent a row in the database. Has attributes for uid, term, definition, tags, and createdAt.

import sqlite3
from .helper import Helper
from config.configurations import dbPath
import datetime


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
        conn = sqlite3.connect(dbPath)
        cursor = conn.cursor()

        cursor.execute("INSERT INTO master (term, definition, tags, createdAt) VALUES (?, ?, ?, ?)",
                       (self.term, self.definition, self.tags.strip(), self.createdAt))
        conn.commit()
        conn.close()

    # Updates entry attributes then updates row in DB where uid matches.
    def edit(self, newTerm: str, newDefinition: str, newTags: str):
        self.term = newTerm
        self.definition = newDefinition
        self.tags = newTags
        uid = self.uid

        conn = sqlite3.connect(dbPath)
        cursor = conn.cursor()
        cursor.execute("UPDATE master SET term = ?, definition = ?, tags = ? WHERE uid = ?",
                       (self.term, self.definition, self.tags.strip(), uid))
        conn.commit()
        conn.close()
    
    # Deletes row in DB with matching uid.
    # NOTE: Does not need to remove from displayList and selectedList to separate functionality from UI. (Button functions will manage this.)
    # NOTE: Only removes from DB, not object.
    def delete(self):
        uid = self.uid

        conn = sqlite3.connect(dbPath)
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
    def select(self, selectedList):
        from .selected_list import SelectedList
        if self not in selectedList.entries:
            selectedList.entries.append(self)

    # Deletes entry from selectedList if in it.
    # NOTE: SelectedList object must be passed as parameter.
    def unselect(self, selectedList):
        from .selected_list import SelectedList
        if self in selectedList.entries:
            selectedList.entries.remove(self)
