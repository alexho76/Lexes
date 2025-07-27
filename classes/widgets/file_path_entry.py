import tkinter.filedialog as filedialog
import customtkinter as ctk
from classes.widgets.export_button import ExportButton
from tkinter import messagebox


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
                 placeholder_text_color,

                 option_one: ExportButton, # checkbox toggle 1
                 option_two: ExportButton, # checkbox toggle 2
                 file_type=None,
                 **kwargs):
        super().__init__(master, fg_color=fg_color, border_color=border_color, border_width=border_width, **kwargs)

        self.icon = ctk.CTkImage(light_image=icon, dark_image=icon, size=icon_size) if icon else None


        self.icon_label = ctk.CTkLabel(self, image=self.icon, text="", fg_color="transparent")
        self.icon_label.pack(side="left", padx=(10,0), pady=5)

        self.placeholder_text = placeholder_text
        self.path_label = ctk.CTkLabel(self, text=self.placeholder_text, font=font, text_color=text_color, fg_color="transparent")
        self.path_label.pack(side="left", padx=10, pady=(2.5,7.5))

        
        self.bind("<Button-1>", self.open_dialog)  # left click
        self.icon_label.bind("<Button-1>", self.open_dialog)
        self.path_label.bind("<Button-1>", self.open_dialog)

        self.option_one = option_one
        self.option_two = option_two
        self.file_type = file_type

        self.file_path = ""

    def open_dialog(self, event=None):
        if self.option_one is None and self.option_two is None:
            file_type = self.file_type if self.file_type else ""
        else:
            if self.option_one.get_state():
                file_type = ".csv"
            elif self.option_two.get_state():
                file_type = ".db"
            else:
                file_type = ""

        if file_type == ".csv":
            file_path = filedialog.asksaveasfilename(title="Save As",
                                                    defaultextension=".csv",
                                                    filetypes=[("CSV Files", "*.csv")]) # only shows csv's and selecting a duplicate will overwrite
                        

        elif file_type == ".db":
            file_path = filedialog.asksaveasfilename(title="Save As",
                                                    defaultextension=".db",
                                                    filetypes=[("SQLite Database Files", "*.db")]) # only shows db's and selecting a duplicate will overwrite
        
        else:
            messagebox.showerror("No File Type Selected", "Please select a file type to export the entries to.", parent=self.master)
            file_path = ""
        
        self.file_path = file_path
        self.path_label.configure(text=self.file_path) if self.file_path else self.path_label.configure(text=self.placeholder_text)

    def get_path(self):
        return self.file_path if self.file_path else ""