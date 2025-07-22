### Images used in the app
### Imported as Image objects, can be converted to CTkImage objects.


from PIL import Image

logoImage = Image.open(r"assets\lexes_logo.png").resize((232,86), Image.LANCZOS)
iconImage = Image.open(r"assets\lexes_icon.png").resize((65,65), Image.LANCZOS)

searchIconImage = Image.open(r"assets\search_icon.png").resize((40,40), Image.LANCZOS)
searchIconDarkImage = Image.open(r"assets\search_icon_dark.png").resize((50,50), Image.LANCZOS)
deleteNeutralIconImage = Image.open(r"assets\delete_neutral_icon.png").resize((47,49), Image.LANCZOS)
deleteActiveIconImage = Image.open(r"assets\delete_active_icon.png").resize((47,49), Image.LANCZOS)

checkboxNeutralIconImage = Image.open(r"assets\checkbox_neutral_icon.png").resize((24,24), Image.LANCZOS)
checkboxActiveIconImage = Image.open(r"assets\checkbox_active_icon.png").resize((24,24), Image.LANCZOS)

# Icons
ellipsisIconImage = Image.open(r"assets\ellipsis_icon.png").resize((34,9), Image.LANCZOS)

clickToSelectIconImage = Image.open(r"assets\click_to_select_icon.png").resize((31,31), Image.LANCZOS)
termIconImage = Image.open(r"assets\term_icon.png").resize((33,21), Image.LANCZOS)
definitionIconImage = Image.open(r"assets\definition_icon.png").resize((26,28), Image.LANCZOS)
tagIconImage = Image.open(r"assets\tag_icon.png").resize((28,28), Image.LANCZOS)

autoDefIconImage = Image.open(r"assets\auto_def_icon.png").resize((45,45), Image.LANCZOS)
editIconImage = Image.open(r"assets\edit_icon.png").resize((39,39), Image.LANCZOS)

ankiNeutralIconImage = Image.open(r"assets\anki_neutral_icon.png").resize((33,41), Image.LANCZOS)
ankiActiveIconImage = Image.open(r"assets\anki_active_icon.png").resize((33,41), Image.LANCZOS)
databaseNeutralIconImage = Image.open(r"assets\database_neutral_icon.png").resize((53,53), Image.LANCZOS)
databaseActiveIconImage = Image.open(r"assets\database_active_icon.png").resize((53,53), Image.LANCZOS)

folderIconImage = Image.open(r"assets\folder_icon.png").resize((46,36), Image.LANCZOS)
