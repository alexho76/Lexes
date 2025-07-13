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
        self.initaliseUI()

    def initaliseUI(self):
        self.setupDB()

        # Initalise displayList and selectedList
        self.entries = [Entry(term="iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii", definition="iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii...iiiiii fsdafadssfdsaffdsafdsfs sdafsdaf sadsdsafasd testing", tags="biology plants energy skibble science chemistry science2 science3"),
            Entry(term="Einstein's Theory of General", definition="A theory of relativity that states that the speed of light is the same in all frames of reference. Einstein discovered this theory in 1905 when he was working on the photoelectric effect.", tags="physics quantum_theory science"),
            Entry(term="Entropy", definition="A measure of the disorder or randomness in a closed system, important in thermodynamics.", tags="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ science physics chemical_science_exam_study"),
            Entry(term="Mitochondria", definition="Organelles known as the powerhouse of the cell; generate most of the cell's supply of ATP.", tags="biology cell energy"),
            Entry(term="Quantum Mechanics", definition="A fundamental theory in physics describing nature at the smallest scales.", tags="physics quantum_theory science"),
            
            Entry(term="Algorithm", definition="A step-by-step procedure for solving a problem or accomplishing some end.",
                    tags="computer_science programming algorit science mathematics science procedural process programming_definition computer_science2 programming_definition2 science2 computer_science3 programming_definition3 science3"),
            
            Entry(term="Ecosystem", definition="A biological community of interacting organisms and their physical environment.", tags="biology     environment ecology computer_science programming logic algorithms science mathematics science procedural process programming_definition computer_science2 programming_definition2 science2 computer_science3 programming_definition3 science3"),
            Entry(term="Thermodynamics", definition="The study of the behavior of matter and energy.", tags="physics thermodynamics science"),
            Entry(term="Electrochemistry", definition="The study of the behavior of matter and energy.", tags="physics chemistry science")]
        
        for i in range(50):
            self.entries.append(Entry(term=f"Term {i}", definition=f"Definition {i}", tags=f"Tag {i}"))
        
        # clear all rows from database
        with sqlite3.connect(dbPath) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM master")
            # clear uid counter
            cursor.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'master'")

        for entry in self.entries:
            # add entry to database
            entry.add()

        self.displayList = DisplayList()
        self.displayList.build()
        self.selectedList = SelectedList()

        # Initialise UI
        self.mainWindow = MainWindow(self)
    
    def start(self):
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
        self.background.pack(fill='both', expand=True)

        # Navigation Bar with Buttons
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
                                       command=lambda: self.openTopLevel())
        self.addButton.pack(side='left', padx=(9,2), pady=9)
        
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
                                          hover_color=Cream2)
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
                                          hover_color=Cream2)
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
                                            hover_color=Cream2)
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
                                             hover_color=DarkGreen1b,
                                             selected_bg_color=DarkGreen3,
                                             selected_text_color=Cream,
                                             width=400,
                                             default_text="Filter by tags",
                                             dropdown_bg_color=DarkGreen1b,
                                             on_close_callback=self.filterBarCommand)
        self.filterBar.pack(side='left', padx=6)

        self.sortBar = SingleSelectComboBox(self.toolBar,
                                            options=["Newest", "Oldest", "A-Z", "Z-A"],
                                            font=("League Spartan", 36),
                                            dropdown_font=("League Spartan", 24),
                                            fg_color=DarkGreen1,
                                            text_color=DarkGreen2,
                                            corner_radius=50,
                                            width=238,
                                            height=65,
                                            border_width=0,
                                            hover_color=DarkGreen1b,
                                            selected_bg_color=DarkGreen3,
                                            selected_text_color=Cream,
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

        # Dictionary List Test
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
                                             on_selection_change=self.onEntrySelectionChanged)
        self.dictionaryList.pack(pady=(15,0))

        # Footer with Logo (will be across all pages)
        self.footer = ctk.CTkFrame(self.background, fg_color=LightGreen1, height=83)
        self.footer.pack(fill='x', side='bottom', pady=0, padx=0)
        self.footer.pack_propagate(False)

        self.entryCounter = ctk.CTkLabel(self.footer, text=f"# Entries: {len(self.masterApp.displayList.entries)}", font=("League Spartan", 20), text_color=DarkGreen3)
        self.entryCounter.pack(side='left', padx=10, pady=0, anchor='n')

        ctkIconImage = ctk.CTkImage(light_image=iconImage, dark_image=iconImage, size=(65,65))
        self.icon = ctk.CTkLabel(self.footer, image=ctkIconImage, text="", anchor='center')
        self.icon.pack(expand=True)

    def searchBarCommand(self, searchKeyword):
        if searchKeyword != self.masterApp.displayList.searchKeyword: # update search term
            self.masterApp.displayList.searchKeyword = searchKeyword
            
            # update ui
            self.updateDictionaryUI()
        else: # selected attribute unchanged so do nothing
            return

    def filterBarCommand(self, selectedTags):
        selectedTags = " ".join(selectedTags)

        if selectedTags != self.masterApp.displayList.filterTags or self.filterBar.require_all_selected() != self.masterApp.displayList.requireAllTags: # update filter tags
            self.masterApp.displayList.filterTags = selectedTags
            self.masterApp.displayList.requireAllTags = self.filterBar.require_all_selected()
            
            # update ui
            self.updateDictionaryUI()
        else: # selected tags unchanged so do nothing
            return

    def sortBarCommand(self, selectedAttribute):
        if selectedAttribute != self.masterApp.displayList.sortAttribute: # update sort attribute
            self.masterApp.displayList.sortAttribute = selectedAttribute
            
            # update ui
            self.updateDictionaryUI()
        else: # selected attribute unchanged so do nothing
            return
    
    def selectAllToggleCommand(self):
        if self.selectAllToggle.get_state():
            self.dictionaryList.select_all()
        else:
            self.dictionaryList.unselect_all()
        
        self.updateDeleteButtonState()

    def onEntrySelectionChanged(self):
        self.updateDeleteButtonState()
    
    def updateDeleteButtonState(self):
        if len(self.masterApp.selectedList.entries) > 0:
            self.deleteSelectedButton.unlock()
        else:
            self.deleteSelectedButton.lock()

    def deleteSelectedButtonCommand(self):
        if not self.masterApp.selectedList.entries:
            return

        uidsToDelete = [entry.uid for entry in self.masterApp.selectedList.entries]

        with sqlite3.connect(dbPath) as conn: # mass removal from db
            cursor = conn.cursor()
            cursor.executemany("DELETE FROM master WHERE uid = ?", [(uid,) for uid in uidsToDelete])
            conn.commit()

        self.masterApp.selectedList.entries.clear()

        self.updateUI()

        if self.dictionaryList.entries == []:
            print("None left")
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
        self.topLevel.grab_set()  # grabs all inputs (kb and mouse)

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
        
    def updateDictionaryUI(self):
        self.masterApp.selectedList.entries.clear()  # clear selected entries
        self.masterApp.displayList.build()  # rebuild filtered list
        self.dictionaryList.entries = self.masterApp.displayList.entries
        self.dictionaryList.populate()  # refresh list UI
        self.selectAllToggle.set_state(False)  # force toggle to be unselected
        self.updateDeleteButtonState()
        
        self.entryCounter.configure(text=f"# Entries: {len(self.masterApp.displayList.entries)}")

    def updateAuxiliaryUI(self):
        self.filterBar.options = self.getUniqueTags()
        self.filterBar.refresh_options()

    def updateUI(self):
        self.updateDictionaryUI()
        self.updateAuxiliaryUI()

    def getUniqueTags(self):
        # gets unique tags
        seen = set()
        orderedTags = []

        with sqlite3.connect(dbPath) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT tags FROM master ORDER BY uid")  # or createdAt
            for (tagString,) in cursor.fetchall():
                if tagString:
                    for tag in tagString.strip().split():
                        if tag not in seen:
                            seen.add(tag)
                            orderedTags.append(tag)
        return orderedTags

app = App()
app.start()