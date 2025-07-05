import customtkinter as ctk

class SearchBarWithIcon(ctk.CTkFrame):
    def __init__(self, master, *,
                 width=500,
                 height=50,
                 corner_radius=200,
                 entry_placeholder="Search by keyword",
                 font=("League Spartan", 36),
                 text_color="green",
                 placeholder_text_color="darkgreen",
                 fg_color="lightgray",
                 border_width=0,
                 icon_text="🔍",
                 icon_font=("Arial", 28),
                 icon_width=60,
                 **kwargs):
        super().__init__(master, width=width, height=height, fg_color="transparent", **kwargs)
        self.pack_propagate(False)

        # Outer fake box to create rounded border look
        self.fake_box = ctk.CTkFrame(
            self,
            width=width,
            height=height,
            corner_radius=corner_radius,
            fg_color=fg_color,
            border_width=border_width
        )
        self.fake_box.pack(fill="both", expand=True)
        self.fake_box.pack_propagate(False)

        # Internal container for proper padding inside the fake box
        self.inner_frame = ctk.CTkFrame(self.fake_box, fg_color="transparent")
        self.inner_frame.pack(side="left", fill="both", expand=True, padx=(25,30))  # right pad keeps away from edge
        self.inner_frame.pack_propagate(False)

        # Actual entry (reduced width to leave space for icon)
        self.search_entry = ctk.CTkEntry(
            self.inner_frame,
            placeholder_text=entry_placeholder,
            width=width - icon_width - 40,  # subtract icon width and a bit extra for spacing
            height=height - 10,
            corner_radius=0,
            font=font,
            text_color=text_color,
            placeholder_text_color=placeholder_text_color,
            fg_color=fg_color,
            border_width=0,
            justify='left'
        )
        self.search_entry.pack(side="left", fill="y", pady=(0,5))

    def get(self):
        return self.search_entry.get()

    def set(self, text):
        self.search_entry.delete(0, "end")
        self.search_entry.insert(0, text)

    def clear(self):
        self.search_entry.delete(0, "end")
