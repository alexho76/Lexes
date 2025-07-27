### App Class
### Manages the interactions between UI and backend classes and methods. All of the app's logic is contained here.

# Class and Asset Imports
from tkinter import messagebox
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
from classes.widgets.export_button import ExportButton
from classes.widgets.file_path_entry import FilePathEntry
from assets.images import *

# Library Imports
import sqlite3
import customtkinter as ctk
import tkinter as tk
import tkinter.filedialog as filedialog
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
        self.entries = [Entry(term="fundamental forces", definition="In physics, fundamental forces (or fundamental interactions) are the basic forces in nature that cannot be reduced to more basic interactions. They are the forces that govern how objects and particles interact and how certain particles decay. There are four known fundamental forces: gravity, electromagnetism, the strong nuclear force, and the weak nuclear force.", tags="physics nuclear_physics forces vce"),
            Entry(term="iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii,", definition="abcde abcde abcde abcde abcde abcde abcde abcde abcde abcde abcde abcde abcde abcde abcde abcde abcde abcde", tags="iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii biology plants energy skibble science chemistry science2 science3"),
            Entry(term="Einstein's Theory of General Relativity (Classical Mechanics) AKA General Relativity", definition="A theory of relativity that states that the speed of light is the same in all frames of reference. Einstein discovered this theory in 1905 when he was working on the photoelectric effect.", tags="physics quantum_theory science"),
            Entry(term="Entropy", definition="A measure of the disorder or randomness in a closed system, important in thermodynamics.", tags="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ science physics chemical_science_exam_study"),
            Entry(term="Mitochondria", definition="Organelles known as the powerhouse of the cell; generate most of the cell's supply of ATP.", tags="biology cell energy"),
            Entry(term="Quantum Mechanics", definition="A fundamental theory in physics describing nature at the smallest scales.", tags="physics quantum_theory science"),
            
            Entry(term="Algorithm", definition="A step-by-step procedure for solving a problem or accomplishing some end.",
                    tags="computer_science_aaaaabbbcc programming algorit science mathematics science procedural process programming_definition computer_science2 programming_definition2 science2 computer_science3 programming_definition3 science3"),
            
            Entry(term="Ecosystem", definition="A biological community of interacting organisms and their physical environment.", tags="biology     environment ecology computer_scienc1e programming logic algorithms science mathematics science procedural process programming_definition computer_science2 programming_definition2 science2 computer_science3 programming_definition3 science3"),
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
                                       command=self.openAddWindow)
        self.addButton.pack(side='left', padx=(9,2), pady=9)
        
        self.quickAddButton = ctk.CTkButton(self.navigationBar,
                                            text="Quick Add",
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
        self.quickAddButton.pack(side='left', padx=2, pady=9)
        
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
                                             on_selection_change=self.onEntrySelectionChanged,
                                             on_row_click=self.handleRowClick)
        self.dictionaryList.pack(pady=(15,0))

        # Footer with Logo (will be across all pages)
        self.footer = ctk.CTkFrame(self.background, fg_color=LightGreen1, height=83)
        self.footer.pack(fill='x', side='bottom', pady=0, padx=0)
        self.footer.pack_propagate(False)

        self.entryCounter = ctk.CTkLabel(self.footer, text=f"# Entries: {len(self.masterApp.displayList.entries)}", font=("League Spartan", 20), text_color=DarkGreen3)
        self.entryCounter.place(relx=0.005, rely=0)

        ctkIconImage = ctk.CTkImage(light_image=iconImage, dark_image=iconImage, size=(65,65))
        self.icon = ctk.CTkLabel(self.footer, image=ctkIconImage, text="", anchor='center')
        self.icon.pack(expand=True)
    
    def handleRowClick(self, row_num, entry):
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
        
        def editButtonCommand():
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
        
        def sidebarAutoDefButtonCommand():
            updatedTerm = self.sidebarTitle.get().strip()
            newDefinition = Helper.wikipediaAPI(updatedTerm)
            if newDefinition:
                self.definitionTextbox.focus_set()
                self.definitionTextbox.delete(1.0, tk.END)
                self.definitionTextbox.insert(1.0, newDefinition)
            else:
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
        
        
        def sidebarDeleteButtonCommand():
            self.sidebarFrame.destroy()

            with sqlite3.connect(dbPath) as conn: # mass removal from db
                cursor = conn.cursor()
                cursor.execute("DELETE FROM master WHERE uid = ?", (entry.uid,))
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

        def sidebarDoneButtonCommand():
            newTerm = self.sidebarTitle.get().strip()
            newDefinition = self.definitionTextbox.get("1.0", tk.END).strip()
            newTags = self.tagsTextbox.get("1.0", tk.END)
            newTags = ' '.join(tag.strip() for tag in newTags.split())

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

        def sidebarCancelButtonCommand():
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

        if not messagebox.askyesno("Delete Entries",
                                   f"Are you sure you want to delete the selected entries ({len(self.masterApp.selectedList.entries)})? This action cannot be undone.",
                                   parent=self):
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

    def openAddWindow(self): # Opens the add entry window
        ### Popup Window Setup
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

        def showPlaceholder():
            definitionEntry.configure(text_color=placeholderColor)
            definitionEntry.insert("1.0", placeholderText)

        def hidePlaceholder(event=None):
            definitionEntry.delete("1.0", tk.END)
            definitionEntry.configure(text_color=normalColor)

        def onFocusIn(event):
            if definitionEntry.get("1.0", tk.END).strip() == placeholderText and definitionEntry.cget("text_color") == placeholderColor:
                hidePlaceholder()

        def onFocusOut(event):
            if not definitionEntry.get("1.0", tk.END).strip():
                showPlaceholder()

        definitionEntry.bind("<FocusIn>", onFocusIn)
        definitionEntry.bind("<FocusOut>", onFocusOut)

        # Show placeholder initially
        showPlaceholder()

        def autoDefButtonCommand():
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

        # Tag display entry
        tagLabelFrame = ctk.CTkFrame(background, corner_radius=0, fg_color="transparent")
        tagLabelFrame.pack(padx=35, pady=(15,0), fill="x")

        ctkTagIcon = ctk.CTkImage(dark_image=tagIconImage, light_image=tagIconImage, size=(36,36))
        tagIconLabel = ctk.CTkLabel(tagLabelFrame, text="", image=ctkTagIcon, compound="left")
        tagIconLabel.pack(padx=0, pady=(10,0), side='left')

        tagLabel = ctk.CTkLabel(tagLabelFrame, text="Tags (optional)", font=("League Spartan", 48), text_color=DarkGreen2)
        tagLabel.pack(padx=7, pady=(0,0), side='left')

        tagEntry = ctk.CTkEntry(background, placeholder_text="e.g. nuclear_physics biology vce", font=("League Spartan", 36),
                                 placeholder_text_color=Cream3, text_color=DarkGreen2, fg_color=Cream, border_color=DarkGreen3,
                                 border_width=2.5)
        tagEntry.pack(padx=35, pady=0, fill="x")

        # Window Navigation Buttons
        buttonFrame = ctk.CTkFrame(background, corner_radius=0, fg_color="transparent")
        buttonFrame.pack(padx=35, pady=(35,0), fill="x")

        def cancelButtonCommand():
            topLevel.destroy()
        cancelButton = ctk.CTkButton(buttonFrame, text="Cancel", font=("League Spartan Bold", 24), height=50, width=130, text_color=Red, corner_radius=5,
                                     border_color=Red, fg_color=Cream, hover_color=Cream2, border_width=2.5, command=cancelButtonCommand)
        cancelButton.pack(side='right', padx=(0,0), pady=0)
    
        def addButtonCommand():
            term = termEntry.get().strip()
            definition = definitionEntry.get("1.0", tk.END).strip()
            tags = tagEntry.get().strip() # still in space separated string format
            if not term or definition == placeholderText or not definition:
                messagebox.showwarning("Missing Fields",
                                       "Please fill in both the term and definition fields.",
                                       parent=topLevel)
                return
            entry = Entry(term=term, definition=definition, tags=tags)
            entry.add() # add to database

            self.updateUI() # update the main app UI including the dictionary list, counter, and filter bar

            # Clear the input fields except for tags and focus on term entry
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
    
    def openExportWindow(self): # Opens the export window
        ### Popup Window Setup
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

        def toggleExport(buttonName):
            if buttonName == "Anki Deck":
                exportAnkiButton.toggle()
                if exportDBButton.get_state():
                    exportDBButton.set_state(False)
            elif buttonName == "Lexes DB":
                exportDBButton.toggle()
                if exportAnkiButton.get_state():
                    exportAnkiButton.set_state(False)

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
                                             border_width=2.5, placeholder_text="Select file path...", placeholder_text_color=Cream3, icon=folderIconImage, icon_size=(46,36),
                                             option_one=exportAnkiButton, option_two=exportDBButton)
        exportDirectoryEntry.pack(padx=0, pady=0, fill="x")

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

        def cancelButtonCommand():
            topLevel.destroy()
        cancelButton = ctk.CTkButton(bottomFrame, text="Cancel", font=("League Spartan Bold", 24), height=50, width=130, text_color=Red, corner_radius=5,
                                     border_color=Red, fg_color=Cream, hover_color=Cream2, border_width=2.5, command=cancelButtonCommand)
        cancelButton.pack(side='right', padx=(0,0), pady=0)


        def exportButtonCommand():
            if not exportAnkiButton.get_state() and not exportDBButton.get_state():
                messagebox.showwarning("No Export Type Selected",
                                       "Please select an export type (Anki Deck or Lexes DB).",
                                       parent=topLevel)
                return
            if not exportDirectoryEntry.get_path():
                messagebox.showwarning("No File Path Selected",
                                       "Please select a file path to export the file to.",
                                       parent=topLevel)
                return
            if len(self.masterApp.selectedList.entries) == 0: # shouldn't ever happen but just in case
                messagebox.showwarning("No Entries Selected",
                                       "Please select entries to export.",
                                       parent=topLevel)
                return
            # all validations passed, proceed with export

            filePath = exportDirectoryEntry.get_path()

            if filePath.endswith(".csv"): # if exporting to anki deck
                self.masterApp.selectedList.exportToAnki(filePath=filePath, includeTags=tagCheckbox.get())
            else:
                self.masterApp.selectedList.exportToDB(filePath=filePath, includeTags=tagCheckbox.get())

            topLevel.destroy()  # close the export window
            messagebox.showinfo("Export Successful",
                                f"Successfully exported {len(self.masterApp.selectedList.entries)} entries.",
                                parent=self)

        exportButton = ctk.CTkButton(bottomFrame, text="Export", font=("League Spartan Bold", 24), height=50, width=130, text_color=DarkGreen3, corner_radius=5,
                                  border_color=DarkGreen3, fg_color=Cream, hover_color=Cream2, border_width=2.5, command=exportButtonCommand)
        exportButton.pack(side='right', padx=(0,5), pady=0)

    # Opens the import window to import raw pasted text.
    def openImportTextWindow(self):
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
            topLevel.title("Import Text")
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
            def parseButtonCommand():
                # Check if importTextbox is empty or contains only placeholder text, and if dropdowns are selected
                if importTextbox.get("1.0", tk.END).strip() == placeholderText or not importTextbox.get("1.0", tk.END).strip():
                    messagebox.showwarning("Empty Text",
                                           "Please paste or type raw text to import.",
                                           parent=topLevel)
                    return
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

                # Parse
                successfulParse, trialParsedEntries = importList.parseText()

                # Clear the importTextbox before inserting parsed entries (regardless of success)
                importTextbox.delete("1.0", tk.END)

                if successfulParse:
                    # Update UI with parsed entries (attempted). For each parsed "entry" (really a tuple of strings), add to the importTextbox
                    # entries delimited by line breaks and term-definition pairs delimited by the selected colon ':' (system-default/recommended)
                    for entry in trialParsedEntries:
                        term, definition = entry
                        importTextbox.insert("end", f"{term}: {definition}\n")
                    
                    messagebox.showinfo("Parse Successful",
                                        f"Successfully parsed {len(trialParsedEntries)} entries.",
                                        parent=topLevel)
                else:
                    # Either a term was missing or a definition was missing (and failed to auto-retrieve), so insert the entries back into the importTextbox
                    # entries and term-definition pairs delimited by the user's originally selected delimiters (may not be system-default or recommended)
                    for entry in trialParsedEntries:
                        term, definition = entry
                        importTextbox.insert("end", f"{term}{termDefinitionDelimiter}{definition}\n")

                    messagebox.showerror("Parse Incomplete",
                                         "Some entries were not parsed successfully. Either a term was missing or a definition failed to auto-retrieve. Please check the input textbox and try again.",
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

            def cancelButtonCommand():
                topLevel.destroy()
            cancelButton = ctk.CTkButton(buttonFrame, text="Cancel", font=("League Spartan Bold", 24), height=50, width=130, text_color=Red, corner_radius=5,
                                     border_color=Red, fg_color=Cream, hover_color=Cream2, border_width=2.5, command=cancelButtonCommand)
            cancelButton.pack(side='right', padx=(0,30), pady=0)

            def importButtonCommand():
                # Check if the importTextbox is empty or contains only placeholder text
                if importTextbox.get("1.0", tk.END).strip() == placeholderText or not importTextbox.get("1.0", tk.END).strip():
                    messagebox.showwarning("Empty Text",
                                           "Please paste or type raw text to import.",
                                           parent=topLevel)
                    return
                
                # Check if all dropdowns have a selected value
                if not entryDelimiterDropdown.get_selected() or not termDefinitionDelimiterDropdown.get_selected():
                    proceed = messagebox.askyesno("Missing Delimiters",
                                           "Delimiters have not been selected. Current operations will use values of:\n- Line Break (Default)\n- Colon (Default)\nDo you want wish to proceed?",
                                           parent=topLevel)
                    if proceed == False:
                        return
                
                # Get mass tags if provided
                importList.massTags = massTagsEntry.get().strip()

                # Get rawText from importTextbox
                importList.rawText = importTextbox.get("1.0", tk.END).strip()

                # Validate entries (remake from rawText)
                isValid = importList.validateEntries()
                print(isValid, len(importList.parsedEntries))  # Debugging output to check validation results

                if not isValid:
                    messagebox.showerror("Invalid Entries",
                                         "Some entries are invalid. Please check the raw text and try again.",
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
    
    def openImportDBWindow(self): # Opens the import window to import a Lexes DB file.
        ### Popup Window Setup
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

        # Import from label and file directory selection and preview
        importFromLabel = ctk.CTkLabel(background, text="Import database from:", font=("League Spartan", 48), text_color=DarkGreen2)
        importFromLabel.pack(padx=35, pady=(15,0), anchor='nw')

        importDirectoryEntry = FilePathEntry(background, font=("League Spartan", 36), text_color=Cream3, fg_color=Cream, border_color=DarkGreen3,
                                             border_width=2.5, placeholder_text="Select file path...", placeholder_text_color=Cream3, icon=folderIconImage, icon_size=(46,36),
                                             option_one=None, option_two=None, file_type=".db")
        importDirectoryEntry.pack(padx=35, pady=0, fill="x")







        # Footer
        footer = ctk.CTkFrame(background, corner_radius=0, fg_color=LightGreen1, height=80)
        footer.pack(fill='x', side='bottom', pady=0, padx=0)
        footer.pack_propagate(False)

        ctkIconImage = ctk.CTkImage(light_image=iconImage, dark_image=iconImage, size=(65,65))
        footerIcon = ctk.CTkLabel(footer, image=ctkIconImage, text="", anchor='center')
        footerIcon.pack(expand=True)

        # Button frame at bottom
        buttonFrame = ctk.CTkFrame(background, corner_radius=0, fg_color="transparent")
        buttonFrame.pack(side="bottom", fill="x", padx=35, pady=(0, 20))

        cancelButton = ctk.CTkButton(buttonFrame, text="Cancel", font=("League Spartan Bold", 24), height=50, width=130,
            text_color=Red, corner_radius=5, border_color=Red, fg_color=Cream,
            hover_color=Cream2, border_width=2.5, command=None)
        cancelButton.pack(side="right", padx=(0, 0), pady=0)

        importButton = ctk.CTkButton(buttonFrame, text="Import", font=("League Spartan Bold", 24), height=50, width=130,
            text_color=DarkGreen3, corner_radius=5, border_color=DarkGreen3, fg_color=Cream,
            hover_color=Cream2, border_width=2.5, command=None)
        importButton.pack(side="right", padx=(0, 5), pady=0)

        # Mass Tags Label and Entry
        massTagsFrame = ctk.CTkFrame(background, corner_radius=0, fg_color="Red", width=560)
        massTagsFrame.pack(padx=0, pady=(0,20))

        massTagsLabelFrame = ctk.CTkFrame(massTagsFrame, corner_radius=0, fg_color="blue")
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

    def truncateText(self, text: str, maxWidth: int = 663, size: int = 64, weight="bold", font = "League Spartan"):
            font = ctk.CTkFont(family=font, size=size, weight=weight)
            if font.measure(text) <= maxWidth:
                return text
            while font.measure(f"{text}...") > maxWidth:
                text = text[:-1]
            truncated = f"{text}..."
            return truncated


app = App()
app.mainWindow.openImportDBWindow()
app.start()