"""
File: classes/widgets/file_path_entry.py

Purpose:
    Defines the FilePathEntry custom widget for the Lexes app. This widget provides a styled entry field for entering a file name or path to save a file.
    Typically used in 'Save As' dialogs, where the user types the desired file name or path. Adjusts file selection type based on the selected export option (e.g., Anki or Database) using option_one and option_two.

Contains:
    - FilePathEntry class: A CTkFrame-based widget containing a CTkEntry and a browse icon.
    - Methods for getting/setting the entry value and handling browse button clicks.

Naming Conventions:
    - Class names: PascalCase (FilePathEntry)
    - Public method names: snake_case (get_path, set_path)
    - Private method names: snake_case, prefixed with an underscore (_open_dialog)
    - Attributes: snake_case (icon, icon_label, placeholder_text)
    - General code: snake_case. NOTE: Custom widgets use snake_case while the rest of the codebase uses camelCase.

Usage:
    Use FilePathEntry to allow users to manually enter the destination file name or path when saving a file.
    Meant to be used with two or more ExportButtons to change the file selection type.
    NOTE: Use SelectFilePathEntry (different file and class) to provide a file browsing dialog for selecting already existing files.
    FilePathEntry used for export file name selection in Export Window.
"""

### Module Imports ###
import tkinter.filedialog as filedialog
import customtkinter as ctk
from tkinter import messagebox
import os

### Local Class Imports ###
from classes.widgets.export_button import ExportButton

class FilePathEntry(ctk.CTkFrame):
    def __init__(self,
                 master,

                 icon,
                 icon_size,

                 font,
                 text_color,
                 fg_color,
                 border_color,
                 border_width,

                 placeholder_text,

                 option_one: ExportButton, # checkbox toggle 1
                 option_two: ExportButton, # checkbox toggle 2

                 on_callback = None,
                 **kwargs):
        """
        Initialise the FilePathEntry widget with custom styles, images, and text.
        """
        super().__init__(master, fg_color=fg_color, border_color=border_color, border_width=border_width, **kwargs)
        self.on_callback = on_callback

        ### Icon and Label Setup ###
        self.icon = ctk.CTkImage(light_image=icon, dark_image=icon, size=icon_size) if icon else None
        self.icon_label = ctk.CTkLabel(self, image=self.icon, text="", fg_color="transparent")
        self.icon_label.pack(side="left", padx=(10,0), pady=5)

        ### Entry Setup ###
        self.placeholder_text = placeholder_text
        self.path_label = ctk.CTkLabel(self, text=self.placeholder_text, font=font, text_color=text_color, fg_color="transparent")
        self.path_label.pack(side="left", padx=10, pady=(2.5,7.5))

        ### Bindings for Click Events ###
        self.bind("<Button-1>", self._open_dialog)  # left click
        self.icon_label.bind("<Button-1>", self._open_dialog)
        self.path_label.bind("<Button-1>", self._open_dialog)

        ### Checkbox Linking Toggles Setup ###
        self.option_one = option_one
        self.option_two = option_two

        self.file_path = ""

    def _open_dialog(self, event=None) -> None:
        """
        Private Method
        Opens a file dialog to select a file path.
        Changes type of files displayed based on the selected export option (using option_one and option_two).
        """
        ### Get the file type based on the selected export option ###
        if self.option_one.get_state():
            file_type = ".csv"
            file_types = [("CSV Files", "*.csv")]
        elif self.option_two.get_state():
            file_type = ".db"
            file_types = [("SQLite Database Files", "*.db")]
        else:
            file_type = ""
            file_types = []

        ### Open the file dialog based on the selected file type ###
        if file_type:
            file_path = filedialog.asksaveasfilename(title="Save As",
                                                    defaultextension=file_type,
                                                    filetypes=file_types) # only shows matching file types and selecting a duplicate will overwrite
        else:
            messagebox.showerror("No File Type Selected", "Please select a file type to export the entries to.", parent=self.master)
            file_path = ""
        
        # Validate file extension
        if file_path:
            root, ext = os.path.splitext(file_path)
            # If wrong extension, show error and return
            if ext and ext.lower() != file_type:
                messagebox.showerror("Invalid File Extension",
                    f"Please save the file as {file_type} only.",
                    parent=self.master)
                self.file_path = ""
                self.path_label.configure(text=self.placeholder_text)
                return
            # If missing extension, add it
            if not ext:
                file_path = file_path + file_type

            self.file_path = file_path
            self.path_label.configure(text=self.file_path)
        else:
            self.file_path = ""
            self.path_label.configure(text=self.placeholder_text)

        if self.on_callback:
            self.on_callback(self.file_path)

    def get_path(self) -> str:
        """
        Public Method
        Returns the currently selected file path or an empty string if none is selected.
        """
        return self.file_path if self.file_path else ""
    
    def reset(self) -> None:
        """
        Public Method
        Resets the file path to "" and clears the entry label.
        """
        self.file_path = ""
        self.path_label.configure(text=self.placeholder_text)  # Reset label to placeholder text
    
    def change_text_color(self, color: str) -> None:
        """
        Public Method
        Changes the text color of the entry label.
        """
        self.path_label.configure(text_color=color)