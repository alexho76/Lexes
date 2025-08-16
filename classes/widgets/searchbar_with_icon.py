"""
File: classes/widgets/searchbar_with_icon.py

Purpose:
    Defines the SearchBarWithIcon custom widget for the Lexes app. This widget provides a search bar with an interactive icon,
    supporting both enter key search and clickable icon activation. The icon visually reacts to hover and search events.

Contains:
    - SearchBarWithIcon class: A CTkFrame-based widget containing a search entry and a clickable/hoverable icon.
    - Methods for getting/setting/clearing the search text, handling search actions, and updating icon appearance.

Naming Conventions:
    - Class names: PascalCase (SearchBarWithIcon)
    - Public method names: snake_case (get, set, clear)
    - Private method names: snake_case, prefixed with an underscore (e.g., _on_icon_click, _on_hover_enter)
    - Attributes: snake_case (search_entry, icon_button, icon_image_default, etc.)
    - General code: snake_case. NOTE: Custom widgets use snake_case while the rest of the codebase uses camelCase.

Usage:
    Use SearchBarWithIcon to provide a visually enhanced search bar with both keyboard and icon-based search submission.
    The icon responds to hover events and search actions for better UX.
    SearchBarWithIcon used for searchbar in Main Window.
"""

### Module Imports ###
import customtkinter as ctk

class SearchBarWithIcon(ctk.CTkFrame):
    def __init__(self, master, *,
                 width: int = 500,
                 height: int = 50,
                 corner_radius: int = 200,
                 entry_placeholder: str = "Search by keyword",
                 font: tuple = ("League Spartan", 36),
                 text_color: str = "green",
                 placeholder_text_color: str = "darkgreen",
                 fg_color: str = "lightgray",
                 border_width: int = 0,
                 icon = None,
                 icon_hover = None,
                 icon_width: int = 60,
                 on_search_callback: callable = None,
                 **kwargs):
        """
        Initialise the SearchBarWithIcon widget with custom styles, icons, and callback.
        - master (CTk): The parent widget for the SearchBarWithIcon. CTk so it can use customTkinter features.
        - width (int): The width of the search bar. Integer as it represents the pixel width.
        - height (int): The height of the search bar. Integer as it represents the pixel height.
        - corner_radius (int): The corner radius of the search bar. Integer as it represents the pixel radius.
        - entry_placeholder (str): The placeholder text for the search entry. String as it represents the default text.
        - font (tuple): The font configuration for the search entry text. Tuple as it represents the font family and size.
        - text_color (str): The text color for the search entry. String as it represents a color value.
        - placeholder_text_color (str): The text color for the placeholder text. String as it represents a color value.
        - fg_color (str): The foreground color for the search bar. String as it represents a color value.
        - border_width (int): The border width for the search bar. Integer as it represents the width in pixels.
        - icon (Image): The default icon for the search button. Image as it represents the icon image.
        - icon_hover (Image): The hover icon for the search button. Image as it represents the icon image.
        - icon_width (int): The width of the search icon. Integer as it represents the width in pixels.
        - on_search_callback (callable): The callback function to call when the search is triggered. Callable as it represents a callback function.
        """
        super().__init__(master, width=width, height=height, fg_color="transparent", **kwargs)
        ### Appearance ###
        self.width = width
        self.height = height
        self.icon_width = icon_width

        self.on_search_callback = on_search_callback # callback for search action

        self.pack_propagate(False)

        ### Outer Fake Box (Rounded) ###
        self.fake_box = ctk.CTkFrame(self,
                                     width=width,
                                     height=height-3,
                                     corner_radius=corner_radius,
                                     fg_color=fg_color,
                                     border_width=border_width)
        self.fake_box.pack(fill="both", expand=True)
        self.fake_box.pack_propagate(False)

        ### Internal container ###
        self.inner_frame = ctk.CTkFrame(self.fake_box, fg_color=fg_color)
        self.inner_frame.pack(side="left", fill="both", expand=True, padx=(25, 70),pady=1)  # right pad keeps away from edge
        self.inner_frame.pack_propagate(False)

        ### Search Entry (Reduced Width to For Icon) ###
        self.search_entry = ctk.CTkEntry(self.inner_frame,
                                         placeholder_text=entry_placeholder,
                                         width=width - self.icon_width - 10,  # subtract icon width and a bit extra for spacing
                                         height=height - 13,
                                         corner_radius=0,
                                         font=font,
                                         text_color=text_color,
                                         placeholder_text_color=placeholder_text_color,
                                         fg_color=fg_color,
                                         border_width=0,
                                         justify='left')
        self.search_entry.pack(side="left", fill="y", pady=(0, 6))

        ### Icon Button Setup ###
        self.icon_image_default = ctk.CTkImage(light_image=icon, dark_image=icon, size=(38,38))
        self.icon_image_hover = ctk.CTkImage(light_image=icon_hover, dark_image=icon_hover, size=(40,40))

        self.icon_button = ctk.CTkButton(self.fake_box,
                                         image=self.icon_image_default,
                                         text="",
                                         fg_color=fg_color,
                                         corner_radius=0,
                                         width=self.icon_width,
                                         height=self.icon_width,
                                         command=self._on_icon_click,
                                         hover_color=fg_color)
        self.icon_button.place(x=self.width - self.icon_width - 25, y=(self.height - (self.height - 2)) // 2 + 5)

        ### Bind events for icon hover and search entry ###
        self.icon_button.bind("<Enter>", self._on_hover_enter)
        self.icon_button.bind("<Leave>", self._on_hover_leave)
        self.search_entry.bind("<Return>", self._on_enter_press)
    
    def _on_icon_click(self, event=None) -> None:
        """
        Private Method

        Handles icon button click event, triggers search callback, and updates icon appearance.
        """
        if self.on_search_callback:
            self.on_search_callback(self.get())

        self._on_hover_leave(event)

        self.after(100, lambda: self._on_hover_enter(event))
        self.search_entry.master.focus_set()
    
    def _on_enter_press(self, event=None) -> None:
        """
        Private Method

        Handles Enter key press in search entry, triggers search callback, and updates icon appearance.
        - event (tk.Event): The event object associated with the key press. Tkinter Event so it can be used to identify the widget that triggered the enter press event.
        """
        if self.on_search_callback:
            self.on_search_callback(self.get())

        self._on_hover_enter(event)

        self.after(100, lambda: self._on_hover_leave(event))
        self.search_entry.master.focus_set()

    def _on_hover_enter(self, event) -> None:
        """
        Private Method

        Handles mouse entering icon button, updates icon to hover image.
        - event (tk.Event): The event object associated with the mouse enter event. Tkinter Event so it can be used to identify the widget that triggered the hover event.
        """
        self.icon_button.configure(image=self.icon_image_hover)
        self.icon_button.place(x=self.width - self.icon_width - 26, y=(self.height - (self.height - 2)) // 2 + 5)

    def _on_hover_leave(self, event) -> None:
        """
        Private Method

        Handles mouse leaving icon button, returns icon to default image.
        - event (tk.Event): The event object associated with the mouse leave event. Tkinter Event so it can be used to identify the widget that triggered the hover event.
        """
        self.icon_button.configure(image=self.icon_image_default)
        self.icon_button.place(x=self.width - self.icon_width - 25, y=(self.height - (self.height - 2)) // 2 + 5)
    
    def get(self) -> str:
        """
        Public Method

        Returns the current search text as a string.
        """
        return self.search_entry.get()

    def set(self, text: str) -> None:
        """
        Public Method

        Sets the search entry text to inputted string.
        - text (str): The text to set in the search entry. String as it represents the search query displayed as a label.
        """
        self.search_entry.delete(0, "end")
        self.search_entry.insert(0, text)

    def clear(self) -> None:
        """
        Public Method

        Clears the search entry text.
        """
        self.search_entry.delete(0, "end")