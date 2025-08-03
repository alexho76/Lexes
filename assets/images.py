"""
File: assets/images.py

Purpose:
    Contains all images for icons and logos used in the Lexes app.
    All images are imported as PIL.Image objects using a file path and resized to appropriate dimensions.
    They can be converted to CTkImage during use within the app to integrate with customtkinter GUI.
    This file centralises image management and ensures that all images are stored in one place for easy access.

Contains:
    - Lexes Brand Images
    - Search and delete icons
    - Checkbox icons
    - Miscellaneous UI icons (ellipsis, click to select)
    - Entry field icons (term, definition, tag)
    - Editing and utility icons (auto definition, edit, zoom)
    - Export icons (Anki, database, folder)
    - Delimiter icons for entries and term/definition separation

Naming Conventions:
    - All PIL.Image objects: camelCase and start with their description and end with "Icon" and/or "Image".
"""

from PIL import Image

### Lexes Logo and Brand Images ###
logoImage = Image.open(r"assets\lexes_logo.png").resize((232,86), Image.LANCZOS)
iconImage = Image.open(r"assets\lexes_icon.png").resize((65,65), Image.LANCZOS)
sloganXImage = Image.open(r"assets\lexes_slogan_x.png").resize((241,65), Image.LANCZOS)
sloganYImage = Image.open(r"assets\lexes_slogan_y.png").resize((171,87), Image.LANCZOS)
sloganXYImage = Image.open(r"assets\lexes_slogan_xy.png").resize((224,73), Image.LANCZOS)

### Search and Delete Icons ###
searchIconImage = Image.open(r"assets\search_icon.png").resize((40,40), Image.LANCZOS)
searchIconDarkImage = Image.open(r"assets\search_icon_dark.png").resize((50,50), Image.LANCZOS)
deleteNeutralIconImage = Image.open(r"assets\delete_neutral_icon.png").resize((47,49), Image.LANCZOS)
deleteActiveIconImage = Image.open(r"assets\delete_active_icon.png").resize((47,49), Image.LANCZOS)

### Checkbox Icons ###
checkboxNeutralIconImage = Image.open(r"assets\checkbox_neutral_icon.png").resize((24,24), Image.LANCZOS)
checkboxActiveIconImage = Image.open(r"assets\checkbox_active_icon.png").resize((24,24), Image.LANCZOS)

### Miscellaneous Icons ###
ellipsisIconImage = Image.open(r"assets\ellipsis_icon.png").resize((34,9), Image.LANCZOS)
clickToSelectIconImage = Image.open(r"assets\click_to_select_icon.png").resize((31,31), Image.LANCZOS)
dangerIconImage = Image.open(r"assets\danger_icon.png").resize((30,30), Image.LANCZOS)

### Entry Field Icons ###
termIconImage = Image.open(r"assets\term_icon.png").resize((33,21), Image.LANCZOS)
definitionIconImage = Image.open(r"assets\definition_icon.png").resize((26,28), Image.LANCZOS)
tagIconImage = Image.open(r"assets\tag_icon.png").resize((28,28), Image.LANCZOS)
tagLightIconImage = Image.open(r"assets\tag_light_icon.png").resize((37,37), Image.LANCZOS)

### Editing and Utility Icons ###
autoDefIconImage = Image.open(r"assets\auto_def_icon.png").resize((45,45), Image.LANCZOS)
editIconImage = Image.open(r"assets\edit_icon.png").resize((39,39), Image.LANCZOS)
zoomIconImage = Image.open(r"assets\zoom_icon.png").resize((32,32), Image.LANCZOS)

### Export (Anki/Database) Icons ###
ankiNeutralIconImage = Image.open(r"assets\anki_neutral_icon.png").resize((33,41), Image.LANCZOS)
ankiActiveIconImage = Image.open(r"assets\anki_active_icon.png").resize((33,41), Image.LANCZOS)
databaseNeutralIconImage = Image.open(r"assets\database_neutral_icon.png").resize((53,53), Image.LANCZOS)
databaseActiveIconImage = Image.open(r"assets\database_active_icon.png").resize((53,53), Image.LANCZOS)
folderIconImage = Image.open(r"assets\folder_icon.png").resize((46,36), Image.LANCZOS)

### Delimiter Icons ###
entryDelimiterIconImage = Image.open(r"assets\entry_delimiter_icon.png").resize((35,34), Image.LANCZOS)
termDefinitionDelimiterIconImage = Image.open(r"assets\term_definition_delimiter_icon.png").resize((33,28), Image.LANCZOS)