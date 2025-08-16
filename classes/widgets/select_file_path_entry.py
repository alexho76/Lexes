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
                 icon_size: tuple,
                 font: tuple,
                 text_color: str,
                 fg_color: str,
                 border_color: str,
                 border_width: float,
                 placeholder_text: str,
                 file_type: str = None,
                 on_callback: callable = None,
                 **kwargs):
        """
        Initialise the SelectFilePathEntry widget with custom styling, icon, and callback.
        - master (CTk): The parent widget for the SelectFilePathEntry. CTk so it can use customTkinter features.
        - icon (Image): The icon image to display in the entry. Image as it represents the icon image.
        - icon_size (tuple): The size of the icon image. Tuple as it represents the dimensions (width, height).
        - font (tuple): The font configuration for the path label text. Tuple as it represents the font family and size.
        - text_color (str): The text color for the path label. String as it represents a color value.
        - fg_color (str): The foreground color for the entry. String as it represents a color value.
        - border_color (str): The border color for the entry. String as it represents a color value.
        - border_width (float): The border width for the entry. Float as it represents the width in pixels.
        - placeholder_text (str): The placeholder text for the path label. String as it represents the default text.
        - file_type (str): The file type to restrict selection (e.g., ".csv", ".db"). String as it represents the file extension.
        - on_callback (callable): The callback function to call when a file is selected. Callable as it represents a callback function.
        """
        super().__init__(master, fg_color=fg_color, border_color=border_color, border_width=border_width, **kwargs)
        ### Icon Setup ###
        self.icon = ctk.CTkImage(light_image=icon, dark_image=icon, size=icon_size) if icon else None
        self.icon_label = ctk.CTkLabel(self, image=self.icon, text="", fg_color="transparent")
        self.icon_label.pack(side="left", padx=(10,0), pady=5)

        ### Path Label Setup ###
        self.placeholder_text = placeholder_text
        self.path_label = ctk.CTkLabel(self, text=self.placeholder_text, font=font, text_color=text_color, fg_color="transparent")
        self.path_label.pack(side="left", padx=10, pady=(2.5,7.5))
        
        ### Bind Click Events (Entry, Icon, Label) ###
        self.bind("<Button-1>", self._open_dialog)  # left click
        self.icon_label.bind("<Button-1>", self._open_dialog)
        self.path_label.bind("<Button-1>", self._open_dialog)

        self.file_type = file_type # file type to restrict selection (e.g., ".csv", ".db")
        self.file_path = "" # initially empty path
        self.on_callback = on_callback # callback function to execute when a file is selected

    def _open_dialog(self, event=None) -> None:
        """
        Private Method

        Opens a file dialog for selecting a file path based on the file type. Updates the label and triggers callback if set.
        - event (tk.Event): The event that triggered the dialog. Tkinter Event containing information about the mouse click.
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

    def get_path(self) -> str:
        """
        Public Method

        Returns the currently selected file path as a string, or empty string if none.
        """
        return self.file_path if self.file_path else ""

    def reset(self) -> None:
        """
        Public Method

        Resets the SelectFilePathEntry widget to its initial state. Clears the stored file path and restores the placeholder text to normal.
        """
        self.file_path = ""
        self.path_label.configure(text=self.placeholder_text)