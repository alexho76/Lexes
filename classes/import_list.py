### Import List Class
### Used to format a list of raw text of terms and/or definitions into valid Entry objects which can be imported into the database.

import re
import sqlite3
from .helper import Helper
from .entry import Entry


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

    # Parses the raw text chunk into entries, then entries into a tuple of (term, definition). Auto-definition if no definition provided. Reworded parsedEntries -> trialParsedEntries to avoid duplicate names.
    # Returns Boolean of successful parse and list of parsed entries as tuples.
    def parseText(self):
        rawEntries = re.split(r"\n+", self.rawText.strip())
        trialParsedEntries = []
        successfulParse = True

        for rawEntry in rawEntries:
            entry = rawEntry.strip().split(self.termDefinitionDelimiter, 1)
            
            if len(entry) == 2:
                term = entry[0].strip()
                definition = entry[1].strip()
            elif len(entry) == 1:
                term = entry[0].strip()
                definition = Helper.wikipediaAPI(term)  # calls Wikipedia API, keeps definition as blank if API request failed
                if definition is None:
                    definition = ""
            
            if term == "" or definition == "":
                successfulParse = False
            trialParsedEntries.append((term,definition)) # tuple of (term, definition)
        
        return successfulParse, trialParsedEntries

    # Checks if text is correctly formatted (entries by line break, term and definition by colon). Returns Boolean, and appends Entry objects to self.parsedEntries list if successful.
    def validateEntries(self):
        self.parsedEntries.clear()

        entriesToValidate = re.split(r"\n+", self.rawText.strip())

        for entryToValidate in entriesToValidate:
            entry = entryToValidate.strip().split(':', 1)

            if len(entry) != 2:
                self.parsedEntries.clear()
                return False
            
            term = entry[0].strip()
            definition = entry[1].strip()

            if term == "" or definition == "":
                self.parsedEntries.clear()
                return False

            entryObject = Entry(term=term, definition=definition, tags=self.massTags)
            self.parsedEntries.append(entryObject)

        return True

    # Adds all entries in self.parsedEntries to DB and clears attributes storing inputs.
    def importAndClear(self):
        for entry in self.parsedEntries:
            entry.add()
        
        self.rawText = ""
        self.parsedEntries.clear()
        # NOTE: DO NOT CLEAR self.entryDelimiter, self.termDefinitionDelimiter, or self.massTags (keeps as a sort of setting)
    
    # Imports all entries from DB at absolutePath into self.parsedEntries.
    def importDB(self,
                 absolutePath: str):
        with sqlite3.connect(absolutePath) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM master")
            rows = cursor.fetchall()

        for row in rows:
            term = row[1]
            definition = row[2]
            tags = row[3] or ""

            combinedTags = f"{self.massTags.strip()} {tags.strip()}".strip()

            entry = Entry(term=term, definition=definition, tags=combinedTags)
            self.parsedEntries.append(entry)