import sqlite3
import re
from .helper import Helper
from .entry import Entry
from .selected_list import SelectedList
from config.database import dbPath

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
        conn = sqlite3.connect(dbPath)
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
