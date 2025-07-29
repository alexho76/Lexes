"""
File: classes/widgets/single_select_combobox.py

Purpose:
    Defines the SingleSelectComboBox custom widget for the Lexes app. This widget provides a dropdown/combobox interface
    allowing the user to select a single option. Selection updates the widget's display and immediately triggers a callback and closes the menu.

Contains:
    - SingleSelectComboBox class: A CTkFrame-based widget with a dropdown menu for single selection.
    - Methods for menu display, selection, visual updates, mouse interaction, keyboard interaction, and retrieving the selected option.

Naming Conventions:
    - Class names: PascalCase (SingleSelectComboBox)
    - Public method names: snake_case (get_selected)
    - Private method names: snake_case, prefixed with an underscore (e.g., _show_menu, _on_select)
    - Attributes: snake_case (options, selected_index, option_labels)
    - General code: snake_case. NOTE: Custom widgets use snake_case while the rest of the codebase uses camelCase.

Usage:
    Use SingleSelectComboBox to provide a visually enhanced dropdown allowing selection of one item.
    Callback can be triggered on close with translated option value.
    SingleSelectComboBox used for sorting dropdown in Main Window.
"""

### Module Imports ###
import tkinter as tk
import customtkinter as ctk

class SingleSelectComboBox(ctk.CTkFrame):
    def __init__(self, master, *,
                 options,
                 width=200,
                 height=50,
                 font=None,
                 dropdown_font=None,
                 fg_color="white",
                 border_color="gray",
                 border_width=1,
                 text_color="black",
                 selected_bg_color="#cce5ff",
                 selected_text_color="#004085",
                 unselected_text_color,
                 corner_radius=8,
                 default_text="Select option ▼",
                 dropdown_bg_color="#C6E1B8",
                 on_close_callback=None,
                 ipadx=(27,0),
                 **kwargs):
        """
        Initialise the SingleSelectComboBox widget with styling, option list, and callback.
        """
        super().__init__(master, width=width, fg_color="transparent", corner_radius=corner_radius, border_color=border_color, border_width=border_width, **kwargs)

        ### Widget Appearance & Options ###
        self.options = options
        self.width = width
        self.height = height

        self.font = font or ("Arial", 14)
        self.dropdown_font = dropdown_font or ("Arial", 12)
        
        self.fg_color = fg_color
        self.border_color = border_color
        self.border_width = border_width
        self.text_color = text_color
        self.selected_bg_color = selected_bg_color
        self.selected_text_color = selected_text_color
        self.unselected_text_color = unselected_text_color
        
        self.corner_radius = corner_radius
        self.default_text = default_text
        self.dropdown_bg_color = dropdown_bg_color
        self.on_close_callback = on_close_callback
        self.ipadx = ipadx  # Padding for dropdown options

        ### Internal State ###
        self.selected_index = None # Index of currently selected option (None if nothing selected)
        self.option_frames = []
        self.option_labels = []
        self.prevent_reopen = False

        ### Options Translation (Mapping) ###
        self.options_dictionary = {
            "Newest": "dateDescending",
            "Oldest": "dateAscending",
            "A-Z": "alphabeticalAscending",
            "Z-A": "alphabeticalDescending",
            None: "dateDescending" # default option if nothing selected
        }

        ### Dropdown Height Calculation ###
        num_options = len(self.options)
        if num_options < 5:
            self.dropdown_height = 40 * num_options
        else:
            self.dropdown_height = 200

        self.configure(border_width=self.border_width, border_color=self.border_color)

        self.selected_text_var = tk.StringVar(value=self.default_text)

        ### Main Container (Rounded) ###
        self.main_container = ctk.CTkFrame(self,
                                           width=self.width,
                                           height=self.height,
                                           corner_radius=self.corner_radius,
                                           fg_color=self.fg_color,
                                           border_color=self.border_color,
                                           border_width=self.border_width)
        self.main_container.pack(fill="x")
        self.main_container.pack_propagate(False)

        self.dropdown_icon = ctk.CTkLabel(self.main_container,
                                          text="▼",
                                          font=self.font,
                                          text_color=self.text_color)
        self.dropdown_icon.pack(side="right", padx=(0, 25), pady=(4,10) )

        self.main_label = ctk.CTkLabel(self.main_container,
                                       textvariable=self.selected_text_var,
                                       font=self.font,
                                       text_color=self.text_color,
                                       anchor="w")
        self.main_label.pack(side="left", fill="x", expand=True, padx=self.ipadx, pady=(4,10))

        ### Bind Click Events ###
        self.main_container.bind("<Button-1>", self._toggle_menu) # left click
        self.dropdown_icon.bind("<Button-1>", self._toggle_menu)
        self.main_label.bind("<Button-1>", self._toggle_menu)

        ### Popup State ###
        self.popup = None
        self.inner_frame = None
        self.is_menu_open = False

        self._create_menu_popup()

    def _create_menu_popup(self) -> None:
        """
        Private Method
        Creates the popup dropdown menu with scrollable option list.
        Binds events for mouse wheel and option selection.
        """
        ### Toplevel Popup Setup ###
        self.popup = tk.Toplevel(self)
        self.popup.withdraw()
        self.popup.overrideredirect(True)
        self.popup.configure(bg=self.dropdown_bg_color)

        outer_frame = tk.Frame(self.popup, bg=self.dropdown_bg_color)
        outer_frame.pack(padx=0, pady=0)

        ### Canvas Setup ###
        self.canvas = tk.Canvas(outer_frame,
                                bg=self.dropdown_bg_color,
                                highlightthickness=0,
                                width=self.width,
                                height=self.dropdown_height)
        self.canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(outer_frame, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=scrollbar.set)

        ### Inner Frame for Options Rows ###
        self.inner_frame = tk.Frame(self.canvas, bg=self.dropdown_bg_color, width=self.width)
        self.inner_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        ### Mouse Enter/Leave Events on Scroll ###
        self.canvas.bind("<Enter>", lambda e: self._bind_mousewheel())
        self.canvas.bind("<Leave>", lambda e: self._unbind_mousewheel())

        ### Generate Option Rows ###
        for i, option in enumerate(self.options):
            row_frame = tk.Frame(self.inner_frame, bg=self.dropdown_bg_color, width=self.width, height=40)
            row_frame.pack(fill="x", anchor="w", pady=0)
            row_frame.pack_propagate(False)

            label = ctk.CTkLabel(row_frame,
                                 text=option,
                                 font=self.dropdown_font,
                                 text_color=self.unselected_text_color,
                                 anchor="w",
                                 justify="left",
                                 width=self.width - 20)
            label.pack(side="left", fill="x", expand=True, padx=10, pady=0)

            def select_option(idx=i):
                """
                Updates selected index, visuals, label, and closes dropdown.
                """
                # Set single selected index
                self.selected_index = idx
                
                self._update_all_options()
                self._on_select()

                # Close menu after selection
                self._hide_menu()

            row_frame.bind("<Button-1>", lambda e, idx=i: select_option(idx))
            label.bind("<Button-1>", lambda e, idx=i: select_option(idx))

            self.option_frames.append(row_frame)
            self.option_labels.append(label)

        self.popup.bind("<FocusOut>", self._on_popup_focus_out)

    def _update_option_visual(self, idx) -> None:
        """
        Private Method
        Updates the appearance of an option row and label based on selection.
        """
        selected = (self.selected_index == idx)
        frame = self.option_frames[idx]
        label = self.option_labels[idx]

        if selected:
            frame.configure(bg=self.selected_bg_color)
            label.configure(text_color=self.selected_text_color)
        else:
            frame.configure(bg=self.dropdown_bg_color)
            label.configure(text_color=self.unselected_text_color)

    def _update_all_options(self) -> None:
        """
        Private Method
        Updates the visual appearance of all option rows and labels.
        """
        for idx in range(len(self.options)):
            self._update_option_visual(idx)

    def _bind_mousewheel(self) -> None:
        """
        Private Method
        Enables mouse wheel scrolling for the dropdown canvas.
        Supports various mouse wheel events for different platforms.
        """ 
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)

    def _unbind_mousewheel(self) -> None:
        """
        Private Method
        Disables mouse wheel scrolling for the dropdown canvas.
        """
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")

    def _on_mousewheel(self, event) -> None:
        """
        Private Method
        Handles mouse wheel scrolling event for the dropdown canvas.
        """
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")

    def _toggle_menu(self, event=None) -> None:
        """
        Private Method
        Toggles the visibility of the dropdown menu.
        Opens the menu if closed; hides it if open.
        """
        if self.is_menu_open:
            self._hide_menu()
        elif not self.prevent_reopen:
            self._show_menu()

    def _show_menu(self) -> None:
        """
        Private Method
        Displays the dropdown menu below the combobox.
        Focuses the popup for keyboard interaction.
        """
        x = self.winfo_rootx()
        y = self.winfo_rooty() + self.winfo_height()
        self.popup.geometry(f"{self.width}x{self.dropdown_height}+{x}+{y}")
        self.popup.deiconify()
        self.popup.focus_set()
        self.popup.bind("<Return>", self._on_enter_press)
        self.is_menu_open = True
        self.dropdown_icon.configure(text="▲")

    def _hide_menu(self) -> None:
        """
        Private Method
        Hides the dropdown menu popup and updates state/visuals.
        Triggers the on_close_callback if provided.
        Prevents immediate reopening.
        """
        self.popup.withdraw()
        self.is_menu_open = False
        self.dropdown_icon.configure(text="▼")

        # Trigger callback if set
        if self.on_close_callback:
            translated_option = self.options_dictionary[self.get_selected()]
            self.on_close_callback(translated_option)

        self.prevent_reopen = True
        # Allow reopening after a short delay to prevent flickering
        self.after(150, lambda: setattr(self, 'prevent_reopen', False))

    def _on_popup_focus_out(self, event=None) -> None:
        """
        Private Method
        Handles loss of focus from the dropdown popup.
        Closes the menu if it is open.
        """
        if self.is_menu_open:
            self._hide_menu()

    def _on_select(self) -> None:
        """
        Private Method
        Updates the main label text based on the selected option.
        """
        if self.selected_index is None:
            self.selected_text_var.set(self.default_text)
        else:
            self.selected_text_var.set(self.options[self.selected_index])
    
    def _on_enter_press(self, event=None) -> None:
        """
        Private Method
        Handles pressing Enter while the dropdown menu is open.
        Closes the menu.
        """
        if self.is_menu_open:
            self._hide_menu()
    
    def get_selected(self) -> str | None:
        """
        Public Method
        Returns the currently selected option string (or None if nothing selected).
        """
        if self.selected_index is None:
            return None
        return self.options[self.selected_index]