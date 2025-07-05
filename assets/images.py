from PIL import Image

logoImage = Image.open("assets\lexes_logo.png").resize((232,86), Image.LANCZOS)
iconImage = Image.open("assets\lexes_icon.png").resize((65,65), Image.LANCZOS)