### Program: Lexes
### Author: Alexander Ho (ho-0084@mhs.vic.edu.au)
### Date Created: 25/06/2025
### Date Finished: TBA  
### Description: Personal dictionary and flashcard creation solution for students. Created for VCE Software Development 3&4 SAT.

import sqlite3
import customtkinter as ctk
from tkinter import messagebox
import datetime

class Entry:
    # Initiates the Entry with its attributes: uid and createdAt are optional parameters.
    def __init__(self, term: str, definition: str, tags: str, createdAt: datetime.datetime | None = None, uid: int | None = None):
        self.uid = uid
        self.term = term
        self.definition = definition
        self.tags = tags
        self.createdAt = createdAt
            
    def add():
        pass