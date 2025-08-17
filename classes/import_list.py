"""
File: classes/import_list.py

Purpose:
    Defines the ImportList class, which is used to format and process a list of raw text (of terms and definitions)
    into valid Entry objects that can be imported into the Lexes app's database. Handles parsing, validation, and batch importing of entries.

Contains:
    - ImportList class with methods for parsing text, validating entries, and importing them into the database.
    - Methods:
        - parseText: Parses the raw text into term-definition tuples, generating definitions using the Wikipedia API if needed.
        - validateEntries: Validates the format of the parsed entries and populates parsedEntries if valid, ready for import.
        - importAndClear: Imports the validated entries into the database and resets the appropriate attributes.

Naming Conventions:
    - Class names: PascalCase (ImportList).
    - Method names: camelCase (parseText, validateEntries, importAndClear, importDB).
    - Attributes: camelCase (rawText, entryDelimiter, termDefinitionDelimiter, massTags, parsedEntries, filePath).
    - General code: camelCase.
"""

### Module Imports ###
import re
import sqlite3

### Local Class Imports ###
from .helper import Helper
from .entry import Entry

class ImportList:
    def __init__(self,
                 filePath: str = "",
                 rawText: str = "",
                 entryDelimiter: str = "\n",
                 termDefinitionDelimiter: str = ":",
                 massTags: str = "",
                 parsedEntries: list[Entry] = None):
        """
        Initiates the ImportList with its attributes, avoiding mutable default arguments.
        - filePath (str): The path to the file to import entries from. String as it represents the file path.
        - rawText (str): The raw text to parse into entries. String as it represents the text to be parsed.
        - entryDelimiter (str): The delimiter to separate entries in the raw text. String as it represents the delimiter used in the text.
        - termDefinitionDelimiter (str): The delimiter to separate terms and definitions in each entry. String as it represents the delimiter used in the entry.
        - massTags (str): The tags to add to each entry. String as it represents the textually inputted series of tags to be added.
        - parsedEntries (list[Entry]): The list of parsed Entry objects. List so that it can be iterated.
        """
        self.rawText = rawText # raw text input to be parsed into entries
        self.entryDelimiter = entryDelimiter # delimiter to separate entries in raw text
        self.termDefinitionDelimiter = termDefinitionDelimiter # delimiter to separate term and definition in each entry
        self.massTags = massTags # tags to be added to each entry
        self.parsedEntries = parsedEntries if parsedEntries is not None else [] # mutable argument solution - list of Entry objects parsed from raw text
        self.filePath = filePath # path to the database file for importing entries

    def parseText(self) -> tuple[bool, list[tuple[str, str]]]:
        """
        Parses the raw text chunk into entries (term, definition) tuples. Generates definitions via Wikipedia API if needed.
        Returns Boolean of successful parse and list of parsed entries as tuples all in a tuple.
        """
        rawEntries = re.split(self.entryDelimiter, self.rawText.strip())
        trialParsedEntries = []
        successfulParse = True

        for rawEntry in rawEntries:
            entry = rawEntry.strip().split(self.termDefinitionDelimiter, 1)
            
            if len(entry) == 2:
                term = entry[0].strip()
                definition = entry[1].strip()

                # Generate definition using Wikipedia API if definition is empty
                if definition == "":
                    try:
                        definition = Helper.wikipediaAPI(term)
                        if definition is not None:
                            definition = definition.replace(":", ";")
                    except Exception as e:
                        print(f"Error occurred while fetching definition for '{term}': {e}")
                        definition = None
                    if definition is None:
                        definition = ""
            
            elif len(entry) == 1:
                term = entry[0].strip()

                # Generate definition using Wikipedia API if definition is empty
                try:
                    definition = Helper.wikipediaAPI(term)
                    if definition is not None:
                            definition = definition.replace(":", ";")
                except Exception as e:
                    print(f"Error occurred while fetching definition for '{term}': {e}")
                    definition = None
                if definition is None:
                    definition = ""
            
            if term == "" or definition == "":
                successfulParse = False

            trialParsedEntries.append((term, definition)) # tuple of (term, definition)

        return successfulParse, trialParsedEntries

    def validateEntries(self) -> bool:
        """
        Validates text format (one entry per line, term and definition separated by colon).
        Populates self.parsedEntries with Entry objects if successful. Returns True if all entries are valid, False otherwise.
        """
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

    def importAndClear(self) -> int:
        """
        Adds all entries in self.parsedEntries to DB and clears attributes storing inputs. Returns the number of entries added.
        """
        count = len(self.parsedEntries)
        
        for entry in self.parsedEntries:
            entry.add()
        
        self.rawText = ""
        self.parsedEntries.clear()
        # NOTE: DO NOT CLEAR self.entryDelimiter, self.termDefinitionDelimiter, or self.massTags (keeps as a sort of setting)
        # TBA: Save this across sessions.

        return count
    
    def importDB(self) -> None:
        """
        Imports all entries from DB at filePath into self.parsedEntries.
        """
        with sqlite3.connect(self.filePath) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM master")
            rows = cursor.fetchall()

        for row in rows: # Reads each row from DB
            term = row[1]
            definition = row[2]
            tags = row[3] or ""

            # Adds massTags to row's pre-existing tags
            combinedTags = f"{self.massTags.strip()} {tags.strip()}".strip()

            entry = Entry(term=term, definition=definition, tags=combinedTags)
            self.parsedEntries.append(entry)