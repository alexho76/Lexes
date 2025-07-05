# Class and Asset Imports
# from config.configurations import *
from config.theme import *
from classes.helper import Helper
from classes.entry import Entry
from classes.display_list import DisplayList
from classes.selected_list import SelectedList
from classes.import_list import ImportList
from classes.widgets.multi_select_combobox import MultiSelectComboBox
from classes.widgets.single_select_combobox import SingleSelectComboBox
from classes.widgets.searchbar_with_icon import SearchBarWithIcon
from assets.images import *

# Library Imports
import sqlite3
import customtkinter as ctk
import tkinter as tk
import ctypes
import tkinter.font as tkFont
from PIL import Image, ImageTk
import platform


class App:
    # Class attribute of database path
    dbPath = r"database\lexes.db"

    if platform.system() == "Windows":
        from ctypes import windll, byref, sizeof, c_int
        windll.shcore.SetProcessDpiAwareness(2)
    def __init__(self):
        self.setupDB()

        self.displayList = DisplayList()
        self.selectedList = SelectedList()
        ######################## UI ########################
        self.mainWindow = MainWindow(self)
        self.mainWindow.mainloop()

    # Ensures DB connection closes upon App closing.
    def __del__(self):
        conn = sqlite3.connect(App.dbPath)
        conn.close()
    
    def setupDB(self):
        conn = sqlite3.connect(App.dbPath)
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
        conn.close()

class MainWindow(ctk.CTk):
    def __init__(self, masterApp, **kwargs):
        super().__init__(**kwargs)

        self.attributes("-fullscreen", True)

        self.masterApp = masterApp

        user32 = ctypes.windll.user32
        screenWidth = user32.GetSystemMetrics(0)
        screenHeight = user32.GetSystemMetrics(1)

        self.geometry(f"{screenWidth}x{screenHeight}")
        self.title("Lexes")

        ### Menubar ###
        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label="Save")
        self.menubar.add_cascade(label="File", menu=self.file_menu)

        ### Background ###
        self.background = ctk.CTkFrame(self, corner_radius=0, fg_color=LightGreen1)
        self.background.pack(fill='both',expand=True)

                ### Navigation Bar ###
        self.navigationBar = ctk.CTkFrame(self.background, corner_radius=0, height=68, fg_color=LightGreen2)
        self.navigationBar.pack(side='top',fill='x')

        ### Navigation Buttons ###
        self.addButton = ctk.CTkButton(self.navigationBar, text="Add", width=120, height=50, corner_radius=5, anchor='center',
                                       font=("League Spartan Bold",22), text_color = NavigationPrimary, fg_color=Cream,
                                       border_color=NavigationPrimary, border_width=2.5,hover_color=Cream2)
        self.addButton.pack(side='left',padx=(9,2),pady=9)
        self.importButton = ctk.CTkButton(self.navigationBar, text="Import", width=120, height=50, corner_radius=5, anchor='center',
                                          font=("League Spartan Bold",22), text_color = NavigationPrimary, fg_color=Cream,
                                          border_color=NavigationPrimary, border_width=2.5,hover_color=Cream2)
        self.importButton.pack(side='left',padx=2,pady=9)
        self.exportButton = ctk.CTkButton(self.navigationBar, text="Export", width=120, height=50, corner_radius=5, anchor='center',
                                          font=("League Spartan Bold",22), text_color = NavigationPrimary, fg_color=Cream,
                                          border_color=NavigationPrimary, border_width=2.5,hover_color=Cream2)
        self.exportButton.pack(side='left',padx=2,pady=9)
        self.settingsButton = ctk.CTkButton(self.navigationBar, text="Settings", width=120, height=50, corner_radius=5, anchor='center',
                                            font=("League Spartan Bold",22), text_color = NavigationSecondary, fg_color=Cream,
                                            border_color=NavigationSecondary, border_width=2.5,hover_color=Cream2)
        self.settingsButton.pack(side='left',padx=2,pady=9)
        self.helpButton = ctk.CTkButton(self.navigationBar, text="Help", width=120, height=50, corner_radius=5, anchor='center',
                                        font=("League Spartan Bold",22), text_color = NavigationSecondary, fg_color=Cream,
                                        border_color=NavigationSecondary, border_width=2.5,hover_color=Cream2)
        self.helpButton.pack(side='left',padx=2,pady=9)
        self.exitButton = ctk.CTkButton(self.navigationBar, text="Exit", width=120, height=50, corner_radius=5, anchor='center',
                                        font=("League Spartan Bold",22), text_color = Red, fg_color=Cream,
                                        border_color=Red, border_width=2.5,hover_color=Cream2, command=self.quit)
        self.exitButton.pack(side='right',padx=(2,9),pady=9)

        ### Logo ###
        ctkLogoImage = ctk.CTkImage(light_image=logoImage, dark_image=logoImage, size=(232,86))
        self.logo = ctk.CTkLabel(self.background, image=ctkLogoImage, text="")
        self.logo.pack(pady=20)

        ### Tool Bar ###
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
            icon_text="...",
            icon_font=("Arial", 28),
            icon_width=40
        )   
        self.searchBar.pack(side='left',padx=(93,6),anchor='n')


        # self.searchBar = ctk.CTkEntry(self.toolBar, placeholder_text="Search by keyword", width=500, height=50,
        #                               corner_radius=200, font=("League Spartan",36), text_color=DarkGreen2,
        #                               placeholder_text_color=DarkGreen2, fg_color=DarkGreen1,border_width=0)
        # self.searchBar.pack(side='left',padx=(93,6),anchor='n')
        # self.searchBar.configure(justify='left')

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



        ### Footer ###
        self.footer = ctk.CTkFrame(self.background, fg_color='white', height=83)
        self.footer.pack(fill='x',side='bottom')

        ctkIconImage = ctk.CTkImage(light_image=iconImage, dark_image=iconImage, size=(65,65))
        self.icon = ctk.CTkLabel(self.footer, image=ctkIconImage, text="")
        self.icon.pack(pady=9)



app = App()