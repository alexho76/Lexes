"""
File: classes/display_list.py

Purpose:
    Defines the DisplayList class, which manages a list of entries displayed in the Lexes app.
    The DisplayList class is responsible for filtering, searching, and sorting entries based on
    user-selected attributes and is used to populate the dictionary display of entries in the app's main window.
    It exists as the communication layer between the app and the database to retrieve entries from the SQLite database.

Contains:
    - DisplayList class with methods to manage displaying entries.
    - Filtering by tags (all, any, or none).
    - Searching by keyword.
    - Sorting by various attributes (alphabeticalAscending, alphabeticalDescending, dateAscending, dateDescending).

Naming Conventions:
    - Class names: PascalCase (DisplayList).
    - Method names: camelCase (filter, search, sort, selectAll).
    - Attributes: camelCase (entries, filterTags, requireAllTags, searchKeyword, sortAttribute).
    - Constants: UPPERCASE (DBPATH).
    - General code: camelCase.
"""

### Module Imports ###
import sqlite3
import re

### Local Class Imports ###
from .helper import Helper
from .entry import Entry
from .selected_list import SelectedList
from config.configurations import DBPATH # Constant path to the database file

class DisplayList:
    # Initiation with default parameters for their respective data types and uses.
    def __init__(self,
                 entries: list[Entry] = None,
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
    def filter(self) -> None:
        self.entries = []

        with sqlite3.connect(DBPATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM master")
            rows = cursor.fetchall()

        # Case for filterTags being None, which gives entries with no tags.
        if self.filterTags is None:
            for row in rows:
                if row[3].strip() == "": # Tags field is empty
                    entry = Entry(uid=row[0], term=row[1], definition=row[2], tags=row[3], createdAt=row[4])
                    self.entries.append(entry)
            return  # Done with this special case, don't proceed further
                
        filterTags = [tag for tag in re.split(r"\s+", self.filterTags.strip())
                      if tag != ""] # filter tags from " a  b  c " to ["a", "b", "c"]
        
        # Case for no filterTags, which gives all entries.
        if len(filterTags) == 0:
            for row in rows:
                entry = Entry(uid=row[0],term=row[1], definition=row[2], tags=row[3], createdAt=row[4])
                self.entries.append(entry)

        # Case for filterTags existing and requireAllTags True which gives entries with ALL filterTags selected.
        elif self.requireAllTags == True:
            for row in rows:
                rowTags = re.split(r"\s+", row[3].strip())
                rowTags = [rowTag.lower() for rowTag in rowTags]
                if all(tag.lower() in rowTags for tag in filterTags):
                    entry = Entry(uid=row[0],term=row[1], definition=row[2], tags=row[3], createdAt=row[4])
                    self.entries.append(entry)

        # Case for filterTags existing and requireAllTags False which gives entries with ANY filterTags selected.
        elif self.requireAllTags == False:
            for row in rows:
                rowTags = re.split(r"\s+", row[3].strip())
                rowTags = [rowTag.lower() for rowTag in rowTags]
                if any(tag.lower() in rowTags for tag in filterTags):
                    entry = Entry(uid=row[0],term=row[1], definition=row[2], tags=row[3], createdAt=row[4])
                    self.entries.append(entry)

    # Rebuilds displayList.entries, excluding those without searchKeyword.
    def search(self) -> None:
        if self.searchKeyword == "":
            return

        # Changed from previously plan of removing entries without keyword to rebuilding displayList.entries, due to issues with removing entries while iterating
        self.entries = [entry for entry in self.entries
                        if self.searchKeyword.lower() in entry.term.lower() 
                        or self.searchKeyword.lower() in entry.definition.lower()
                        or self.searchKeyword.lower() in entry.tags.lower()]

    # Uses Helper.quickSort(), assumes sortAttribute is among alphabeticalAscending, alphabeticalDescending, dateAscending, dateDescending.
    def sort(self) -> None:
        self.entries = Helper.quickSort(self.entries, self.sortAttribute)

    # NOTE: IMPORTANT ORDER: filter -> search -> sort, and self.entries is cleared in filter() not build() itself.
    def build(self) -> None:
        self.filter()
        self.search()
        self.sort()

    # Selects all entries in displayList.entries, calling select() on each entry.
    # NOTE: Takes selectedList object as parameter for adequate scope.
    def selectAll(self,
                  selectedList: SelectedList) -> None: 
        for entry in self.entries:
            entry.select(selectedList)