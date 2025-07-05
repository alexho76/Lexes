import customtkinter as ctk
from PIL import ImageTk  # to convert PIL images for tkinter
import time

class SearchBarWithIcon(ctk.CTkFrame):
    def __init__(self, master, *,
                 width=500,
                 height=50,
                 corner_radius=200,
                 entry_placeholder="Search by keyword",
                 font=("League Spartan", 36),
                 text_color="green",
                 bg_color=None,
                 placeholder_text_color="darkgreen",
                 fg_color="lightgray",
                 border_width=0,
                 icon=None,
                 icon_hover=None,
                 icon_width=60,
                 **kwargs):
        super().__init__(master, width=width, height=height, fg_color="transparent", **kwargs)
        self.width = width
        self.height = height
        
        self.pack_propagate(False)

        self.icon_width = icon_width

        # Outer fake box to create rounded border look
        self.fake_box = ctk.CTkFrame(
            self,
            width=width,
            height=height-3,
            corner_radius=corner_radius,
            fg_color=fg_color,
            border_width=border_width
        )
        self.fake_box.pack(fill="both", expand=True)
        self.fake_box.pack_propagate(False)

        # Internal container for proper padding inside the fake box
        self.inner_frame = ctk.CTkFrame(self.fake_box, fg_color=fg_color)
        self.inner_frame.pack(side="left", fill="both", expand=True, padx=(25, 70),pady=1)  # right pad keeps away from edge
        self.inner_frame.pack_propagate(False)

        # Actual entry (reduced width to leave space for icon)
        self.search_entry = ctk.CTkEntry(
            self.inner_frame,
            placeholder_text=entry_placeholder,
            width=width - self.icon_width - 10,  # subtract icon width and a bit extra for spacing
            height=height - 13,
            corner_radius=0,
            font=font,
            text_color=text_color,
            placeholder_text_color=placeholder_text_color,
            fg_color=fg_color,
            border_width=0,
            justify='left'
        )
        self.search_entry.pack(side="left", fill="y", pady=(0, 6))

        self.icon_image_default = ImageTk.PhotoImage(icon)
        self.icon_image_hover = ImageTk.PhotoImage(icon_hover)

        self.icon_button = ctk.CTkButton(
            self.fake_box,
            image=self.icon_image_default,
            text="",
            fg_color=fg_color,
            corner_radius=0,
            width=self.icon_width,
            height=self.icon_width,
            command=self._on_icon_click,
            hover_color=fg_color
        )
        self.icon_button.place(x=self.width - self.icon_width - 25, y=(self.height - (self.height - 2)) // 2 + 8)

        # BIND HOVER EVENTS
        self.icon_button.bind("<Enter>", self._on_hover_enter)
        self.icon_button.bind("<Leave>", self._on_hover_leave)
        self.search_entry.bind("<Return>", self._on_enter_press)


    def get(self):
        return self.search_entry.get()

    def set(self, text):
        self.search_entry.delete(0, "end")
        self.search_entry.insert(0, text)

    def clear(self):
        self.search_entry.delete(0, "end")
    
    def _on_icon_click(self, event=None):
        print(f"Searching {self.get()}")

        self._on_hover_leave(event)

        self.after(100, lambda: self._on_hover_enter(event))
        self.search_entry.master.focus_set()
    
    def _on_enter_press(self, event=None):
        print(f"Searching {self.get()}")

        self._on_hover_enter(event)

        self.after(100, lambda: self._on_hover_leave(event))
        self.search_entry.master.focus_set()

    def _on_hover_enter(self, event):
        self.icon_button.configure(image=self.icon_image_hover)
        self.icon_button.place(x=self.width - self.icon_width - 27, y=(self.height - (self.height - 2)) // 2 + 4)

    def _on_hover_leave(self, event):
        self.icon_button.configure(image=self.icon_image_default)
        self.icon_button.place(x=self.width - self.icon_width - 25, y=(self.height - (self.height - 2)) // 2 + 8)



