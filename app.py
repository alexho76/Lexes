"""
Program: Lexes
Author: Alexander Ho (ho-0084@mhs.vic.edu.au / alexanderh6886@gmail.com)
Date Created: 25/06/2025
Date Last Modified: 31/07/2025  
Description: Personal dictionary and flashcard creation solution for students. Created for VCE Software Development 3&4 SAT. See README.md for more information.

File: app.py

Purpose:
    This file contains all main application logic, including the UI and backend integration.
    It is the single entry point for running the Lexes application.

Contains:
    - App class: Responsible for initialising the UI and managing backend interactions and events.
    - MainWindow class: Handles all UI construction, event callbacks, and page logic for the Main Window.
    - Methods within MainWindow for handling external popup windows (Add, Import, Export, etc.).

Naming Conventions:
    - Class names: PascalCase (App, MainWindow).
    - Method names: camelCase (initialiseUI, start, setupDB).
    - Attributes: camelCase (displayList, selectedList, mainWindow).
    - Constants: UPPERCASE (DBPATH, LASTUSEDTAGSPATH, TAGSPREFERENCEPATH, DEFAULTTAGSPATH).
    - General code: camelCase.

Usage:
    Run this file directly to launch the Lexes application: 'python app.py'.
    All UI and main logic is contained here. No external main.py is required.
"""

### External Module/Library Imports ###
# CustomTkinter and Tkinter for UI
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

# SQLite3 for database interactions
import sqlite3

# Other libraries for system interactions
import ctypes
import platform
import os

### Local Class & Assets Imports ###
# Config and Assets Imports
from config.theme import *
from config.configurations import * # PATH constants
from assets.images import *

# Backend Class Imports
from classes.helper import Helper
from classes.entry import Entry
from classes.display_list import DisplayList
from classes.selected_list import SelectedList
from classes.import_list import ImportList

# Widget Imports
from classes.widgets.multi_select_combobox import MultiSelectComboBox
from classes.widgets.single_select_combobox import SingleSelectComboBox
from classes.widgets.searchbar_with_icon import SearchBarWithIcon
from classes.widgets.toggle_checkbox_button import ToggleCheckboxButton
from classes.widgets.locked_button import LockedButton
from classes.widgets.dictionary_list import DictionaryList
from classes.widgets.export_button import ExportButton
from classes.widgets.file_path_entry import FilePathEntry
from classes.widgets.select_file_path_entry import SelectFilePathEntry

class App:
    """
    Main application class. Hdandles initialisation of UI and setup of backend database.
    """
    if platform.system() == "Windows": # fullscreen the app
        from ctypes import windll, byref, sizeof, c_int
        windll.shcore.SetProcessDpiAwareness(2)
    
    def __init__(self) -> None:
        """
        Setups up the database, instantiates backend classes (DisplayList, SelectedList), and initialises the Main Window.
        """
        self.setupDB()
        self.displayList = DisplayList()
        self.displayList.build()
        self.selectedList = SelectedList()
        self.mainWindow = MainWindow(self) # instantiates main window

    def start(self) -> None:
        """
        Starts the Main Application's customTkinter main loop to start the UI running and event handling.
        """
        self.mainWindow.mainloop()

    def setupDB(self) -> None:
        """
        Initialises the SQLite database by either creating a new database file or connecting to an existing one.
        If a database file with the path of DBPATH exists, it will connect to it.
        Otherwise, it will create a new database file and a table named 'master' with the specified columns.
        """
        with sqlite3.connect(DBPATH) as conn:
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
    """
    Main application window class. Builds the UI and handles all main page logic and event callbacks.
    All auxiliary popup windows (Add, Import, Export, etc.) are children of this main window.
    """
    def __init__(self, masterApp, **kwargs) -> None:
        """
        Initialises the main window with customTkinter settings, sets the window to fullscreen, and creates the main UI elements.
        """
        super().__init__(**kwargs)
        ### CustomTkinter System Settings to Improve Scaling and Fit to Screen Size ###
        self.attributes("-fullscreen", True)
        user32 = ctypes.windll.user32
        screenWidth = user32.GetSystemMetrics(0)
        screenHeight = user32.GetSystemMetrics(1)
        self.applyCustomScaling()

        ### Root Window Settings ###
        self.masterApp = masterApp
        self.geometry(f"{screenWidth}x{screenHeight}")
        self.title("Lexes - Main Window")

        # Background Frame
        self.background = ctk.CTkFrame(self, corner_radius=0, fg_color=LightGreen1)
        self.background.pack(fill='both', expand=True)

        # Navigation Bar (with Buttons)
        self.navigationBar = ctk.CTkFrame(self.background, corner_radius=0, height=68, fg_color=LightGreen2)
        self.navigationBar.pack(side='top', fill='x')

        # Navigation Bar Buttons
        self.addButton = ctk.CTkButton(self.navigationBar,
                                       text="Add",
                                       width=129,
                                       height=50,
                                       corner_radius=5,
                                       anchor='center',
                                       font=("League Spartan Bold",24),
                                       text_color=NavigationPrimary,
                                       fg_color=Cream,
                                       border_color=NavigationPrimary,
                                       border_width=2,
                                       hover_color=Cream2,
                                       command=self.openAddWindow)
        self.addButton.pack(side='left', padx=(9,2), pady=9)
        
        self.bulkAddButton = ctk.CTkButton(self.navigationBar,
                                            text="Bulk Add",
                                            width=129,
                                            height=50,
                                            corner_radius=5,
                                            anchor='center',
                                            font=("League Spartan Bold",24),
                                            text_color=NavigationPrimary,
                                            fg_color=Cream,
                                            border_color=NavigationPrimary,
                                            border_width=2,
                                            hover_color=Cream2,
                                            command=self.openImportTextWindow)
        self.bulkAddButton.pack(side='left', padx=2, pady=9)
        
        self.importButton = ctk.CTkButton(self.navigationBar,
                                          text="Import",
                                          width=129,
                                          height=50,
                                          corner_radius=5,
                                          anchor='center',
                                          font=("League Spartan Bold",24),
                                          text_color = NavigationPrimary,
                                          fg_color=Cream,
                                          border_color=NavigationPrimary,
                                          border_width=2,
                                          hover_color=Cream2,
                                          command=self.openImportDBWindow)
        self.importButton.pack(side='left', padx=2, pady=9)
        
        self.exportButton = ctk.CTkButton(self.navigationBar,
                                          text="Export",
                                          width=129,
                                          height=50,
                                          corner_radius=5,
                                          anchor='center',
                                          font=("League Spartan Bold",24),
                                          text_color=NavigationPrimary,
                                          fg_color=Cream,
                                          border_color=NavigationPrimary,
                                          border_width=2,
                                          hover_color=Cream2,
                                          command=self.openExportWindow)
        self.exportButton.pack(side='left', padx=2, pady=9)
        
        self.settingsButton = ctk.CTkButton(self.navigationBar,
                                            text="Settings",
                                            width=129,
                                            height=50,
                                            corner_radius=5,
                                            anchor='center',
                                            font=("League Spartan Bold",24),
                                            text_color=NavigationSecondary,
                                            fg_color=Cream,
                                            border_color=NavigationSecondary,
                                            border_width=2,
                                            hover_color=Cream2,
                                            command=self.openSettingsWindow)
        self.settingsButton.pack(side='left', padx=2, pady=9)
        
        self.helpButton = ctk.CTkButton(self.navigationBar,
                                        text="Help",
                                        width=129,
                                        height=50,
                                        corner_radius=5,
                                        anchor='center',
                                        font=("League Spartan Bold",24),
                                        text_color=NavigationSecondary,
                                        fg_color=Cream,
                                        border_color=NavigationSecondary,
                                        border_width=2,
                                        hover_color=Cream2)
        self.helpButton.pack(side='left', padx=2, pady=9)
        
        self.exitButton = ctk.CTkButton(self.navigationBar,
                                        text="Exit",
                                        width=129,
                                        height=50,
                                        corner_radius=5,
                                        anchor='center',
                                        font=("League Spartan Bold",24),
                                        text_color=Red,
                                        fg_color=Cream,
                                        border_color=Red,
                                        border_width=2,
                                        hover_color=Cream2,
                                        command=self.quit)
        self.exitButton.pack(side='right', padx=9, pady=9)

        # Lexes Main Logo
        ctkLogoImage = ctk.CTkImage(light_image=logoImage, dark_image=logoImage, size=(258,95))
        self.logo = ctk.CTkLabel(self.background, image=ctkLogoImage, text="")
        self.logo.pack(pady=39)

        # Tool Bar with Searchbar, Filterbar, Sortbar, Select Button, Delete Button widgets
        self.toolBar = ctk.CTkFrame(self.background, fg_color=LightGreen1, height=70)
        self.toolBar.pack(fill='x', pady=(8,0))
        
        self.searchBar = SearchBarWithIcon(self.toolBar,
                                           width=661,
                                           height=65,
                                           corner_radius=200,
                                           entry_placeholder="Search by keyword",
                                           font=("League Spartan", 36),
                                           text_color=DarkGreen2,
                                           placeholder_text_color=DarkGreen2,
                                           fg_color=DarkGreen1,
                                           border_width=0,
                                           icon=searchIconImage,
                                           icon_hover=searchIconDarkImage,
                                           icon_width=40,
                                           bg_color=LightGreen1,
                                           on_search_callback=self.searchBarCommand)   
        self.searchBar.pack(side='left', padx=(93,6))

        self.filterBar = MultiSelectComboBox(self.toolBar,
                                             options=self.getUniqueTags(),
                                             font=("League Spartan", 36),
                                             dropdown_font=("League Spartan", 24),
                                             fg_color=DarkGreen1,
                                             text_color=DarkGreen2,
                                             corner_radius=50,
                                             height=65,
                                             border_width=0,
                                             require_frame_color=DarkGreen3,
                                             selected_bg_color=DarkGreen3,
                                             selected_text_color=Cream,
                                             width=400,
                                             default_text="Filter by tags",
                                             dropdown_bg_color=DarkGreen1b,
                                             on_close_callback=self.filterBarCommand)
        self.filterBar.pack(side='left', padx=6)

        ### Options Translation (Mapping) ###
        self.sortOptionsDictionary = {
            "Newest": "dateDescending",
            "Oldest": "dateAscending",
            "A-Z": "alphabeticalAscending",
            "Z-A": "alphabeticalDescending",
            None: "dateDescending" # default option if nothing selected
        }
        self.sortBar = SingleSelectComboBox(self.toolBar,
                                            options=["Newest", "Oldest", "A-Z", "Z-A"],
                                            options_dictionary=self.sortOptionsDictionary,
                                            font=("League Spartan", 36),
                                            dropdown_font=("League Spartan", 24),
                                            fg_color=DarkGreen1,
                                            text_color=DarkGreen2,
                                            corner_radius=50,
                                            width=238,
                                            height=65,
                                            border_width=0,
                                            selected_bg_color=DarkGreen3,
                                            selected_text_color=Cream,
                                            unselected_text_color=DarkGreen2,
                                            default_text="Sort by",
                                            dropdown_bg_color=DarkGreen1b,
                                            on_close_callback=self.sortBarCommand)
        self.sortBar.pack(side='left', padx=6)

        self.selectAllToggle = ToggleCheckboxButton(self.toolBar,
                                                    neutral_text="Select all",
                                                    active_text="Unselect all",
                                                    width=250,
                                                    height=65,
                                                    corner_radius=5,
                                                    font=("League Spartan", 36),
                                                    image_neutral=checkboxNeutralIconImage,
                                                    image_active=checkboxActiveIconImage,
                                                    fg_color_neutral=DarkGreen1,
                                                    fg_color_active=DarkGreen2,
                                                    text_color_neutral=DarkGreen2,
                                                    text_color_active=DarkGreen1,
                                                    bg_color="transparent",
                                                    command=self.selectAllToggleCommand)
        self.selectAllToggle.pack(side='left', padx=(85,5))

        self.deleteSelectedButton = LockedButton(self.toolBar,
                                                 neutral_icon=deleteNeutralIconImage,
                                                 active_icon=deleteActiveIconImage,
                                                 icon_size=(47,49),
                                                 width=65,
                                                 height=65,
                                                 corner_radius=5,
                                                 anchor='center',
                                                 fg_color_neutral=Grey1,
                                                 fg_color_active=LightRed1,
                                                 hover_color_active=LightRed2,
                                                 text="",
                                                 command=self.deleteSelectedButtonCommand)
        self.deleteSelectedButton.pack(side='right', padx=(0,93))

        # Dictionary List
        self.dictionaryList = DictionaryList(self.background,
                                             entries=self.masterApp.displayList.entries,
                                             selectedList=self.masterApp.selectedList,
                                             width=1920,
                                             height=644,
                                             row_height=100,
                                             term_font_size=48,
                                             definition_font_size=24,
                                             tag_font_size=36,
                                             header_bg_color=Cream,
                                             header_text_color=DarkGreen3,
                                             row_bg_color_1=DarkGreen1,
                                             row_bg_color_2=LightGreen2,
                                             selected_row_color_1="#C7EBD9",
                                             selected_row_color_2="#D5F6E9",
                                             divider_color=DarkGreen2,
                                             main_text_color="black",
                                             checkbox_color=DarkGreen3,
                                             tag_box_bg_color=Cream,
                                             tag_text_color=DarkGreen3,
                                             scroll_speed=1,
                                             overflow_icon = ellipsisIconImage,
                                             select_icon = clickToSelectIconImage,
                                             term_icon = termIconImage,
                                             definition_icon = definitionIconImage,
                                             tag_icon = tagIconImage,
                                             on_selection_change=self.onEntrySelectionChanged,
                                             on_row_click=self.handleRowClick)
        self.dictionaryList.pack(pady=(15,0))
    
        # Footer with Slogan and Entry Counter
        self.footer = ctk.CTkFrame(self.background, fg_color=LightGreen1)
        self.footer.pack(fill='both', side='bottom', pady=0, padx=0, expand=True)

        ctkSloganImage = ctk.CTkImage(light_image=sloganXYImage, dark_image=sloganXYImage, size=(224,73))
        self.icon = ctk.CTkLabel(self.footer, image=ctkSloganImage, text="", anchor='center')
        self.icon.pack(expand=True)
    
        self.entryCounter = ctk.CTkLabel(self.footer, text=f"Entries: {len(self.masterApp.selectedList.entries)}/{len(self.masterApp.displayList.entries)}", font=("League Spartan", 20), text_color=DarkGreen3)
        self.entryCounter.place(relx=0.005, rely=0)

    def updateCounter(self) -> None:
        """
        Updates the entry counter label to reflect the current number of selected entries and total entries.
        """
        # Add a delay to ensure the UI updates correctly
        self.entryCounter.after(5, lambda: self.entryCounter.configure(text=f"Entries: {len(self.masterApp.selectedList.entries)}/{len(self.masterApp.displayList.entries)}"))

    def handleRowClick(self, row_num, entry) -> None:
        """
        Callback for when a row in the dictionary list is clicked.
        Creates a sidebar with the entry's details and allows editing.
        Side bar features a title, UID, created date, and text boxes for definition and tags.
        Buttons for actions such as auto-defining, deleting, and saving changes or cancelling.
        """
        self.sidebarFrame.destroy() if hasattr(self, 'sidebarFrame') else None  # remove previous sidebar if exists
        
        # Make popup sidebar
        self.sidebarFrame = ctk.CTkFrame(self,
                                         width=720,
                                         height=977,
                                         corner_radius=0,
                                         fg_color=LightGreen2,
                                         bg_color=LightGreen1) # bottom
        self.sidebarFrame.place(x=1920 - 720, y=0)
        self.sidebarFrame.pack_propagate(False)

        # Title Card
        self.titleFrame = ctk.CTkFrame(self.sidebarFrame, width=720 - 70, corner_radius=0, fg_color="transparent", bg_color="transparent")
        self.titleFrame.pack(pady=(68,0), padx=35)
        self.titleFrame.pack_propagate(False)

        # Title Row
        self.titleRow = ctk.CTkFrame(self.titleFrame, width=720 - 70, corner_radius=0, fg_color="transparent", bg_color="transparent")
        self.titleRow.pack(pady=(0,0), padx=0, fill='x')
        
        def editButtonCommand() -> None:
            """
            Just focuses into the title entry field.
            Title is always editable, but this allows the user to click the edit button to focus into the title entry, making it easier to edit.
            """
            self.sidebarTitle.focus_set()
        
        ctkEditIconImage = ctk.CTkImage(light_image=editIconImage, dark_image=editIconImage, size=(35,35))
        self.editButton = ctk.CTkButton(self.titleRow,
                                        text="",
                                        image=ctkEditIconImage,
                                        height=35,
                                        width=35,
                                        fg_color="transparent",
                                        hover_color=DarkGreen1,
                                        command=editButtonCommand)
        self.editButton.pack(padx=0, pady=(8,0), side='left')

        self.sidebarTitle = ctk.CTkEntry(self.titleRow,
                                  font=("League Spartan Bold", 48),
                                  text_color=DarkGreen3,
                                  justify='left',
                                  fg_color=LightGreen2,
                                  bg_color="transparent",
                                  corner_radius=0,
                                  border_width=0,
                                  width=600)
        self.sidebarTitle.pack(pady=0, padx=0, fill='x', side='left')
        self.sidebarTitle.insert(0, entry.term)

        self.titleInfo = ctk.CTkFrame(self.titleFrame, fg_color="transparent", bg_color="transparent", corner_radius=0, width=720 - 70, height=22)
        self.titleInfo.pack(pady=(0,0), padx=0, fill='x')
        self.titleInfo.pack_propagate(False)
        self.uidInfo = ctk.CTkLabel(self.titleInfo, text=f"UID: {entry.uid}", font=("League Spartan Bold", 24), text_color="black")
        self.uidInfo.pack(pady=0, padx=0, side='left')
        self.createdAtInfo = ctk.CTkLabel(self.titleInfo, text=f"Created {entry.createdAt}", font=("League Spartan Bold", 24), text_color="black")
        self.createdAtInfo.pack(pady=0, padx=(22,0), side='left')

        # Title Buttons
        self.sidebarButtons = ctk.CTkFrame(self.titleFrame, width=720 - 70, height=65, corner_radius=0, fg_color="transparent", bg_color="transparent")
        self.sidebarButtons.pack(pady=(20,0), padx=0, fill='x')
        
        def sidebarAutoDefButtonCommand() -> None:
            """
            Retrieves the definition from Wikipedia for the current term in the sidebar title.
            If a definition is found, it updates the definition textbox.
            Else, it shows an error message.
            """
            updatedTerm = self.sidebarTitle.get().strip()
            newDefinition = Helper.wikipediaAPI(updatedTerm) # get definition from wikipedia
            if newDefinition:
                self.definitionTextbox.focus_set()
                self.definitionTextbox.delete(1.0, tk.END)
                self.definitionTextbox.insert(1.0, newDefinition)
            else: # no definition found
                messagebox.showerror("No Definition Found",
                                     f"No definition found for '{updatedTerm}'. Please enter a definition manually or try a different term.",
                                     parent=self.sidebarFrame)

        ctkAutoDefIconImage = ctk.CTkImage(light_image=autoDefIconImage, dark_image=autoDefIconImage, size=(45,45))
        self.sidebarAutoDefButton = ctk.CTkButton(self.sidebarButtons, 
                                                  image=ctkAutoDefIconImage,
                                                  text="",
                                                  border_color= Pink,
                                                  border_width=2.5,
                                                  fg_color=LightPink1,
                                                  hover_color=LightPink2,
                                                  height=65,
                                                  width=65,
                                                  corner_radius=5,
                                                  command=sidebarAutoDefButtonCommand)
        self.sidebarAutoDefButton.pack(padx=0, pady=0, side='left')
        
        def sidebarDeleteButtonCommand() -> None:
            """
            Destroys the sidebar frame and deletes the entry from the database.
            Clears selectedList entries and updates the display list.
            """
            self.sidebarFrame.destroy()

            with sqlite3.connect(DBPATH) as conn: # mass removal from db
                cursor = conn.cursor()
                cursor.execute("DELETE FROM master WHERE uid = ?", (entry.uid,))
                conn.commit()

            self.masterApp.selectedList.entries.clear()

            self.updateUI()

            if self.dictionaryList.entries == []:
                """
                No more entries remaining reset the displayList to default filter parameters and display.
                Checks only the dictinaryList. There may still be entries in the database.
                """
            
                # Reset displayList filter attributes
                self.masterApp.displayList.filterTags = ""
                self.masterApp.displayList.requireAllTags = False

                # Reset filter bar visually
                self.filterBar.selected_indices.clear()
                self.filterBar.require_all_var.set(False)
                self.filterBar.selected_text_var.set(self.filterBar.default_text)
                self.filterBar.refresh_options()

                # Reset search keyword attribute
                self.masterApp.displayList.searchKeyword = ""

                # Reset search bar visually
                self.searchBar.clear()  

                # Rebuild the display list again with filters off
                self.updateUI()

        ctkDeleteActiveIconImage = ctk.CTkImage(light_image=deleteActiveIconImage, dark_image=deleteActiveIconImage, size=(45,45))
        self.sidebarDeleteButton = ctk.CTkButton(self.sidebarButtons,
                                                 image=ctkDeleteActiveIconImage,
                                                 text="",
                                                 border_color=Red,
                                                 border_width=2.5,
                                                 fg_color=LightRed1,
                                                 hover_color=LightRed2,
                                                 height=65,
                                                 width=65,
                                                 corner_radius=5,
                                                 command=sidebarDeleteButtonCommand)
        self.sidebarDeleteButton.pack(padx=(10,0), pady=0, side='left')

        def sidebarDoneButtonCommand() -> None:
            """
            Saves the changes made in the sidebar to the entry.
            If no changes are made, it simply closes the sidebar.
            If changes are made, it updates the entry in the database and refreshes the UI.
            """
            newTerm = self.sidebarTitle.get().strip()
            newDefinition = self.definitionTextbox.get("1.0", tk.END).strip()
            newTags = self.tagsTextbox.get("1.0", tk.END)
            newTags = ' '.join(tag.strip() for tag in newTags.split())

            if newTerm == "" or newDefinition == "":
                # Empty term or definition fields. Show error message and return
                messagebox.showwarning("Missing Term or Definition",
                                       "Entry is missing a term or definition. Please try again.",
                                       parent=self.sidebarFrame)
                return

            if entry.tags == newTags and entry.term == newTerm and entry.definition == newDefinition: # close the sidebar as nothing has changed
                self.sidebarFrame.destroy()
                return

            entry.edit(newTerm=newTerm, newDefinition=newDefinition, newTags=newTags)

            self.sidebarFrame.destroy()
            self.updateUI()

        self.sidebarDoneButton = ctk.CTkButton(self.sidebarButtons,
                                               text="Done",
                                               font=("League Spartan Bold", 24),
                                               height=50,
                                               width=130,
                                               text_color=ButtonGreen,
                                               corner_radius=5,
                                               border_color=ButtonGreen,
                                               fg_color=Cream,
                                               hover_color=Cream2,
                                               border_width=2.5,
                                               command=sidebarDoneButtonCommand)
        self.sidebarDoneButton.pack(padx=0, pady=0, side='right')

        def sidebarCancelButtonCommand() -> None:
            """
            Closes the sidebar without saving any changes.
            """
            self.sidebarFrame.destroy()

        self.sidebarCancelButton = ctk.CTkButton(self.sidebarButtons,
                                               text="Cancel",
                                               font=("League Spartan Bold", 24),
                                               height=50,
                                               width=130,
                                               text_color=Red,
                                               corner_radius=5,
                                               border_color=Red,
                                               fg_color=Cream,
                                               hover_color=Cream2,
                                               border_width=2.5,
                                               command=sidebarCancelButtonCommand)
        self.sidebarCancelButton.pack(padx=5, pady=0, side='right')
        
        self.titleDefinitionDivider = ctk.CTkFrame(self.sidebarFrame, fg_color=DarkGreen1, height=1.5)
        self.titleDefinitionDivider.pack(padx=0,pady=0,fill="x")

        self.sidebarDefinitionLabel = ctk.CTkLabel(self.sidebarFrame,
                                                   text="Definition",
                                                   font=("League Spartan Bold", 36),
                                                   text_color=DarkGreen3,
                                                   anchor='w',
                                                   justify='left')
        self.sidebarDefinitionLabel.pack(pady=(10,0), padx=25, fill='x')
    
        # Definition Text Box
        self.definitionTextbox = ctk.CTkTextbox(self.sidebarFrame,
                                            font=("League Spartan", 26),
                                            text_color="black",
                                            fg_color=DarkGreen1,
                                            corner_radius=5,
                                            height=400,
                                            scrollbar_button_color=DarkGreen3,
                                            scrollbar_button_hover_color=ScrollbarGreen,
                                            border_spacing=0,
                                            border_width=5,
                                            border_color=DarkGreen1,
                                            wrap="word")
        self.definitionTextbox.pack(pady=(10, 0), padx=25, fill='both')
        self.definitionTextbox.insert("end", entry.definition)

        # Tags Label and Text box
        self.tagsTextbox = ctk.CTkTextbox(self.sidebarFrame,
                                            font=("League Spartan", 26),
                                            text_color="black",
                                            fg_color=DarkGreen1,
                                            corner_radius=5,
                                            height=50,
                                            scrollbar_button_color=DarkGreen3,
                                            scrollbar_button_hover_color=ScrollbarGreen,
                                            border_spacing=0,
                                            border_width=5,
                                            border_color=DarkGreen1,
                                            wrap="none")
        self.tagsTextbox.pack(pady=(0, 20), padx=25, fill='both', side='bottom')
        self.tagsTextbox.insert("end", entry.tags)
        # Prevent newlines and tab characters in the tags textbox (excess whitespace characters)
        self.tagsTextbox.bind("<Return>", lambda e: "break")
        self.tagsTextbox.bind("<Tab>", lambda e: "break")

        self.sidebarTagsFrame = ctk.CTkFrame(self.sidebarFrame, width=720 - 70, height=65, corner_radius=0, fg_color="transparent", bg_color="transparent")
        self.sidebarTagsFrame.pack(pady=(0,5), padx=25, fill='x', side='bottom')
        ctkTagsIconImage = ctk.CTkImage(light_image=tagIconImage, dark_image=tagIconImage, size=(30,30))
        self.sidebarTagsIcon = ctk.CTkLabel(self.sidebarTagsFrame,
                                            image=ctkTagsIconImage,
                                            text="")
        self.sidebarTagsIcon.pack(side="left", pady=(8,0), padx=(0,7))
        self.sidebarTagsLabel = ctk.CTkLabel(self.sidebarTagsFrame,
                                             text="Tags",
                                             font=("League Spartan Bold", 36),
                                             text_color=DarkGreen3,
                                             justify='left')
        self.sidebarTagsLabel.pack(side="left", pady=(0,0), padx=0, fill='x')

        self.definitionTagsDivider = ctk.CTkFrame(self.sidebarFrame, fg_color=DarkGreen1, height=1.5)
        self.definitionTagsDivider.pack(padx=0, pady=(0,7.5), fill="x", side='bottom')

        self.sidebarDivider = ctk.CTkFrame(self.sidebarFrame, width=3, corner_radius=0, fg_color=DarkGreen3, height=977)
        self.sidebarDivider.place(relx=0, rely=0)

    def searchBarCommand(self, searchKeyword) -> None:
        """
        Callback for when the search bar is used.
        Updates the displayList's searchKeyword attribute if it has changed and refreshes the dictionary UI.
        """
        if searchKeyword != self.masterApp.displayList.searchKeyword: # update search term
            self.masterApp.displayList.searchKeyword = searchKeyword
            
            self.updateDictionaryUI()
        else: # search keyword unchanged so do nothing
            return

    def filterBarCommand(self, selectedTags) -> None:
        """
        Callback for when the filter bar is used.
        Updates the displayList's filterTags and requireAllTags attributes based on the selected tags if they have changed.
        If no tags are selected, it resets the filterTags to None and requireAllTags to False.
        Refreshes the dictionary UI to reflect the changes.
        """
        if selectedTags is None: # option is "No tags" (show entries with no tags)
            self.masterApp.displayList.filterTags = None
            self.masterApp.displayList.requireAllTags = False
            self.updateDictionaryUI()
        else:
            selectedTags = " ".join(selectedTags)

            if (selectedTags != self.masterApp.displayList.filterTags or 
                self.filterBar.require_all_selected() != self.masterApp.displayList.requireAllTags): # update filter tags if something has changed
                
                self.masterApp.displayList.filterTags = selectedTags
                self.masterApp.displayList.requireAllTags = self.filterBar.require_all_selected()
                
                self.updateDictionaryUI()
            
            else: # selected tags unchanged so do nothing
                return

    def sortBarCommand(self, selectedAttribute) -> None:
        """
        Callback for when the sort bar is used.
        Updates the displayList's sortAttribute attribute based on the selected attribute if it has changed.
        Refreshes the dictionary UI to reflect the changes.
        """
        if selectedAttribute != self.masterApp.displayList.sortAttribute: # update sort attribute
            self.masterApp.displayList.sortAttribute = selectedAttribute
            
            self.updateDictionaryUI()
        else: # selected attribute unchanged so do nothing
            return

    def selectAllToggleCommand(self) -> None:
        """
        Callback for when the select all toggle is used.
        Selects or unselects all entries in the dictionary list.
        """
        if self.selectAllToggle.get_state():
            self.dictionaryList.select_all()
        else:
            self.dictionaryList.unselect_all()
        
        # Update both buttons immediately after bulk change
        self.updateDeleteButtonState()
        self.updateSelectAllButtonState()

    def onEntrySelectionChanged(self) -> None:
        """
        Callback for when the entry selection changes.
        Updates the delete button state and the entry counter.
        """
        self.updateDeleteButtonState()
        self.updateSelectAllButtonState()
        self.updateCounter()  # Update the entry counter when selection changes

    def updateSelectAllButtonState(self) -> None:
        """
        Updates the state of the select all button based on the current selection.
        If all entries are selected, the button displays in the "Unselect all"; otherwise, it displays "Select all".
        """
        if len(self.masterApp.selectedList.entries) == len(self.masterApp.displayList.entries): # All selected
            if self.selectAllToggle.get_state() == False:
                self.selectAllToggle.set_state(True) # Show "Unselect all"
        else:
            if self.selectAllToggle.get_state() == True:
                self.selectAllToggle.set_state(False) # Show "Select all"

    def updateDeleteButtonState(self) -> None:
        """
        Updates the state of the delete button based on the current selection.
        If selected entries exist, the button is enabled; otherwise, it is locked.
        This method is called whenever the selection changes in the dictionary list.
        """
        if len(self.masterApp.selectedList.entries) > 0:
            self.deleteSelectedButton.unlock()
        else:
            self.deleteSelectedButton.lock()

    def deleteSelectedButtonCommand(self) -> None:
        """
        Callback for when the delete selected button is pressed.
        Deletes the currently selected entries from the database and updates the UI.
        """
        if not self.masterApp.selectedList.entries:
            return

        if not messagebox.askyesno("Delete Entries",
                                   f"Are you sure you want to delete the selected entries ({len(self.masterApp.selectedList.entries)})? This action cannot be undone.",
                                   parent=self):
            return

        uidsToDelete = [entry.uid for entry in self.masterApp.selectedList.entries]

        with sqlite3.connect(DBPATH) as conn: # mass removal from db instead of individual deletes (entry.delete() method)
            cursor = conn.cursor()
            cursor.executemany("DELETE FROM master WHERE uid = ?", [(uid,) for uid in uidsToDelete])
            conn.commit()

        self.masterApp.selectedList.entries.clear()

        self.updateUI()

        if self.dictionaryList.entries == []:
            """
            No more entries remaining reset the displayList to default filter parameters and display.
            Checks only the dictinaryList. There may still be entries in the database.
            """
            # Reset displayList filter attributes
            self.masterApp.displayList.filterTags = ""
            self.masterApp.displayList.requireAllTags = False

            # Reset filter bar visually
            self.filterBar.selected_indices.clear()
            self.filterBar.require_all_var.set(False)
            self.filterBar.selected_text_var.set(self.filterBar.default_text)
            self.filterBar.refresh_options()

            # Reset search keyword attribute
            self.masterApp.displayList.searchKeyword = ""

            # Reset search bar visually
            self.searchBar.clear()  

            # Rebuild the display list again with filters off
            self.updateUI()

    def openAddWindow(self) -> None:
        """
        Opens a new window for adding a dictionary entry.
        The window contains fields for term, definition, and tags.
        It includes buttons for auto-defining the term, saving the entry, and cancelling.
        Uses LASTUSEDTAGSPATH to store the last used tag to pre-fill the tags field (saves between sessions).
        """
        ### Popup Window Setup ###
        topLevel = ctk.CTkToplevel(self)
        topLevel.geometry("1280x720")
        topLevel.title("Add Entry")
        topLevel.resizable(False, False)

        # Make sure it appears above the main window 
        topLevel.lift()
        topLevel.attributes("-topmost", True)
        topLevel.after(10, lambda: topLevel.attributes("-topmost", False))

        # Force focus (keyboard + window manager)
        topLevel.focus_force()
        topLevel.grab_set()  # grabs all inputs (kb and mouse)

        background = ctk.CTkFrame(topLevel, corner_radius=0, fg_color=LightGreen2)
        background.pack(fill="both", expand=True)

        # Term display and entry
        termLabelFrame = ctk.CTkFrame(background, corner_radius=0, fg_color="transparent")
        termLabelFrame.pack(padx=35,pady=(15,0), fill="x")

        ctktermIcon = ctk.CTkImage(dark_image=termIconImage, light_image=termIconImage, size=(46,30))
        termIconLabel = ctk.CTkLabel(termLabelFrame, text="", image=ctktermIcon, compound="left")
        termIconLabel.pack(padx=0, pady=(10,0), side='left')
        
        termLabel = ctk.CTkLabel(termLabelFrame, text="Term", font=("League Spartan", 48), text_color=DarkGreen2)
        termLabel.pack(padx=7, pady=(0,0), side='left')

        termEntry = ctk.CTkEntry(background, placeholder_text="e.g. photosynthesis", font=("League Spartan", 36),
                                 placeholder_text_color=Cream3, text_color=DarkGreen2, fg_color=Cream, border_color=DarkGreen3,
                                 border_width=2.5)
        termEntry.pack(padx=35, pady=0, fill="x")

        # Definition display, entry, and auto definition button
        definitionLabelFrame = ctk.CTkFrame(background, corner_radius=0, fg_color="transparent")
        definitionLabelFrame.pack(padx=35, pady=(15,0), fill="x")

        ctkDefinitionIcon = ctk.CTkImage(dark_image=definitionIconImage, light_image=definitionIconImage, size=(36,36))
        definitionIconLabel = ctk.CTkLabel(definitionLabelFrame, text="", image=ctkDefinitionIcon, compound="left")
        definitionIconLabel.pack(padx=0, pady=(13,0), side='left')

        definitionLabel = ctk.CTkLabel(definitionLabelFrame, text="Definition", font=("League Spartan", 48), text_color=DarkGreen2)
        definitionLabel.pack(padx=7, pady=(0,0), side='left')

        definitionEntry = ctk.CTkTextbox(background, font=("Bahnschrift", 36), text_color=DarkGreen2, fg_color=Cream,
                                         border_color=DarkGreen3, border_width=2.5, height=150, wrap="word",
                                         scrollbar_button_color=DarkGreen3, scrollbar_button_hover_color=ScrollbarGreen)

        definitionEntry.pack(padx=35, pady=0, fill="x")

        # Add placeholder text to definition entry
        placeholderText = "e.g. The process by which green plants and some other organisms use sunlight to synthesize nutrients from carbon dioxide and water."
        placeholderColor = Cream3
        normalColor = DarkGreen2

        def showPlaceholder() -> None:
            """
            Method to manually program placeholder text in the definition entry.
            Sets the text color to the placeholder color and inserts the placeholder text to the definition entry.
            """
            definitionEntry.configure(text_color=placeholderColor)
            definitionEntry.insert("1.0", placeholderText)

        def hidePlaceholder(event=None) -> None:
            """
            Method to manually program placeholder text in the definition entry.
            Hides placeholder text and sets the text color to normal.
            """
            definitionEntry.delete("1.0", tk.END)
            definitionEntry.configure(text_color=normalColor)

        def onFocusIn(event) -> None:
            """
            When the definition entry gains focus, check if it shows placeholder text.
            If it does, hide the placeholder text.
            """
            if definitionEntry.get("1.0", tk.END).strip() == placeholderText and definitionEntry.cget("text_color") == placeholderColor:
                hidePlaceholder()

        def onFocusOut(event) -> None:
            """
            When the definition entry loses focus, check if it is empty.
            If it is empty, show the placeholder text.
            """
            if not definitionEntry.get("1.0", tk.END).strip():
                showPlaceholder()

        definitionEntry.bind("<FocusIn>", onFocusIn)
        definitionEntry.bind("<FocusOut>", onFocusOut)

        # Show placeholder initially
        showPlaceholder()

        def autoDefButtonCommand() -> None:
            """
            Automatically defines the term entered by the user.
            Retrieves the definition from Wikipedia using the Helper class.
            If a definition is found, it updates the definition entry with the new definition.
            If no definition is found, it shows an error message.
            """
            term = termEntry.get().strip()
            if term:
                newDefinition = Helper.wikipediaAPI(term)
                if newDefinition:
                    definitionEntry.configure(text_color=DarkGreen2)  # reset text color to normal
                    definitionEntry.focus_set()
                    definitionEntry.delete(1.0, tk.END)
                    definitionEntry.insert(1.0, newDefinition)
                else:
                    messagebox.showerror("No Definition Found",
                                         f"No definition found for '{term}'. Please enter a definition manually or try a different term.",
                                         parent=topLevel)
            else:
                messagebox.showwarning("Empty Term",
                                       "Please enter a term before auto-defining.",
                                       parent=topLevel)
        ctkAutoDefineIcon = ctk.CTkImage(dark_image=autoDefIconImage, light_image=autoDefIconImage, size=(30,30))
        autoDefineButton = ctk.CTkButton(definitionLabelFrame, text="Auto-Define", font=("League Spartan", 28), command=autoDefButtonCommand, width=200, height=32,
                                         text_color=Pink, fg_color=Cream, border_color=Pink, border_width=2.5, hover_color=Cream2, image=ctkAutoDefineIcon, anchor='w')
        autoDefineButton.pack(padx=15, pady=(8,0), side='left')

        def saveLastUsedTags(tags: str) -> None:
            """
            Saves the last used tags to a file so that they can be pre-filled
            in the tag entry field next time the add entry window is opened.
            Using 'w' mode automatically overwrites the file's contents if it exists.
            """
            with open(LASTUSEDTAGSPATH, "w", encoding="utf-8") as file:
                file.write(tags)
        
        def getLastUsedTags() -> str:
            """
            Returns the last used tags from a file to pre-fill the tags field in the add entry window.
            """
            try:
                with open(LASTUSEDTAGSPATH, "r", encoding="utf-8") as file:
                    return file.read().strip()
            except FileNotFoundError:
                return ""

        # Tag display entry
        tagLabelFrame = ctk.CTkFrame(background, corner_radius=0, fg_color="transparent")
        tagLabelFrame.pack(padx=35, pady=(15,0), fill="x")

        ctkTagIcon = ctk.CTkImage(dark_image=tagIconImage, light_image=tagIconImage, size=(36,36))
        tagIconLabel = ctk.CTkLabel(tagLabelFrame, text="", image=ctkTagIcon, compound="left")
        tagIconLabel.pack(padx=0, pady=(10,0), side='left')

        tagLabel = ctk.CTkLabel(tagLabelFrame, text="Tags (optional)", font=("League Spartan", 48), text_color=DarkGreen2)
        tagLabel.pack(padx=7, pady=(0,0), side='left')

        ### Tag Entry ###
        tagEntry = ctk.CTkEntry(background, placeholder_text="e.g. nuclear_physics biology vce", font=("League Spartan", 36),
                                 placeholder_text_color=Cream3, text_color=DarkGreen2, fg_color=Cream, border_color=DarkGreen3,
                                 border_width=2.5)
        tagEntry.pack(padx=35, pady=0, fill="x")

        ### Tags Autofill ###
        # Read TAGSPREFERENCEPATH
        try:
            with open(TAGSPREFERENCEPATH, 'r', encoding='utf-8') as file:
                autofillPreference = file.read().strip()
        except FileNotFoundError:
            autofillPreference = "last_used" # default to last_used if file not found
        
        # If the autofill preference is set to "last_used", pre-fill the tag entry with the last used tags
        if autofillPreference == "last_used":
            # Ensure the LASTUSEDTAGSPATH file exists
            if not os.path.exists(LASTUSEDTAGSPATH):
                with open(LASTUSEDTAGSPATH, "w", encoding="utf-8") as file:
                    file.write("")
            else:
                # If the file exists, read the last used tags and pre-fill the tag entry
                lastUsedTags = getLastUsedTags()
                if lastUsedTags:
                    tagEntry.insert(0, lastUsedTags)
        
        # If the autofill preference is set to "default", pre-fill the tag entry with the default tags from DEFAULTTAGSPATH
        elif autofillPreference == "default":
            # Ensure the DEFAULTTAGSPATH file exists
            if not os.path.exists(DEFAULTTAGSPATH):
                with open(DEFAULTTAGSPATH, "w", encoding="utf-8") as file:
                    file.write("")
            else:
                # If the file exists, read the default tags and pre-fill the tag entry
                with open(DEFAULTTAGSPATH, "r", encoding="utf-8") as file:
                    defaultTags = file.read().strip()
                    if defaultTags:
                        tagEntry.insert(0, defaultTags)
        
        # If the autofill preference is set to "none", do not pre-fill the tag entry
        elif autofillPreference == "none":
            pass

        else: # No autofill preference set, fill it using last used tags
            # Ensure the LASTUSEDTAGSPATH file exists
            if not os.path.exists(LASTUSEDTAGSPATH):
                with open(LASTUSEDTAGSPATH, "w", encoding="utf-8") as file:
                    file.write("")
            else:
                # If the file exists, read the last used tags and pre-fill the tag entry
                lastUsedTags = getLastUsedTags()
                if lastUsedTags:
                    tagEntry.insert(0, lastUsedTags)

        # Window Navigation Buttons
        buttonFrame = ctk.CTkFrame(background, corner_radius=0, fg_color="transparent")
        buttonFrame.pack(padx=35, pady=(35,0), fill="x")

        def closeButtonCommand() -> None:
            """
            Closes the add entry window without saving any changes.
            """
            topLevel.destroy()
        closeButton = ctk.CTkButton(buttonFrame, text="Close", font=("League Spartan Bold", 24), height=50, width=130, text_color=Red, corner_radius=5,
                                     border_color=Red, fg_color=Cream, hover_color=Cream2, border_width=2.5, command=closeButtonCommand)
        closeButton.pack(side='right', padx=(0,0), pady=0)

        def addButtonCommand() -> None:
            """
            Adds the new entry to the database using fields from the UI (term, definition, tags).
            Also saves the last used tags to a file for pre-filling next time.
            """
            term = termEntry.get().strip()
            definition = definitionEntry.get("1.0", tk.END).strip()
            tags = tagEntry.get().strip() # still in space separated string format
            if (not term) or (definition == placeholderText) or (not definition):
                messagebox.showwarning("Missing Fields",
                                       "Please fill in both the term and definition fields.",
                                       parent=topLevel)
                return
            entry = Entry(term=term, definition=definition, tags=tags)
            entry.add()

            # Save the last used tags to a file
            saveLastUsedTags(tags)

            self.updateUI() # update the main app UI including the dictionary list, counter, and filter bar

            # Clear the input fields except for tags and focus on term entry (for convenience of adding multiple entries)
            termEntry.delete(0, tk.END)
            definitionEntry.delete(1.0, tk.END)
            definitionEntry.configure(text_color=placeholderColor)  # reset text color to placeholder
            definitionEntry.insert(1.0, placeholderText)  # reset to placeholder text
            termEntry.focus_set()

        addButton = ctk.CTkButton(buttonFrame, text="Add", font=("League Spartan Bold", 24), height=50, width=130, text_color=DarkGreen3, corner_radius=5,
                                  border_color=DarkGreen3, fg_color=Cream, hover_color=Cream2, border_width=2.5, command=addButtonCommand)
        addButton.pack(side='right', padx=(0,5), pady=0)

        # Footer
        footer = ctk.CTkFrame(background, corner_radius=0, fg_color=LightGreen1, height=80)
        footer.pack(fill='x', side='bottom', pady=0, padx=0)
        footer.pack_propagate(False)
        
        ctkIconImage = ctk.CTkImage(light_image=iconImage, dark_image=iconImage, size=(65,65))
        footerIcon = ctk.CTkLabel(footer, image=ctkIconImage, text="", anchor='center')
        footerIcon.pack(expand=True)

        # Focus into term entry once everything has been packed
        topLevel.after(500, termEntry.focus_set)

    def openExportWindow(self) -> None:
        """
        Opens a new window for exporting entries.
        The window allows the user to select the export format (Anki Deck or Lexes DB),
        specify the export file path, and choose whether to include tags.
        """
        ### Popup Window Setup ###
        topLevel = ctk.CTkToplevel(self)
        topLevel.geometry("1280x720")
        topLevel.title("Export Entries")
        topLevel.resizable(False, False)

        # Make sure it appears above the main window 
        topLevel.lift()
        topLevel.attributes("-topmost", True)
        topLevel.after(10, lambda: topLevel.attributes("-topmost", False))

        # Force focus (keyboard + window manager)
        topLevel.focus_force()
        topLevel.grab_set()  # grabs all inputs (kb and mouse)

        background = ctk.CTkFrame(topLevel, corner_radius=0, fg_color=LightGreen2)
        background.pack(fill="both", expand=True)

        # Export as label and frame for buttons
        exportAsLabel = ctk.CTkLabel(background, text="Export entries as:", font=("League Spartan", 48), text_color=DarkGreen2)
        exportAsLabel.pack(padx=35, pady=(15,0), anchor='nw')
        
        exportAsFrame = ctk.CTkFrame(background, corner_radius=0, fg_color="transparent")
        exportAsFrame.pack(padx=35, pady=(0,0), fill="x")

        def toggleExport(buttonName) -> None:
            """
            Toggles the export options for each button based on their respective states and function input.
            """
            exportDirectoryEntry.reset()  # Reset the file path entry when toggling export options
            
            if buttonName == "Anki Deck": # toggle Anki Deck export
                exportAnkiButton.toggle()
                if exportDBButton.get_state(): # if Lexes DB export is active, deactivate it
                    exportDBButton.set_state(False)

            elif buttonName == "Lexes DB": # toggle Lexes DB export
                exportDBButton.toggle()
                if exportAnkiButton.get_state(): # if Anki Deck export is active, deactivate it
                    exportAnkiButton.set_state(False)
            
            # if both buttons are inactive, change colours of export directory entry to represent deactivation
            if not exportAnkiButton.get_state() and not exportDBButton.get_state():
                exportDirectoryEntry.change_text_color("#C1C9BD")
                exportDirectoryEntry.configure(fg_color=Grey1)
            # if both buttons are active, reset export directory entry colours
            else:
                exportDirectoryEntry.change_text_color(Cream3)
                exportDirectoryEntry.configure(fg_color=Cream)

        exportAnkiButton = ExportButton(exportAsFrame, neutral_text="Anki Deck", active_text="Anki Deck", width=220, height=65, corner_radius=5,
                                                font=("League Spartan", 36), image_neutral=ankiNeutralIconImage, image_active=ankiActiveIconImage, fg_color_neutral=LightGreen2, fg_color_active=ExportBlue,
                                                text_color_neutral=ExportBlue, text_color_active=LightGreen2, border_color=ExportBlue, image_size=(33,41), callback_command=toggleExport)
        exportAnkiButton.pack(padx=0, pady=0, side='left')

        exportDBButton = ExportButton(exportAsFrame, neutral_text="Lexes DB", active_text="Lexes DB", width=220, height=65, corner_radius=5,
                                                font=("League Spartan", 36), image_neutral=databaseNeutralIconImage, image_active=databaseActiveIconImage, fg_color_neutral=LightGreen2, fg_color_active=ExportBlue,
                                                text_color_neutral=ExportBlue, text_color_active=LightGreen2, border_color=ExportBlue, image_size=(50,50), callback_command=toggleExport)
        exportDBButton.pack(padx=15, pady=0, side='left')

        # Export File Directory Selection
        exportDirectoryFrame = ctk.CTkFrame(background, corner_radius=0, fg_color="transparent")
        exportDirectoryFrame.pack(padx=35, pady=(20,0), fill="x")

        exportDirectoryLabel = ctk.CTkLabel(exportDirectoryFrame, text="Export file as:", font=("League Spartan", 48), text_color=DarkGreen2)
        exportDirectoryLabel.pack(padx=0, pady=0, anchor='nw')

        exportDirectoryEntry = FilePathEntry(exportDirectoryFrame, font=("League Spartan", 36), text_color=Cream3, fg_color=Cream, border_color=DarkGreen3,
                                             border_width=2.5, placeholder_text="Select file path...", icon=folderIconImage, icon_size=(46,36),
                                             option_one=exportAnkiButton, option_two=exportDBButton)
        exportDirectoryEntry.pack(padx=0, pady=0, fill="x")
        exportDirectoryEntry.change_text_color("#C1C9BD")
        exportDirectoryEntry.configure(fg_color=Grey1)

        # Include Tags Option
        tagFrame = ctk.CTkFrame(background, corner_radius=0, fg_color="transparent")
        tagFrame.pack(padx=35, pady=(25,0), fill="x")

        ctkTagIcon = ctk.CTkImage(dark_image=tagIconImage, light_image=tagIconImage, size=(36,36))
        tagIconLabel = ctk.CTkLabel(tagFrame, image=ctkTagIcon, text="", fg_color="transparent")
        tagIconLabel.pack(side="left", padx=0, pady=(0,5))

        tagLabel = ctk.CTkLabel(tagFrame, text="Include tags", font=("League Spartan", 48), text_color=DarkGreen2)
        tagLabel.pack(side="left", padx=(10,0), pady=(0,15))

        tagCheckbox = ctk.CTkCheckBox(tagFrame, text="", fg_color=DarkGreen2, border_color=DarkGreen2, bg_color=LightGreen2, text_color=DarkGreen2, border_width=3,
                                      checkbox_height=28, checkbox_width=28, corner_radius=5, hover_color=DarkGreen3, checkmark_color=Cream)
        tagCheckbox.pack(side="left", padx=(25,0), pady=0)

        # Footer
        footer = ctk.CTkFrame(background, corner_radius=0, fg_color=LightGreen1, height=80)
        footer.pack(fill='x', side='bottom', pady=0, padx=0)
        footer.pack_propagate(False)

        ctkIconImage = ctk.CTkImage(light_image=iconImage, dark_image=iconImage, size=(65,65))
        footerIcon = ctk.CTkLabel(footer, image=ctkIconImage, text="", anchor='center')
        footerIcon.pack(expand=True)

        # Button and Entry Counter Frame. Packed above the footer.
        bottomFrame = ctk.CTkFrame(background, corner_radius=0, fg_color="transparent")
        bottomFrame.pack(padx=35, pady=0, fill="x", side='bottom')

        entryCounter = ctk.CTkLabel(bottomFrame, text=f"{len(self.masterApp.selectedList.entries)} entries selected", font=("League Spartan", 48), text_color=DarkGreen2)
        entryCounter.pack(padx=0, pady=(0,20), side='left')

        def cancelButtonCommand() -> None:
            """
            Closes the export window without saving changes.
            """
            topLevel.destroy()
        cancelButton = ctk.CTkButton(bottomFrame, text="Cancel", font=("League Spartan Bold", 24), height=50, width=130, text_color=Red, corner_radius=5,
                                     border_color=Red, fg_color=Cream, hover_color=Cream2, border_width=2.5, command=cancelButtonCommand)
        cancelButton.pack(side='right', padx=(0,0), pady=0)

        def exportButtonCommand() -> None:
            """
            Initiates the export process based on the selected options.
            Validates the selected export type, file path, and ensures entries are selected before proceeding.
            If any validation fails, it shows a warning message.
            If all validations pass, it calls the appropriate export method on the selectedList.
            Closes the export window and shows a success message.
            """
            if not exportAnkiButton.get_state() and not exportDBButton.get_state(): # no export type selected
                messagebox.showwarning("No Export Type Selected",
                                       "Please select an export type (Anki Deck or Lexes DB).",
                                       parent=topLevel)
                return
            if not exportDirectoryEntry.get_path(): # no file path selected
                messagebox.showwarning("No File Path Selected",
                                       "Please select a file path to export the file to.",
                                       parent=topLevel)
                return
            if len(self.masterApp.selectedList.entries) == 0: # (shouldn't ever happen but just in case)
                messagebox.showwarning("No Entries Selected",
                                       "Please select entries to export.",
                                       parent=topLevel)
                return
            # all validations passed, proceed with export

            filePath = exportDirectoryEntry.get_path()

            if filePath.endswith(".csv"): # exporting to anki deck
                self.masterApp.selectedList.exportToAnki(filePath=filePath, includeTags=tagCheckbox.get())
            else: # exporting to lexes db
                self.masterApp.selectedList.exportToDB(filePath=filePath, includeTags=tagCheckbox.get())

            topLevel.destroy() # close the export window
            messagebox.showinfo("Export Successful",
                                f"Successfully exported {len(self.masterApp.selectedList.entries)} entries.",
                                parent=self)

        exportButton = ctk.CTkButton(bottomFrame, text="Export", font=("League Spartan Bold", 24), height=50, width=130, text_color=DarkGreen3, corner_radius=5,
                                  border_color=DarkGreen3, fg_color=Cream, hover_color=Cream2, border_width=2.5, command=exportButtonCommand)
        exportButton.pack(side='right', padx=(0,5), pady=0)

    def openImportTextWindow(self) -> None:
            """
            Opens the import window to import raw pasted text (also known as bulk add entries).
            The window allows the user to paste or type raw text, select entry and term-definition delimiters.
            The text can get parsed into individual entries based on the delimiters and definitions can be auto-generated using Wikipedia.
            """
            # Instantiate ImportList object
            importList = ImportList(filePath="",
                                    rawText="",
                                    entryDelimiter="",
                                    termDefinitionDelimiter="",
                                    massTags="",
                                    parsedEntries=[])
            
            ### Popup Window Setup ###
            topLevel = ctk.CTkToplevel(self)
            topLevel.geometry("1280x720")
            topLevel.title("Bulk Add Entries")
            topLevel.resizable(False, False)

            # Make sure it appears above the main window 
            topLevel.lift()
            topLevel.attributes("-topmost", True)
            topLevel.after(10, lambda: topLevel.attributes("-topmost", False))

            # Force focus (keyboard + window manager)
            topLevel.focus_force()
            topLevel.grab_set()  # grabs all inputs (kb and mouse)

            ### UI ###
            background = ctk.CTkFrame(topLevel, corner_radius=0, fg_color=LightGreen2)
            background.pack(fill="both", expand=True)

            # Split the window into two columns.
            columnFrame = ctk.CTkFrame(background, corner_radius=0, fg_color="transparent")
            columnFrame.pack(padx=25, pady=(25,15), fill="both", expand=True)

            leftColumn = ctk.CTkFrame(columnFrame, corner_radius=0, fg_color="transparent", width=1230/2)
            leftColumn.pack(side='left', padx=(0,10), pady=0, fill='y')
            leftColumn.pack_propagate(False)

            rightColumn = ctk.CTkFrame(columnFrame, corner_radius=0, fg_color="transparent", width=1230/2)
            rightColumn.pack(side='right', padx=0, pady=0, fill='y')
            rightColumn.pack_propagate(False)

            # Left Column: Textbox
            importTextbox = ctk.CTkTextbox(leftColumn, font=("League Spartan", 24), text_color=DarkGreen2, fg_color=Cream,
                                           corner_radius=5, height=500, width=574, wrap="word", border_color=DarkGreen3,
                                           border_width=2.5, scrollbar_button_color=DarkGreen3, scrollbar_button_hover_color=ScrollbarGreen)
            importTextbox.pack(padx=0, pady=0, fill="x")

            # Placeholder for importTextbox
            placeholderText = "Paste or type raw text..."
            placeholderColor = Cream3
            normalColor = DarkGreen2

            ### Functions for placeholder text functionality in importTextbox ###
            def showPlaceholder():
                importTextbox.configure(text_color=placeholderColor)
                importTextbox.delete("1.0", tk.END) # clear the textbox before inserting placeholder text
                importTextbox.insert("1.0", placeholderText)
            def hidePlaceholder():
                importTextbox.delete("1.0", tk.END)
                importTextbox.configure(text_color=normalColor)
            def onFocusIn(event):
                if (importTextbox.get("1.0", tk.END).strip() == placeholderText and
                    importTextbox.cget("text_color") == placeholderColor):
                    hidePlaceholder()
            def onFocusOut(event):
                if not importTextbox.get("1.0", tk.END).strip():
                    showPlaceholder()
            
            # Bind placeholder events to textbox
            importTextbox.bind("<FocusIn>", onFocusIn)
            importTextbox.bind("<FocusOut>", onFocusOut)

            # Initialise the textbox with placeholder text
            showPlaceholder()

            # Icon and slider for adjusting the font size of the importTextbox (zoom)
            sliderFrame = ctk.CTkFrame(leftColumn, corner_radius=0, fg_color="transparent")
            sliderFrame.pack(padx=0, pady=(7.5,0), fill='x')

            ctkZoomIconImage = ctk.CTkImage(light_image=zoomIconImage, dark_image=zoomIconImage, size=(32,32))
            zoomIcon = ctk.CTkLabel(sliderFrame, image=ctkZoomIconImage, text="", fg_color="transparent")
            zoomIcon.pack(side='left', padx=(2.5,10), pady=0)

            fontSizeSlider = ctk.CTkSlider(sliderFrame, from_=10, to=32, number_of_steps=22,
                                           command=lambda value: importTextbox.configure(font=("League Spartan", int(value))),
                                           fg_color=Cream, button_color=DarkGreen3, button_hover_color=ScrollbarGreen, progress_color=DarkGreen2,
                                           border_color=DarkGreen3, border_width=2.5, height=15, corner_radius=5)
            fontSizeSlider.set(24)
            fontSizeSlider.pack(padx=0, pady=(0,1), fill='x', side='left', expand=True)

            # Left Column: Parse Button
            def parseButtonCommand() -> None:
                """
                Validates the input in the importTextbox and the selected delimiters from the dropdowns.
                Parses the text from the importTextbox and adds reinserts entries into the importTextbox.
                Can generate definitions automatically using Wikipedia if the term is missing a definition.
                """
                # Check if importTextbox is empty or contains only placeholder text
                if importTextbox.get("1.0", tk.END).strip() == placeholderText or not importTextbox.get("1.0", tk.END).strip():
                    messagebox.showwarning("Empty Text",
                                           "Please paste or type raw text to parse and import.",
                                           parent=topLevel)
                    return
                # Check if dropdowns are selected
                if not entryDelimiterDropdown.get_selected() or not termDefinitionDelimiterDropdown.get_selected():
                    messagebox.showwarning("Missing Delimiters",
                                           "Please select both entry and term-definition delimiters.",
                                           parent=topLevel)
                    return

                # Get values from the importTextbox and dropdowns
                rawText = importTextbox.get("1.0", tk.END).strip()
                entryDelimiter = entryDelimiterDropdown.get_selected()
                termDefinitionDelimiter = termDefinitionDelimiterDropdown.get_selected()
                
                # Setup delimiter value mapping
                entryDelimiterMap = {
                    "Line Break (Default)": "\n+",
                    "Semicolon": ";",
                    "Comma": ","
                }

                termDefinitionDelimiterMap = {
                    "Colon (Default)": ":",
                    "Hyphen": "-",
                    "Equals": "="
                }

                entryDelimiter = entryDelimiterMap.get(entryDelimiter, "\n")  # Default to line break if not selected (but should always be selected since we validated above)
                termDefinitionDelimiter = termDefinitionDelimiterMap.get(termDefinitionDelimiter, ":")  # Default to colon if not selected

                # Update importList object with new parameters
                importList.rawText = rawText
                importList.entryDelimiter = entryDelimiter
                importList.termDefinitionDelimiter = termDefinitionDelimiter

                successfulParse, trialParsedEntries = importList.parseText()

                # Clear the importTextbox before inserting parsed entries (regardless of success)
                importTextbox.delete("1.0", tk.END)

                if successfulParse:
                    """
                    Update UI with parsed entries (attempted). For each parsed "entry" (really a tuple of strings), add to the importTextbox
                    entries delimited by line breaks and term-definition pairs delimited by the selected colon ':' (system-default/recommended)
                    """
                    for entry in trialParsedEntries:
                        term, definition = entry
                        importTextbox.insert("end", f"{term}: {definition}\n")
                    
                    messagebox.showinfo("Parse Successful",
                                        f"Successfully parsed {len(trialParsedEntries)} entries.",
                                        parent=topLevel)
                else:
                    """
                    Either a term was missing or a definition was missing (and failed to auto-retrieve), so insert the entries back into the importTextbox
                    entries and term-definition pairs delimited by the user's originally selected delimiters (may not be system-default or recommended)
                    """
                    for entry in trialParsedEntries:
                        term, definition = entry
                        importTextbox.insert("end", f"{term}{termDefinitionDelimiter}{definition}\n")

                    messagebox.showerror("Parse Incomplete",
                                         "Some entries could not be parsed. Either a term or a definition is missing. Please review your input and try again.",
                                         parent=topLevel)

            parseButton = ctk.CTkButton(leftColumn, text="Parse", font=("League Spartan Bold", 24), height=50, width=130,
                                        text_color=Pink, corner_radius=5, border_color=Pink, fg_color=Cream,
                                        hover_color=Cream2, border_width=2.5, command=parseButtonCommand)
            parseButton.pack(side='bottom', padx=0, pady=0)

            # Right Column: Entry delimiter label and selection
            entryDelimiterFrame = ctk.CTkFrame(rightColumn, corner_radius=0, fg_color="transparent")
            entryDelimiterFrame.pack(padx=0, pady=0, fill='x')

            ctkEntryDelimiterIcon = ctk.CTkImage(dark_image=entryDelimiterIconImage, light_image=entryDelimiterIconImage, size=(35,34))
            entryDelimiterIcon = ctk.CTkLabel(entryDelimiterFrame, image=ctkEntryDelimiterIcon, text="", fg_color="transparent")
            entryDelimiterIcon.pack(side='left', padx=0, pady=0)
            entryDelimiterLabel = ctk.CTkLabel(entryDelimiterFrame, text="Delimit entries by:", font=("League Spartan", 36), text_color=DarkGreen2)
            entryDelimiterLabel.pack(padx=(15,0), pady=(0,7), side='left')

            entryDelimiterOptions = ["Line Break (Default)", "Semicolon", "Comma"]
            entryDelimiterDropdown = SingleSelectComboBox(rightColumn,
                                                          options=entryDelimiterOptions,
                                                          font=("League Spartan", 32),
                                                          dropdown_font=("League Spartan", 24),
                                                          fg_color=Cream,
                                                          text_color=Cream3,
                                                          corner_radius=5,
                                                          width=285,
                                                          height=50,
                                                          border_width=2.5,
                                                          border_color=DarkGreen3,
                                                          selected_bg_color=DarkGreen3,
                                                          selected_text_color=Cream,
                                                          unselected_text_color=DarkGreen3,
                                                          default_text="Select delimiter character",
                                                          dropdown_bg_color=DarkGreen1b,
                                                          on_close_callback=None,
                                                          ipadx=(10,0))
        
            entryDelimiterDropdown.pack(padx=(0,30), pady=(0,0), fill='x')

            # Right Column: Term definition delimiter label and selection
            termDefinitionDelimiterFrame = ctk.CTkFrame(rightColumn, corner_radius=0, fg_color="transparent")
            termDefinitionDelimiterFrame.pack(padx=0, pady=(40,0), fill='x')

            ctkTermDefinitionDelimiterIcon = ctk.CTkImage(dark_image=termDefinitionDelimiterIconImage, light_image=termDefinitionDelimiterIconImage, size=(35,34))
            termDefinitionDelimiterIcon = ctk.CTkLabel(termDefinitionDelimiterFrame, image=ctkTermDefinitionDelimiterIcon, text="", fg_color="transparent")
            termDefinitionDelimiterIcon.pack(side='left', padx=0, pady=0)
            termDefinitionDelimiterLabel = ctk.CTkLabel(termDefinitionDelimiterFrame, text="Delimit term-definitions by:", font=("League Spartan", 36), text_color=DarkGreen2)
            termDefinitionDelimiterLabel.pack(padx=(15,0), pady=(0,7), side='left')

            termDefinitionDelimiterOptions = ["Colon (Default)", "Hyphen", "Equals"]

            termDefinitionDelimiterDropdown = SingleSelectComboBox(rightColumn,
                                                          options=termDefinitionDelimiterOptions,
                                                          font=("League Spartan", 32),
                                                          dropdown_font=("League Spartan", 24),
                                                          fg_color=Cream,
                                                          text_color=Cream3,
                                                          corner_radius=5,
                                                          width=285,
                                                          height=50,
                                                          border_width=2.5,
                                                          border_color=DarkGreen3,
                                                          selected_bg_color=DarkGreen3,
                                                          selected_text_color=Cream,
                                                          unselected_text_color=DarkGreen3,
                                                          default_text="Select delimiter character",
                                                          dropdown_bg_color=DarkGreen1b,
                                                          on_close_callback=None,
                                                          ipadx=(10,0))
            termDefinitionDelimiterDropdown.pack(padx=(0,30), pady=(0,0), fill='x')

            # Right Column: Mass tags label and entry. (Optional for user input)
            massTagsFrame = ctk.CTkFrame(rightColumn, corner_radius=0, fg_color="transparent")
            massTagsFrame.pack(padx=0, pady=(40,0), fill='x')

            ctkMassTagsIcon = ctk.CTkImage(dark_image=tagLightIconImage, light_image=tagLightIconImage, size=(37,37))
            massTagsIcon = ctk.CTkLabel(massTagsFrame, image=ctkMassTagsIcon, text="", fg_color="transparent")
            massTagsIcon.pack(side='left', padx=0, pady=0)
            massTagsLabel = ctk.CTkLabel(massTagsFrame, text="Mass tags (optional):", font=("League Spartan", 36), text_color=DarkGreen2)
            massTagsLabel.pack(padx=(15,0), pady=(0,7), side='left')

            massTagsEntry = ctk.CTkEntry(rightColumn, placeholder_text="e.g. nuclear_physics biology vce", font=("League Spartan", 32),
                                         placeholder_text_color=Cream3, text_color=DarkGreen2, fg_color=Cream, border_color=DarkGreen3,
                                         border_width=2.5, height=50)
            massTagsEntry.pack(padx=(0,30), pady=(0,0), fill='x')

            # Right Column: Navigation Buttons (bottom right)
            buttonFrame = ctk.CTkFrame(rightColumn, corner_radius=0, fg_color="transparent")
            buttonFrame.pack(padx=0, pady=0, anchor='se', side='bottom')

            def cancelButtonCommand() -> None:
                """
                Closes the import window without saving any changes.
                """
                topLevel.destroy()
            cancelButton = ctk.CTkButton(buttonFrame, text="Cancel", font=("League Spartan Bold", 24), height=50, width=130, text_color=Red, corner_radius=5,
                                     border_color=Red, fg_color=Cream, hover_color=Cream2, border_width=2.5, command=cancelButtonCommand)
            cancelButton.pack(side='right', padx=(0,30), pady=0)

            def importButtonCommand() -> None:
                """
                Initiates the import process for the raw text.
                Validates the input in the importTextbox, checks if delimiters are selected,
                retrieves mass tags if provided, and validates the entries.
                If all validations pass, it imports the entries into the database and updates the main app UI.
                """
                # Check if the importTextbox is empty or contains only placeholder text
                if importTextbox.get("1.0", tk.END).strip() == placeholderText or not importTextbox.get("1.0", tk.END).strip():
                    messagebox.showwarning("Empty Text",
                                           "Please paste or type raw text to import.",
                                           parent=topLevel)
                    return
                
                # Check if all dropdowns have a selected value
                if not entryDelimiterDropdown.get_selected() or not termDefinitionDelimiterDropdown.get_selected():
                    proceed = messagebox.askyesno("Missing Delimiters",
                                           "Delimiters have not been selected. Current operations will use values of:\n- Line Break (Default)\n- Colon (Default)\nDo you wish to proceed?",
                                           parent=topLevel)
                    if proceed == False:
                        return
                
                importList.massTags = massTagsEntry.get().strip()
                importList.rawText = importTextbox.get("1.0", tk.END).strip()

                # Validate entries (uses rawText which should have been parsed)
                isValid = importList.validateEntries()
                if not isValid:
                    messagebox.showerror("Invalid Entries",
                                         "Some entries are invalid. Please review or re-parse the text and try again.",
                                         parent=topLevel)
                    return
                
                # Import the validated entries into the database
                count = importList.importAndClear()

                # Clear importTextbox, close window
                importTextbox.delete("1.0", tk.END)
                topLevel.destroy()

                # Update the main app UI, show success message
                self.updateUI()
                messagebox.showinfo("Import Successful",
                                     f"Successfully imported {count} entries.",
                                     parent=self)

            importButton = ctk.CTkButton(buttonFrame, text="Import", font=("League Spartan Bold", 24), height=50, width=130, text_color=DarkGreen3, corner_radius=5,
                                    border_color=DarkGreen3, fg_color=Cream, hover_color=Cream2, border_width=2.5, command=importButtonCommand)
            importButton.pack(side='right', padx=(0,5), pady=0)

            # Footer
            footer = ctk.CTkFrame(background, corner_radius=0, fg_color=LightGreen1, height=80)
            footer.pack(fill='x', side='bottom', pady=0, padx=0)
            footer.pack_propagate(False)

            ctkIconImage = ctk.CTkImage(light_image=iconImage, dark_image=iconImage, size=(65,65))
            footerIcon = ctk.CTkLabel(footer, image=ctkIconImage, text="", anchor='center')
            footerIcon.pack(expand=True)

    def openImportDBWindow(self) -> None: # Opens the import window to import a Lexes DB file.
        """
        Opens the import window to import a Lexes DB file.
        The window allows the user to select a Lexes DB file and preview the file before import.
        Mass tags can be added to all entries in the database.
        """
        ### Popup Window Setup ###
        topLevel = ctk.CTkToplevel(self)
        topLevel.geometry("1280x720")
        topLevel.title("Import Database")
        topLevel.resizable(False, False)

        # Make sure it appears above the main window 
        topLevel.lift()
        topLevel.attributes("-topmost", True)
        topLevel.after(10, lambda: topLevel.attributes("-topmost", False))

        # Force focus (keyboard + window manager)
        topLevel.focus_force()
        topLevel.grab_set()  # grabs all inputs (kb and mouse)

        background = ctk.CTkFrame(topLevel, corner_radius=0, fg_color=LightGreen2)
        background.pack(fill="both", expand=True)
        
        # Initiate importList object
        importList = ImportList(filePath="",
                                massTags="",
                                parsedEntries=[])
        
        # Max Widths For Columns
        termWidth = 220
        definitionWidth = 660
        tagsWidth = 330
        
        def populatePreviewBox(entries) -> None:
            """
            Populates the preview box with entries from the database.
            Limits to the first 100 entries for performance.
            """
            entries = entries[:100]

            # Clear previous rows (except header)
            for widget in previewScrollable.winfo_children()[3:]:
                widget.destroy()
            # Add new rows
            for i, (term, definition, tags) in enumerate(entries):
                # Use rowFont tuple for font family and size
                fontFamily = rowFont[0]
                fontSize = rowFont[1]
                fontWeight = "normal"

                # Use MainWindow truncateText method to truncate
                truncatedTerm = self.truncateText(str(term), maxWidth=termWidth-50, size=fontSize, font=fontFamily, weight=fontWeight)
                truncatedDefinition = self.truncateText(str(definition), maxWidth=definitionWidth - 50, size=fontSize, font=fontFamily, weight=fontWeight)
                truncatedTags = self.truncateText(str(tags), maxWidth=tagsWidth - 50, size=fontSize, font=fontFamily, weight=fontWeight)

                ctk.CTkLabel(previewScrollable, text=truncatedTerm, font=rowFont, text_color=rowColor,
                             anchor="w", width=termWidth).grid(row=i, column=0, sticky="w", padx=(8, 8))
                ctk.CTkLabel(previewScrollable, text=truncatedDefinition, font=rowFont, text_color=rowColor,
                             anchor="w", width=definitionWidth).grid(row=i, column=1, sticky="w", padx=(8, 8))
                ctk.CTkLabel(previewScrollable, text=truncatedTags, font=rowFont, text_color=rowColor,
                             anchor="w", width=tagsWidth).grid(row=i, column=2, sticky="w", padx=(8, 8))

        def onFileSelected(filepath) -> None:
            """
            Callback function for when a file is selected in the importDirectoryEntry.
            Reads the database file at filepath, extracts entries, and populates the preview box.
            Updates the chosenFile label with the file name and number of entries.
            """
            fileName = os.path.basename(filepath)

            # Read the database file at filepath and extract entries
            with sqlite3.connect(filepath) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT term, definition, tags FROM master")
                entries = cursor.fetchall()
                count = len(entries)

                populatePreviewBox(entries)
                previewScrollable._parent_canvas.yview_moveto(0)

            chosenFile.configure(text=f"{fileName} ({count} entries)")  # Update the label with the selected file name and number of entries

        # Import from label and file directory selection and preview
        importFromLabel = ctk.CTkLabel(background, text="Import database from:", font=("League Spartan", 48), text_color=DarkGreen2)
        importFromLabel.pack(padx=35, pady=(15,0), anchor='nw')

        importDirectoryEntry = SelectFilePathEntry(background, font=("League Spartan", 36), text_color=Cream3, fg_color=Cream, border_color=DarkGreen3,
                                             border_width=2.5, placeholder_text="Select file path...", icon=folderIconImage, icon_size=(46,36),
                                             file_type=".db", on_callback=onFileSelected)
        importDirectoryEntry.pack(padx=35, pady=0, fill="x")

        # Preview Box Frame
        previewBoxFrame = ctk.CTkFrame(background, corner_radius=8, fg_color=Cream, border_color=DarkGreen3, border_width=2.5, height=195)
        previewBoxFrame.pack(padx=35, pady=(20,0), fill="x")
        previewBoxFrame.pack_propagate(False)  # Keep fixed height

        # Colours and Fonts for Preview
        headerFont = ("Bahnschrift Bold", 16)
        headerColor = Cream3
        rowFont = ("Bahnschrift", 16)
        rowColor = Cream4

        # Header frame (external to the scrollable frame)
        headerFrame = ctk.CTkFrame(previewBoxFrame, corner_radius=0, fg_color="transparent")
        headerFrame.pack(fill="x", padx=2.5, pady=(2.5,0))

        termHeader = ctk.CTkLabel(headerFrame, text="Term", font=headerFont, text_color=headerColor, anchor="w", width=termWidth-12)
        termHeader.grid(row=0, column=0, sticky="w", padx=8, pady=0)
        termHeader.grid_propagate(False)

        definitionHeader = ctk.CTkLabel(headerFrame, text="Definition", font=headerFont, text_color=headerColor, anchor="w", width=definitionWidth-38)
        definitionHeader.grid(row=0, column=1, sticky="w", padx=8, pady=0)
        definitionHeader.grid_propagate(False)

        tagsHeader = ctk.CTkLabel(headerFrame, text="Tags", font=headerFont, text_color=headerColor, anchor="w", width=tagsWidth)
        tagsHeader.grid(row=0, column=2, sticky="w", padx=8, pady=0)
        tagsHeader.grid_propagate(False)

        # Scrollable Frame inside Preview Box
        previewScrollable = ctk.CTkScrollableFrame(previewBoxFrame, fg_color="transparent", width=10, height=210, corner_radius=0,
                                                   scrollbar_button_color=Cream3, scrollbar_button_hover_color=Cream4, scrollbar_fg_color="transparent")
        previewScrollable.pack(expand=True, fill="both", padx=2.5, pady=2.5)

        # Configure column weights for even distribution
        previewScrollable.grid_columnconfigure(0, weight=2)
        previewScrollable.grid_columnconfigure(1, weight=6)
        previewScrollable.grid_columnconfigure(2, weight=3)
        
        chosenFileLabel = ctk.CTkLabel(background, text="Chosen File:", font=("Bahnschrift", 24), text_color=DarkGreen2)
        chosenFileLabel.pack(padx=35, pady=(5,0), anchor='nw')
        chosenFile = ctk.CTkLabel(background, text="", font=("Bahnschrift", 24), text_color=DarkGreen2)
        chosenFile.pack(padx=35, pady=0, anchor='nw')

        # Footer
        footer = ctk.CTkFrame(background, corner_radius=0, fg_color=LightGreen1, height=80)
        footer.pack(fill='x', side='bottom', pady=0, padx=0)
        footer.pack_propagate(False)

        ctkIconImage = ctk.CTkImage(light_image=iconImage, dark_image=iconImage, size=(65,65))
        footerIcon = ctk.CTkLabel(footer, image=ctkIconImage, text="", anchor='center')
        footerIcon.pack(expand=True)

        # Bottom Frame for buttons and mass tagging
        bottomFrame = ctk.CTkFrame(background, corner_radius=0, fg_color="transparent")
        bottomFrame.pack(padx=35, pady=(0,20), fill="x", side='bottom')

        # Button frame
        buttonFrame = ctk.CTkFrame(bottomFrame, corner_radius=0, fg_color="transparent")
        buttonFrame.pack(side="right", fill="x", padx=0, pady=0, anchor='s')

        def cancelButtonCommand() -> None:
            """
            Closes the import window without saving any changes.
            """
            topLevel.destroy()
        cancelButton = ctk.CTkButton(buttonFrame, text="Cancel", font=("League Spartan Bold", 24), height=50, width=130,
            text_color=Red, corner_radius=5, border_color=Red, fg_color=Cream,
            hover_color=Cream2, border_width=2.5, command=cancelButtonCommand)
        cancelButton.pack(side="right", padx=(0, 0), pady=0)

        def importButtonCommand() -> None:
            """
            Validates and imports the selected database file.
            Conditions for validation:
            - A file path must be selected.
            - The table must be called 'master'.
            - The table must contain columns: term, definition, tags (in that order).
            - The table must contain at least one entry.
            If all validations pass, it imports the entries into the database and updates the main app UI.
            """
            # File path selected
            if not importDirectoryEntry.get_path():
                messagebox.showwarning("No File Path Selected",
                                       "Please select a file path to import database from.",
                                       parent=topLevel)
                return

            # Table is called 'master'
            with sqlite3.connect(importDirectoryEntry.get_path()) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='master'")
                if not cursor.fetchone():
                    messagebox.showerror("Invalid Database",
                                         "The selected database does not contain a 'master' table. Please select a valid Lexes database file.",
                                         parent=topLevel)
                    return

            # Table contains correct columns.
            with sqlite3.connect(importDirectoryEntry.get_path()) as conn:
                cursor = conn.cursor()
                cursor.execute("PRAGMA table_info(master)")
                columns = [col[1] for col in cursor.fetchall()]
                expectedColumns = ["uid", "term", "definition", "tags"]
                if columns != expectedColumns:
                    messagebox.showerror("Invalid Database",
                                         "The selected database does not contain the required columns: term, definition, tags. Please select a valid Lexes database file.",
                                         parent=topLevel)
                    return

            # Table isn't empty.
            with sqlite3.connect(importDirectoryEntry.get_path()) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM master")
                count = cursor.fetchone()[0]
                if count == 0:
                    messagebox.showerror("Empty Database",
                                         "The selected database is empty. Please select a valid Lexes database file.",
                                         parent=topLevel)
                    return

            # If we reach here, all validations passed
            
            # Update importList with the file path and mass tags
            importList.filePath = importDirectoryEntry.get_path().strip()
            importList.massTags = massTagsEntry.get().strip()
            
            # Add DB entries to importList.parsedEntries
            importList.importDB()
            count = importList.importAndClear() # imports and stores imported entry count

            topLevel.destroy()

            # Update the main app UI, show success message
            self.updateUI()
            messagebox.showinfo("Import Successful",
                                    f"Successfully imported {count} entries.",
                                    parent=self)

        importButton = ctk.CTkButton(buttonFrame, text="Import", font=("League Spartan Bold", 24), height=50, width=130,
            text_color=DarkGreen3, corner_radius=5, border_color=DarkGreen3, fg_color=Cream,
            hover_color=Cream2, border_width=2.5, command=importButtonCommand)
        importButton.pack(side="right", padx=(0, 5), pady=0)

        # Mass Tags Label and Entry
        massTagsFrame = ctk.CTkFrame(bottomFrame, corner_radius=0, fg_color="transparent", width=560)
        massTagsFrame.pack(padx=0, pady=0, side='left')

        massTagsLabelFrame = ctk.CTkFrame(massTagsFrame, corner_radius=0, fg_color="transparent")
        massTagsLabelFrame.pack(padx=0, pady=0, fill='x')
        
        ctkMassTagsIcon = ctk.CTkImage(dark_image=tagLightIconImage, light_image=tagLightIconImage, size=(37,37))
        massTagsIcon = ctk.CTkLabel(massTagsLabelFrame, image=ctkMassTagsIcon, text="", fg_color="transparent")
        massTagsIcon.pack(side='left', padx=0, pady=0)
        massTagsLabel = ctk.CTkLabel(massTagsLabelFrame, text="Mass tags (optional):", font=("League Spartan", 36), text_color=DarkGreen2)
        massTagsLabel.pack(padx=(15,0), pady=(0,7), side='left')

        massTagsEntry = ctk.CTkEntry(massTagsFrame, placeholder_text="e.g. nuclear_physics biology vce", font=("League Spartan", 32),
                                        placeholder_text_color=Cream3, text_color=DarkGreen2, fg_color=Cream, border_color=DarkGreen3,
                                        border_width=2.5, height=50, width=578)
        massTagsEntry.pack(padx=0, pady=(0,0))
    
    def openSettingsWindow(self) -> None: # Opens the settings window to adjust application settings.
        """
        Opens the settings window to change the app settings.
        Window allows the user to set whether the app pre-load the tags entry with the last used tag, a default tag, or no tag at all.
        Also allows the user to full reset the database which will delete all entry rows, but also reset the auto-increment UID counter back to 1.
        This will allow the user to start fresh with a new database, but will not delete the database file itself
        NOTE: Should ask the user to confirm they know what they are doing.
        TBA: Graph for showing the number of entries in the database, and the tag distribution, and timeline on database growth.
        """
        ### Popup Window Setup ###
        topLevel = ctk.CTkToplevel(self)
        topLevel.geometry("1280x720")
        topLevel.title("Settings")
        topLevel.resizable(False, False)

        # Make sure it appears above the main window 
        topLevel.lift()
        topLevel.attributes("-topmost", True)
        topLevel.after(10, lambda: topLevel.attributes("-topmost", False))

        # Force focus (keyboard + window manager)
        topLevel.focus_force()
        topLevel.grab_set()  # grabs all inputs (kb and mouse)

        background = ctk.CTkFrame(topLevel, corner_radius=0, fg_color=LightGreen2)
        background.pack(fill="both", expand=True)

        ### Tags Autofill Settings ###
        tagsAutofillFrame = ctk.CTkFrame(background, corner_radius=0, fg_color="transparent")
        tagsAutofillFrame.pack(padx=(30,0), pady=(30,0), fill='x')

        # Label 
        ctkTagsAutofillIcon = ctk.CTkImage(dark_image=tagLightIconImage, light_image=tagLightIconImage, size=(37,37))
        tagsAutofillIcon = ctk.CTkLabel(tagsAutofillFrame, image=ctkTagsAutofillIcon, text="", fg_color="transparent")
        tagsAutofillIcon.pack(side='left', padx=0, pady=0)
        autoFillLabel = ctk.CTkLabel(tagsAutofillFrame, text="Autofill Tags Settings", font=("League Spartan", 36), text_color=DarkGreen2)
        autoFillLabel.pack(padx=(15,0), pady=(0,7), side='left')

        # Dropdown
        def tagsAutofillDropdownCommand(selectedOption) -> None:
            """
            Callback function for when the tags autofill dropdown is closed.
            Packs the "default tags" entry if "Default" is selected.
            Else hides it.
            """
            if selectedOption == "Default":
                if not defaultTagsEntry.winfo_ismapped(): # pack only if not already packed
                    defaultTagsFrame.pack(padx=(30,0), pady=(20,0), fill='x') 
                    defaultTagsEntry.pack(padx=30, pady=0, anchor='w')

                # Read the current default tags from DEFAULTTAGSPATH and set it in the entry
                try:
                    with open(DEFAULTTAGSPATH, 'r', encoding='utf-8') as defaultTagsFile:
                        defaultTags = defaultTagsFile.read().strip()
                        if defaultTags:  # Only set if not empty
                            defaultTagsEntry.delete(0, 'end')  # Clear the entry first
                            defaultTagsEntry.insert(0, defaultTags)
                except FileNotFoundError:
                    # if the file doesn't exist, do nothing
                    pass
            else:
                background.focus_set()  # Remove focus
                defaultTagsEntry.delete(0, 'end')  # Clear the entry
                defaultTagsEntry.pack_forget()
                defaultTagsFrame.pack_forget()
        
        tagsAutofillOptions = ["Last Used", "Default", "None"]
        tagsAutofillDropdown = SingleSelectComboBox(background,
                                                        options=tagsAutofillOptions,
                                                        font=("League Spartan", 32),
                                                        dropdown_font=("League Spartan", 24),
                                                        fg_color=Cream,
                                                        text_color=Cream3,
                                                        corner_radius=5,
                                                        width=500,
                                                        height=60,
                                                        border_width=2.5,
                                                        border_color=DarkGreen3,
                                                        selected_bg_color=DarkGreen3,
                                                        selected_text_color=Cream,
                                                        unselected_text_color=DarkGreen3,
                                                        default_text="Select tag autofill option...",
                                                        dropdown_bg_color=DarkGreen1b,
                                                        on_close_callback=tagsAutofillDropdownCommand,
                                                        ipadx=(10,0))



        ### Default Tags ###
        defaultTagsFrame = ctk.CTkFrame(background, corner_radius=0, fg_color="transparent")
        # defaultTagsFrame.pack(padx=(30,0), pady=(20,0), fill='x') 
        # Hidden by default, shown if "Default" is selected in the dropdown

        # Label 
        ctkdefaultTagsIcon = ctk.CTkImage(dark_image=tagLightIconImage, light_image=tagLightIconImage, size=(37,37))
        defaultTagsIcon = ctk.CTkLabel(defaultTagsFrame, image=ctkdefaultTagsIcon, text="", fg_color="transparent")
        defaultTagsIcon.pack(side='left', padx=0, pady=0)
        defaultTagsLabel = ctk.CTkLabel(defaultTagsFrame, text="Default Tags", font=("League Spartan", 36), text_color=DarkGreen2)
        defaultTagsLabel.pack(padx=(15,0), pady=(0,7), side='left')

        # Default tags entry (Hidden by default, shown if "Default" is selected in the dropdown)
        defaultTagsEntry = ctk.CTkEntry(background, placeholder_text="e.g. nuclear_physics biology vce", font=("League Spartan", 32),
                                 placeholder_text_color=Cream3, text_color=DarkGreen2, fg_color=Cream, border_color=DarkGreen3,
                                 border_width=2.5, width=1000)
        # defaultTagsEntry.pack(padx=30, pady=0, anchor='w')
        # Hidden by default, shown if "Default" is selected in the dropdown

        ### Auto Select the Current Tags Autofill Option ###
        # Read the current tags autofill option from TAGSPREFERENCEPATH and translate
        TAGSPREFERENCEMAP = {
            "last_used": "Last Used",
            "default": "Default",
            "none": "None"
        }
        try:
            with open(TAGSPREFERENCEPATH, 'r', encoding='utf-8') as file:
                autofillOption = file.read().strip()
                if autofillOption in TAGSPREFERENCEMAP:
                    tagsAutofillDropdown.set_selected_option(TAGSPREFERENCEMAP[autofillOption])
                tagsAutofillDropdown.pack(padx=(30,0), pady=(0,0), anchor='w')
                if autofillOption == "default":
                    # Pack the default tags entry if "Default" is selected and fill it with the current default tag
                    defaultTagsFrame.pack(padx=(30,0), pady=(20,0), fill='x')
                    defaultTagsEntry.pack(padx=30, pady=0, anchor='w')
                    try:
                        with open(DEFAULTTAGSPATH, 'r', encoding='utf-8') as defaultTagsFile:
                            defaultTags = defaultTagsFile.read().strip()
                            if defaultTags:  # Only set if not empty
                                defaultTagsEntry.insert(0, defaultTags)
                    except FileNotFoundError:
                        # if the file doesn't exist, do nothing
                        pass
        except FileNotFoundError:
            # if the file doesn't exist do nothing
            pass

        # Footer
        footer = ctk.CTkFrame(background, corner_radius=0, fg_color=LightGreen1, height=80)
        footer.pack(fill='x', side='bottom', pady=0, padx=0)
        footer.pack_propagate(False)

        ctkIconImage = ctk.CTkImage(light_image=iconImage, dark_image=iconImage, size=(65,65))
        footerIcon = ctk.CTkLabel(footer, image=ctkIconImage, text="", anchor='center')
        footerIcon.pack(expand=True)

        # Window Navigation Buttons
        buttonFrame = ctk.CTkFrame(background, corner_radius=0, fg_color="transparent")
        buttonFrame.pack(padx=0, pady=(0,20), fill="x", side='bottom')

        def cancelButtonCommand() -> None:
            """
            Closes the add entry window without saving any changes.
            """
            topLevel.destroy()
        cancelButton = ctk.CTkButton(buttonFrame, text="Close", font=("League Spartan Bold", 24), height=50, width=130, text_color=Red, corner_radius=5,
                                     border_color=Red, fg_color=Cream, hover_color=Cream2, border_width=2.5, command=cancelButtonCommand)
        cancelButton.pack(side='right', padx=(0,35), pady=0)

        def saveButtonCommand() -> None:
            """
            Saves the settings and closes the window.
            - Saves the tags autofill option selected in the dropdown to TAGSPREFERENCEPATH.
            - If "Default" is selected, also saves the default tags entry to DEFAULTTAGSPATH.
            """
            autofillOption = tagsAutofillDropdown.get_selected()

            # Save autofill option
            if autofillOption == "Last Used": # Write "last_used" to TAGSPREFERENCEPATH file
                with open(TAGSPREFERENCEPATH, 'w', encoding='utf-8') as file:
                    file.write("last_used")
            
            elif autofillOption == "Default": # Write to TAGSPREFERENCEPATH file and also save default tags
                defaultTags = defaultTagsEntry.get().strip()
                if not defaultTags:  # If the entry is empty, show a warning
                    messagebox.showwarning("Empty Default Tags",
                                               "Default tags entry is empty. Please enter default tags or select 'None' to disable.",
                                               parent=topLevel)
                    return
                with open(TAGSPREFERENCEPATH, 'w', encoding='utf-8') as file: # Write "default" to TAGSPREFERENCEPATH file
                    file.write("default")
                
                with open(DEFAULTTAGSPATH, 'w', encoding='utf-8') as defaultTagsFile: # Write the default tags to DEFAULTTAGSPATH file
                    defaultTagsFile.write(defaultTags)

            elif autofillOption == "None": # Write "none" to TAGSPREFERENCEPATH file
                with open(TAGSPREFERENCEPATH, 'w', encoding='utf-8') as file:
                    file.write("none")
            
            else: # fallback write "last_used" to TAGSPREFERENCEPATH file as the application default
                with open(TAGSPREFERENCEPATH, 'w', encoding='utf-8') as file:
                    file.write("last_used")
            
            topLevel.destroy()  # Close the settings window
            messagebox.showinfo("Settings Saved",
                                    f"Successfully changed tags autofill setting to '{autofillOption}'.",
                                    parent=self)

        saveButton = ctk.CTkButton(buttonFrame, text="Save", font=("League Spartan Bold", 24), height=50, width=130, text_color=DarkGreen3, corner_radius=5,
                                   border_color=DarkGreen3, fg_color=Cream, hover_color=Cream2, border_width=2.5, command=saveButtonCommand)
        saveButton.pack(side='right', padx=(0,5), pady=0)

        ### Reset Database ###        
        def resetDatabase() -> None:
            """
            Resets the database by deleting all entries and resetting the UID counter.
            Asks for confirmation before proceeding.
            """
            confirm = messagebox.askyesno("Reset Database",
                                          "Are you sure you want to reset the database? This will DELETE ALL ENTRIES and reset the UID counter.\nThis action cannot be undone.",
                                          parent=topLevel)
            if not confirm:
                return
            try:
                with sqlite3.connect(DBPATH) as conn:
                    cursor = conn.cursor()
                    # Delete all entries in the master table
                    cursor.execute("DELETE FROM master")

                    # Reset the UID counter by deleting the uid table
                    cursor.execute("DELETE FROM sqlite_sequence WHERE name='master'")
                
                topLevel.destroy()  # Close the settings window
                self.updateUI()  # Update the main app UI
                messagebox.showinfo("Database Reset",
                                    "Database successfully reset. All entries have been deleted and the UID counter has been reset.",
                                    parent=self)
            except sqlite3.Error as e:
                messagebox.showerror("Database Error",
                                     f"An error occurred while resetting the database: {e}",
                                     parent=topLevel)

        ctkResetDatabaseIcon = ctk.CTkImage(dark_image=dangerIconImage, light_image=dangerIconImage, size=(30,27))
        resetDatabaseButton = ctk.CTkButton(buttonFrame, text="Reset Database", font=("League Spartan Bold", 24), height=50, width=225,
                                            text_color=Red, corner_radius=5, border_color=Red, fg_color=Cream, hover_color=Cream2,
                                            image=ctkResetDatabaseIcon, border_width=2.5, command=resetDatabase)
        resetDatabaseButton.pack(padx=30, pady=0, side='left')

    def applyCustomScaling(self) -> None:
        """
        Apply custom scaling to the application window and widgets.
        This method checks the current DPI scaling of the display and adjusts the scaling of the application window and widgets accordingly.
        
        For example:
            Since Lexes was designed and developed on 100% DPI, if the device's DPI is set to 125%,
            the application will scale down to 100% to maintain consistent sizing.
        """
        user32 = ctypes.windll.user32 
        gdi32 = ctypes.windll.gdi32

        hdc = user32.GetDC(0)
        dpi = gdi32.GetDeviceCaps(hdc, 88) # returns DPI (dots per inch)
        user32.ReleaseDC(0, hdc)

        """
        Since 96 DPI (default) is 100%, by dividing the current DPI by 96 and multiplying by 100,
        we get the scaling percentage.
        """
        scalingPercent = int((dpi / 96) * 100)

        if scalingPercent != 100:
            # scale is not 100%, manipulate to get to 100%
            scale = 100/scalingPercent
            ctk.set_window_scaling(scale)
            ctk.set_widget_scaling(scale)
        else:
            # scale is already 100%, so set to 1.0 to keep it at 100%
            ctk.set_window_scaling(1.0)
            ctk.set_widget_scaling(1.0)
        
    def updateDictionaryUI(self) -> None:
        """
        Updates only the dictionary UI.
        Clears the selected entries, to reset all entries highlighted.
        Rebuilds the display list and populates the dictionary list with the entries filtered through the new parameters.
        Also updates the select all toggle state to be unselected as all entries are now unselected and calls delete button to update its state.
        Shows or hides info message on dictionary list to indicate no entries shown.

        This method is called after any change to the dictionary list, such as filtering, adding, deleting, or editing entries.
        """
        self.dictionaryList.hide_empty_message()

        self.masterApp.selectedList.entries.clear()  # clear selected entries
        self.masterApp.displayList.build()  # rebuild filtered list
        self.dictionaryList.entries = self.masterApp.displayList.entries
        self.dictionaryList.populate()  # refresh list UI
        self.selectAllToggle.set_state(False)  # force toggle to be unselected
        self.updateDeleteButtonState()
        
        ### Check length of database ###
        with sqlite3.connect(DBPATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM master")
            count = cursor.fetchone()[0]
        if count == 0: # No entries exist at all
            self.dictionaryList.hide_empty_message()
            self.dictionaryList.display_empty_message(entries_exist = False)
        elif len(self.dictionaryList.entries) == 0:
            self.dictionaryList.hide_empty_message()
            self.dictionaryList.display_empty_message(entries_exist = True)

        self.updateCounter() # update the counter label in the footer

    def updateAuxiliaryUI(self) -> None:
        """
        Updates only the auxiliary UI components (filterBar).
        Updates the filterBar options with the unique tags from the database as the total available tags change.

        This method is called after any change to the tags in the database, such as adding, deleting, or editing tags.
        It ensures that the filterBar reflects the current state of the tags available for filtering.
        """
        self.filterBar.options = self.getUniqueTags()
        self.filterBar.refresh_options()

    def updateUI(self) -> None:
        """
        Updates the entire UI of the application.
        Calls both updateDictionaryUI and updateAuxiliaryUI to refresh the dictionary list and auxiliary components.

        This method is called after any significant change to the application state that affects both the dictionary list and auxiliary components,
        such as importing a new database, adding or deleting entries, or changing the filter options.
        """
        self.updateDictionaryUI()
        self.updateAuxiliaryUI()

    def getUniqueTags(self) -> list[str]:
        """
        Returns an list of unique tags, ordered by their first appearance in the database.
        Uses a set for efficient uniqueness checking and a list to maintain order.
        """
        seen = set()
        orderedTags = []

        with sqlite3.connect(DBPATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT tags FROM master ORDER BY uid")  # or createdAt
            for (tagString,) in cursor.fetchall():
                if tagString:
                    for tag in tagString.strip().split():
                        if tag not in seen:
                            seen.add(tag)
                            orderedTags.append(tag)
        return orderedTags

    def truncateText(self, text: str, maxWidth: int = 663, size: int = 64, weight="bold", font = "League Spartan") -> str:
            """
            Returns the text truncated to fit within the specified pixel width, adding an ellipsis if necessary.
            If the text fits within maxWidth, returns the original text. Else, truncates the text and appends an ellipsis.
            """
            font = ctk.CTkFont(family=font, size=size, weight=weight)
            if font.measure(text) <= maxWidth:
                return text
            while font.measure(f"{text}...") > maxWidth:
                text = text[:-1]
            truncated = f"{text}..."
            return truncated

### App Startup ###
if __name__ == "__main__":
    app = App()
    app.start()