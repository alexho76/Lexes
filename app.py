### App Class
### Manages the interactions between UI and backend classes and methods. All of the app's logic is contained here.

# Class and Asset Imports
from config.theme import *
from config.configurations import *
from classes.helper import Helper
from classes.entry import Entry
from classes.display_list import DisplayList
from classes.selected_list import SelectedList
from classes.import_list import ImportList
from classes.widgets.multi_select_combobox import MultiSelectComboBox
from classes.widgets.single_select_combobox import SingleSelectComboBox
from classes.widgets.searchbar_with_icon import SearchBarWithIcon
from classes.widgets.toggle_checkbox_button import ToggleCheckboxButton
from classes.widgets.locked_button import LockedButton
from classes.widgets.dictionary_list import DictionaryList
from assets.images import *

# Library Imports
import sqlite3
import customtkinter as ctk
import tkinter as tk
import ctypes
import tkinter.font as tkFont
from PIL import Image, ImageTk
import platform
import time

class App:
    if platform.system() == "Windows": # fullscreen the app
        from ctypes import windll, byref, sizeof, c_int
        windll.shcore.SetProcessDpiAwareness(2)
    
    def __init__(self):
        self.setupDB()

        # Initalise displayList and selectedList
        self.displayList = DisplayList()
        self.selectedList = SelectedList()

        # Initialise UI
        self.mainWindow = MainWindow(self)
        self.mainWindow.mainloop()
    
    def setupDB(self):
        with sqlite3.connect(dbPath) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS master (
                    uid INTEGER PRIMARY KEY AUTOINCREMENT,
                    term TEXT NOT NULL,
                    definition TEXT NOT NULL,
                    tags TEXT,
                    createdAt TEXT NOT NULL)
            """)
            conn.commit()

class MainWindow(ctk.CTk):
    def __init__(self, masterApp, **kwargs):
        super().__init__(**kwargs)
        self.attributes("-fullscreen", True)
        user32 = ctypes.windll.user32
        screenWidth = user32.GetSystemMetrics(0)
        screenHeight = user32.GetSystemMetrics(1)
        self.applyCustomScaling()

        self.masterApp = masterApp
        self.geometry(f"{screenWidth}x{screenHeight}")
        self.title("Lexes - Main Window")

        # Menubar
        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)
        self.fileMenu = tk.Menu(self.menubar, tearoff=0)
        self.fileMenu.add_command(label="Save")
        self.menubar.add_cascade(label="File", menu=self.fileMenu)

        # Background Frame (behind all UI elements)
        self.background = ctk.CTkFrame(self, corner_radius=0, fg_color=LightGreen1)
        self.background.pack(fill='both',expand=True)

        # Navigation Bar with Buttons
        self.navigationBar = ctk.CTkFrame(self.background, corner_radius=0, height=60, fg_color=LightGreen2)
        self.navigationBar.pack(side='top',fill='x')

        # Navigation Bar Buttons
        self.addButton = ctk.CTkButton(self.navigationBar, text="Add", width=100, height=40, corner_radius=5, anchor='center',
                                       font=("League Spartan Bold",22), text_color = NavigationPrimary, fg_color=Cream,
                                       border_color=NavigationPrimary, border_width=2.5,hover_color=Cream2,command=lambda: self.openTopLevel())
        self.addButton.pack(side='left',padx=(9,2),pady=9)
        self.importButton = ctk.CTkButton(self.navigationBar, text="Import", width=100, height=40, corner_radius=5, anchor='center',
                                          font=("League Spartan Bold",22), text_color = NavigationPrimary, fg_color=Cream,
                                          border_color=NavigationPrimary, border_width=2.5,hover_color=Cream2)
        self.importButton.pack(side='left',padx=2,pady=9)
        self.exportButton = ctk.CTkButton(self.navigationBar, text="Export", width=100, height=40, corner_radius=5, anchor='center',
                                          font=("League Spartan Bold",22), text_color = NavigationPrimary, fg_color=Cream,
                                          border_color=NavigationPrimary, border_width=2.5,hover_color=Cream2)
        self.exportButton.pack(side='left',padx=2,pady=9)
        self.settingsButton = ctk.CTkButton(self.navigationBar, text="Settings", width=100, height=40, corner_radius=5, anchor='center',
                                            font=("League Spartan Bold",22), text_color = NavigationSecondary, fg_color=Cream,
                                            border_color=NavigationSecondary, border_width=2.5,hover_color=Cream2)
        self.settingsButton.pack(side='left',padx=2,pady=9)
        self.helpButton = ctk.CTkButton(self.navigationBar, text="Help", width=100, height=40, corner_radius=5, anchor='center',
                                        font=("League Spartan Bold",22), text_color = NavigationSecondary, fg_color=Cream,
                                        border_color=NavigationSecondary, border_width=2.5,hover_color=Cream2)
        self.helpButton.pack(side='left',padx=2,pady=9)
        self.exitButton = ctk.CTkButton(self.navigationBar, text="Exit", width=100, height=40, corner_radius=5, anchor='center',
                                        font=("League Spartan Bold",22), text_color = Red, fg_color=Cream,
                                        border_color=Red, border_width=2.5,hover_color=Cream2, command=self.quit)
        self.exitButton.pack(side='right',padx=(2,9),pady=9)

        # Lexes Main Logo
        ctkLogoImage = ctk.CTkImage(light_image=logoImage, dark_image=logoImage, size=(232,86))
        self.logo = ctk.CTkLabel(self.background, image=ctkLogoImage, text="")
        self.logo.pack(pady=20)

        # Tool Bar with Searchbar, Filterbar, Sortbar, Select Button, Delete Button widgets
        self.toolBar = ctk.CTkFrame(self.background, fg_color=LightGreen1,height=100)
        self.toolBar.pack(fill='x')
        
        self.searchBar = SearchBarWithIcon(
            master=self.toolBar,
            width=500,
            height=60,
            corner_radius=200,
            entry_placeholder="Search by keyword",
            font=("League Spartan", 36),
            text_color=DarkGreen2,
            placeholder_text_color=DarkGreen2,
            fg_color=DarkGreen1,
            border_width=0,
            icon = searchIconImage,
            icon_hover=searchIconDarkImage,
            icon_width=40,
            bg_color=LightGreen1
        )   
        self.searchBar.pack(side='left',padx=(55,6),anchor='n')

        self.filterBar = MultiSelectComboBox(self.toolBar,
        options=["Math", "Physics","3","4","5","6","7","8","9","10","11","12"],
        font=("League Spartan", 36), dropdown_font=("League Spartan", 24), fg_color=DarkGreen1,
        text_color=DarkGreen2, corner_radius=50, height=60, border_width=0,
        hover_color=DarkGreen1b, selected_bg_color=DarkGreen3, selected_text_color=Cream,
        width=350, default_text="Filter by tags")
        self.filterBar.pack(side='left', padx=6)

        self.sortBar = SingleSelectComboBox(self.toolBar,
        options=["Newest", "Oldest", "A-Z", "Z-A"],
        font=("League Spartan", 36), dropdown_font=("League Spartan", 24), fg_color=DarkGreen1,
        text_color=DarkGreen2, corner_radius=50, height=60, border_width=0,
        hover_color=DarkGreen1b, selected_bg_color=DarkGreen3, selected_text_color=Cream,
        width=200, default_text="Sort by")
        self.sortBar.pack(side='left', padx=6)

        self.selectAllToggle = ToggleCheckboxButton(self.toolBar, neutral_text="Select all", active_text="Unselect all",
        width=220, height=60, corner_radius=5, font=("League Spartan", 36), image_neutral=checkboxNeutralIconImage,
        image_active=checkboxActiveIconImage, fg_color_neutral=DarkGreen1, fg_color_active=DarkGreen2,
        text_color_neutral=DarkGreen2, text_color_active=DarkGreen1, bg_color="transparent",
        command=self.selectAllToggleCommand)
        self.selectAllToggle.pack(side='left',padx=(55,5))

        self.deleteSelectedButton = LockedButton(self.toolBar, neutral_icon=deleteNeutralIconImage, active_icon=deleteActiveIconImage,
        icon_size=(47,49), width=60, height=60, corner_radius=5, anchor='center', fg_color_neutral=Grey1, fg_color_active=LightRed1,
        hover_color_active=LightRed2, text="")
        self.deleteSelectedButton.pack(side='left',padx=(0,9))

        # Dictionary List Test
        self.dictionaryList = DictionaryList(self.background)
        self.dictionaryList.pack(pady=(10,0))

        entries = [
            Entry(term="Photosynthesis", definition="Process used by plants and other organisms to convert light energy into chemical energy stored in glucose.", tags="biology plants energy skibble"),
            Entry(term="Entropy", definition="A measure of the disorder or randomness in a closed system, important in thermodynamics.", tags="physics thermodynamics"),
            Entry(term="Mitochondria", definition="Organelles known as the powerhouse of the cell; generate most of the cell's supply of ATP.", tags="biology cell energy"),
            Entry(term="Quantum Mechanics", definition="A fundamental theory in physics describing nature at the smallest scales.", tags="physics quantum theory science"),
            Entry(term="Algorithm", definition="A step-by-step procedure for solving a problem or accomplishing some end.", tags="computer science programming logic"),
            Entry(term="Ecosystem", definition="A biological community of interacting organisms and their physical environment.", tags="biology environment ecology"),
        ]

        self.dictionaryList.populate(entries)


        # Footer with Logo (will be across all pages)
        self.footer = ctk.CTkFrame(self.background, fg_color='blue', height=10)
        self.footer.pack(fill='x',side='bottom',pady=9)

        ctkIconImage = ctk.CTkImage(light_image=iconImage, dark_image=iconImage, size=(1,1))
        self.icon = ctk.CTkLabel(self.footer, image=ctkIconImage, text="")
        self.icon.pack(pady=1)
    
    def selectAllToggleCommand(self): #! bound to selectAllToggle Button to toggle deleteSelectedButton appearance.
        if self.selectAllToggle.get_state():
            self.deleteSelectedButton.unlock()
        else:
            self.deleteSelectedButton.lock()
    
    def openTopLevel(self): #! temporary function to test TopLevels
        self.topLevel = ctk.CTkToplevel(self)
        self.topLevel.geometry("600x400")
        self.topLevel.title("Add Entry")

        # Make sure it's above the main window
        self.topLevel.lift()
        self.topLevel.attributes("-topmost", True)
        self.topLevel.after(10, lambda: self.topLevel.attributes("-topmost", False))

        # Force focus (keyboard + window manager)
        self.topLevel.focus_force()
        self.topLevel.grab_set()  # Makes it modal – grabs all input

        # Test label
        self.focusLabel = ctk.CTkLabel(self.topLevel, text="Waiting for focus...", font=("Arial", 20))
        self.focusLabel.pack(pady=20)

        # Entry to test keyboard focus
        entry = ctk.CTkEntry(self.topLevel, placeholder_text="Type here")
        entry.pack(pady=20)
        entry.focus_set()

        self.topLevel.bind("<FocusIn>", lambda e: self.focus_label.configure(text="TopLevel HAS focus!"))
        self.topLevel.bind("<FocusOut>", lambda e: self.focus_label.configure(text="TopLevel lost focus."))

    # Sets Windows display settings scaling to match intended scaling for app
    def applyCustomScaling(self):
        user32 = ctypes.windll.user32
        gdi32 = ctypes.windll.gdi32

        hdc = user32.GetDC(0)
        dpi = gdi32.GetDeviceCaps(hdc, 88)
        user32.ReleaseDC(0, hdc)

        scalingPercent = int((dpi / 96) * 100)

        if scalingPercent != 100:
            # scale is not 100%, manipulate to get to 100%
            scale = 100/scalingPercent
            ctk.set_window_scaling(scale)
            ctk.set_widget_scaling(scale)
        else:
            # scale is already 100%
            ctk.set_window_scaling(1.0)
            ctk.set_widget_scaling(1.0)

app = App()