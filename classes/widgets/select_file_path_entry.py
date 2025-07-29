"""
File: classes/widgets/select_file_path_entry.py

Purpose:
    Defines the SelectFilePathEntry custom widget for the Lexes app. This widget provides a clickable entry area
    with an icon and placeholder, enabling users to select a file path via a dialog. Supports file type restriction
    and notifies via callback when a selection is made.

Contains:
    - SelectFilePathEntry class: A CTkFrame-based widget with an icon and a path label. Clicking opens a file dialog.
    - Methods for opening the file dialog, handling file type restriction, updating the label, and retrieving the selected path.

Naming Conventions:
    - Class names: PascalCase (SelectFilePathEntry)
    - Public method names: snake_case (get_path)
    - Private method names: snake_case, prefixed with an underscore (e.g., _open_dialog)
    - Attributes: snake_case (icon, icon_label, path_label, file_type, file_path)
    - General code: snake_case. NOTE: Custom widgets use snake_case while the rest of the codebase uses camelCase.

Usage:
    Use SelectFilePathEntry to visually prompt users to select an export file path. Supports .csv and .db files with error handling if file type is missing.
    SelectFilePathEntry used for import file selection in Import DB Window.
"""

### Module Imports ###
import tkinter.filedialog as filedialog
import customtkinter as ctk
from tkinter import messagebox

class SelectFilePathEntry(ctk.CTkFrame):
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

                 file_type=None,

                 on_callback = None,
                 **kwargs):
        """
        Initialise the SelectFilePathEntry widget with custom styling, icon, and callback.
        """
        super().__init__(master, fg_color=fg_color, border_color=border_color, border_width=border_width, **kwargs)

        self.icon = ctk.CTkImage(light_image=icon, dark_image=icon, size=icon_size) if icon else None

        self.icon_label = ctk.CTkLabel(self, image=self.icon, text="", fg_color="transparent")
        self.icon_label.pack(side="left", padx=(10,0), pady=5)

        self.placeholder_text = placeholder_text
        self.path_label = ctk.CTkLabel(self, text=self.placeholder_text, font=font, text_color=text_color, fg_color="transparent")
        self.path_label.pack(side="left", padx=10, pady=(2.5,7.5))
        
        ### Bind Click Events (Entry, Icon, Label) ###
        self.bind("<Button-1>", self._open_dialog)  # left click
        self.icon_label.bind("<Button-1>", self._open_dialog)
        self.path_label.bind("<Button-1>", self._open_dialog)

        self.file_type = file_type
        self.file_path = ""
        self.on_callback = on_callback

    def get_path(self) -> str:
        """
        Public Method
        Returns the currently selected file path as a string, or empty string if none.
        """
        return self.file_path if self.file_path else ""

    def _open_dialog(self, event=None) -> None:
        """
        Private Method
        Opens a file dialog for selecting a file path based on the file type.
        Updates the label and triggers callback if set.
        """
        file_type = self.file_type if self.file_type else ""

        # Only allows certain file types based on the file_type attribute.
        if file_type == ".csv":
            file_path = filedialog.askopenfilename(title="Save As",
                                                   defaultextension=".csv",
                                                   filetypes=[("CSV Files", "*.csv")]) # only shows csv's and selecting a duplicate will overwrite
        elif file_type == ".db":
            file_path = filedialog.askopenfilename(title="Save As",
                                                   defaultextension=".db",
                                                   filetypes=[("SQLite Database Files", "*.db")]) # only shows db's and selecting a duplicate will overwrite
        else:
            messagebox.showerror("No File Type Selected", "Please select a file type to export the entries to.", parent=self.master)
            file_path = ""
        
        self.file_path = file_path
        if self.file_path:
            self.path_label.configure(text=self.file_path)
        else:
            self.path_label.configure(text=self.placeholder_text)

        # Trigger the callback with selected file path if provided.
        if self.on_callback:
            self.on_callback(self.file_path)