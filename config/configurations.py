"""
File: config/configurations.py

Purpose:
    Stores constant app-wide configurations and settings for the program.

Contains:
    - DBPATH: Default database path for the application.
    - LASTUSEDTAGSPATH: Path to the file storing the last used tag for the application.

Naming Conventions:
    - Constants: UPPERCASE (DBPATH).
"""

### Constants ###
"""
Default database path for the application.
"""
DBPATH = r"database\lexes.db"

"""
Last used tag for the application, used to remember the last tag selected by the user.
Will be updated when the user adds a new entry with tags and will be used to pre-fill the tag field in the entry form.
"""
LASTUSEDTAGSPATH = r"config\last_used_tags.txt"

"""
Path to the file storing the tags preference for the application.
This file will contain the tags that the user has set as their preference for autofill in the entry form
(either "Last Used", "Default", or "None").
"""
TAGSPREFERENCEPATH = r"config\tags_preference.txt"

"""
Default tags path for the application.
This file will contain the default tags that the user has set for the application.
"""
DEFAULTTAGSPATH = r"config\default_tags.txt"