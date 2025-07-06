from PIL import Image

logoImage = Image.open("assets\lexes_logo.png").resize((232,86), Image.LANCZOS)
iconImage = Image.open("assets\lexes_icon.png").resize((65,65), Image.LANCZOS)

searchIconImage = Image.open("assets\search_icon.png").resize((40,40), Image.LANCZOS)
searchIconDarkImage = Image.open("assets\search_icon_dark.png").resize((50,50), Image.LANCZOS)
deleteNeutralIconImage = Image.open("assets\delete_neutral_icon.png").resize((47,49), Image.LANCZOS)
deleteActiveIconImage = Image.open("assets\delete_active_icon.png").resize((47,49), Image.LANCZOS)

checkboxNeutralIconImage = Image.open("assets\checkbox_neutral_icon.png").resize((24,24), Image.LANCZOS)
checkboxActiveIconImage = Image.open("assets\checkbox_active_icon.png").resize((24,24), Image.LANCZOS)
