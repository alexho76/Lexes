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
    - Class names: PascalCase (Entry).
    - Method names: camelCase (add, edit, delete, select, unselect, autoGenerate).
    - Attributes: camelCase (uid, term, definition, tags, createdAt).
    - Constants: UPPERCASE (DBPATH).
    - General code: camelCase.
"""

### Module Imports ###
import sqlite3
import datetime

### Local Class Imports ###
from .helper import Helper
from config.configurations import DBPATH # Constant path to the database file
from .selected_list import SelectedList

### CONSTANT CHARACTER LIMITS ###
TERM_MAX_CHAR = 500
DEFINITION_MAX_CHAR = 5000
TAGS_MAX_CHAR = 1000

def _char_limit_warn(field_name, original_text, max_len) -> None:
    """
    Private Method

    Checks if the length of the original text exceeds the maximum allowed length for a field.
    If it does, prints a warning message indicating the field name and the maximum length.
    - field_name (str): The name of the field being checked. String as it represents whether the field is a term, definition, or tags.
    - original_text (str): The original text to check. String as it represents the textually inputted original text.
    - max_len (int): The maximum allowed length for the field. Integer as it represents the maximum number of characters allowed.
    """
    if len(original_text) > max_len:
        print(f"Warning: {field_name.capitalize()} exceeds {max_len} characters. {field_name.capitalize()} will be truncated.")

class Entry:
    def __init__(self,
                 term: str,
                 definition: str,
                 tags: str = "",
                 createdAt: str = None,
                 uid: int = None):
        """
        Initiates the Entry with its attributes: uid and createdAt are optional parameters. Auto-generates timestamp.
        - term (str): term of the entry (word or phrase). String as it represents the textually inputted term.
        - definition (str): Definition of the entry (meaning or explanation). String as it represents the textually inputted definition.
        - tags (str): Tags associated with the entry, can be empty. String as it represents the textually inputted series of tags.
        - createdAt (str): Creation timestamp of the entry. String as it represents the textually inputted creation timestamp.
        """
        ### Range check for term, definition, tags length ###
        _char_limit_warn("term", term, TERM_MAX_CHAR)
        _char_limit_warn("definition", definition, DEFINITION_MAX_CHAR)
        _char_limit_warn("tags", tags, TAGS_MAX_CHAR)

        self.uid = uid # unique identifier for the entry, optional for new entries
        self.term = term[:TERM_MAX_CHAR]  # term of the entry, truncated to max length
        self.definition = definition[:DEFINITION_MAX_CHAR]
        self.tags = tags[:TAGS_MAX_CHAR]
        if createdAt is None: # mutable argument solution, creates timestamp in __init__ instead of when object is constructed.
            self.createdAt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            self.createdAt = createdAt
    
    def __repr__(self) -> str:
        """
        Custom representation of what the entry object looks like when printed. Returns a string representation of the entry.
        """
        return f"Entry(uid={self.uid}, term={self.term}, definition={self.definition}, tags={self.tags}, createdAt={self.createdAt})"

    def add(self) -> None:
        """
        Adds the entry to the database.
        """
        with sqlite3.connect(DBPATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO master (term, definition, tags, createdAt) VALUES (?, ?, ?, ?)",
                (self.term, self.definition, self.tags.strip(), self.createdAt)
            )
            conn.commit()

    def edit(self, newTerm: str, newDefinition: str, newTags: str) -> None:
        """
        Updates entry attributes then updates row in DB where uid matches.
        - newTerm (str): The new term for the entry. String as it represents the textually inputted new term.
        - newDefinition (str): The new definition for the entry. String as it represents the textually inputted new definition.
        - newTags (str): The new tags for the entry. String as it represents the textually inputted new series of tags.
        """
        ### Range check for newTerm, newDefinition, newTags length ###
        _char_limit_warn("term", newTerm, TERM_MAX_CHAR)
        _char_limit_warn("definition", newDefinition, DEFINITION_MAX_CHAR)
        _char_limit_warn("tags", newTags, TAGS_MAX_CHAR)

        self.term = newTerm[:TERM_MAX_CHAR]  # update term, truncated to max length
        self.definition = newDefinition[:DEFINITION_MAX_CHAR] # update definition, truncated to max length
        self.tags = newTags[:TAGS_MAX_CHAR] # update tags, truncated to max length
        uid = self.uid

        with sqlite3.connect(DBPATH) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE master SET term = ?, definition = ?, tags = ? WHERE uid = ?",
                        (self.term, self.definition, self.tags.strip(), uid))
            conn.commit()

    def delete(self) -> None:
        """
        Deletes row in DB with matching uid.
        Does not need to remove from displayList and selectedList to separate functionality from UI (Button functions will manage this).
        Only removes from DB, doesn't "delete" the object. Once object is no longer referenced, it will be garbage collected.
        """
        uid = self.uid

        with sqlite3.connect(DBPATH) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM master WHERE uid = ?",
                        (uid,))
            conn.commit()
    
    def autoGenerate(self) -> str:
        """
        Retrieves definition from Wikipedia API using helper function. Returns retrieved definition as string or empty string if not found.
        """
        retrievedDefinition = Helper.wikipediaAPI(self.term)
        return retrievedDefinition if retrievedDefinition is not None else ""

    def select(self, selectedList: SelectedList) -> None:
        """
        Adds entry to selectedList if not in it.
        - selectedList (SelectedList): The list to add selected entries to. SelectedList to hold all selected entries.
        """
        if self not in selectedList.entries:
            selectedList.entries.append(self)

    def unselect(self, selectedList: SelectedList) -> None:
        """
        Deletes entry from selectedList if in it.
        - selectedList (SelectedList): The list to remove unselected entries from. SelectedList to hold all selected entries.
        """
        if self in selectedList.entries:
            selectedList.entries.remove(self)