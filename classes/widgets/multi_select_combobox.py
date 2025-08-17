"""
File: classes/widgets/multi_select_combobox.py

Purpose:
    Defines the MultiSelectComboBox custom widget for the Lexes app. This widget provides a dropdown/combobox
    that allows users to select multiple options simultaneously, with support for changing selection requirements.

Contains:
    - MultiSelectComboBox class: A CTkFrame-based widget containing a dropdown list with checkboxes, "Require all tags" and "None" toggles,
    tooltips for truncated text, and scrollable options.
    - Methods for showing/hiding the dropdown, updating selection visuals, refreshing options, and retrieving selected values.

Naming Conventions:
    - Class names: PascalCase (MultiSelectComboBox)
    - Public method names: snake_case (get_selected, require_all_selected, refresh_options)
    - Private method names: snake_case, prefixed with an underscore (e.g., _toggle_menu, _create_menu_popup)
    - Attributes: snake_case (option_frames, option_labels, selected_indices, etc.)
    - General code: snake_case. NOTE: Custom widgets use snake_case while the rest of the codebase uses camelCase.

Usage:
    Use MultiSelectComboBox to provide a flexible dropdown that enables multi-selection for tags, categories, or other options.
    Supports dynamic option refresh and "require all" and "None" logic for advanced workflows.
    MultiSelectComboBox used for tag dropdown in Main Window.
"""

### Module Imports ###
import tkinter as tk
import customtkinter as ctk

class MultiSelectComboBox(ctk.CTkFrame):
    def __init__(self, master, *,
                 options: list[str],
                 width: int = 200,
                 height: int = 50,
                 font: tuple = None,
                 dropdown_font: tuple = None,
                 fg_color: str = "white",
                 border_color: str = "gray",
                 text_color: str = "black",
                 selected_bg_color: str = "#cce5ff",
                 selected_text_color: str = "#004085",
                 require_frame_color: str = "#e6f0ff",
                 corner_radius: int = 8,
                 default_text: str = "Select options ▼",
                 dropdown_bg_color: str = "#C6E1B8",
                 on_close_callback: callable = None,
                 **kwargs):
        """
        Initialise the MultiSelectComboBox widget with custom styles, options, and callbacks.
        - master (CTk): The parent widget for the MultiSelectComboBox. CTk so it can use customTkinter features.
        - options (list[str]): The list of options to display in the dropdown. List of strings so it is iterable and represents multiple selections as text.
        - width (int): The width of the dropdown. Integer as it represents the dropdown width in pixels.
        - height (int): The height of the dropdown. Integer as it represents the dropdown height in pixels.
        - font (tuple): The font configuration for the dropdown text. Tuple as it represents the font family and size.
        - dropdown_font (tuple): The font configuration for the dropdown options. Tuple as it represents the font family and size.
        - fg_color (str): The foreground color for the dropdown. String as it represents a color value.
        - border_color (str): The border color for the dropdown. String as it represents a color value.
        - text_color (str): The text color for the dropdown. String as it represents a color value.
        - selected_bg_color (str): The background color for selected options. String as it represents a color value.
        - selected_text_color (str): The text color for selected options. String as it represents a color value.
        - require_frame_color (str): The background color for the "Require All Tags?" frame. String as it represents a color value.
        - corner_radius (int): The corner radius for the dropdown. Integer as it represents the corner radius in pixels.
        - default_text (str): The default text to display when no options are selected. String as it represents the default text to be displayed in the label.
        - dropdown_bg_color (str): The background color for the dropdown. String as it represents a color value.
        - on_close_callback (callable): The callback function to call when the dropdown is closed. Callable as it represents a callback function.
        """
        super().__init__(master, width=width, fg_color="transparent", corner_radius=corner_radius, **kwargs)

        ### Config and State ###
        self.options = options # list of options to display in the dropdown
        self.width = width
        self.height = height
        self.font = font or ("Arial", 14)
        self.dropdown_font = dropdown_font or ("Arial", 12)
        self.fg_color = fg_color
        self.border_color = border_color
        self.text_color = text_color
        self.selected_bg_color = selected_bg_color
        self.selected_text_color = selected_text_color
        self.require_frame_color = require_frame_color # color for the "Require All Tags?" frame
        self.corner_radius = corner_radius
        self.default_text = default_text # text to display when no options are selected
        self.dropdown_bg_color = dropdown_bg_color
        self.on_close_callback = on_close_callback # callback to execute when the dropdown is closed

        ### Option Config ###
        self.selected_indices = set() # Uses set for efficient membership testing
        self.option_frames = [] # list of frames for each option in the dropdown
        self.option_labels = [] # list of labels for each option in the dropdown
        
        self.prevent_reopen = False # flag to prevent immediate reopening of the dropdown after closing
        self.measure_font = ctk.CTkFont(family=self.dropdown_font[0], size=self.dropdown_font[1]) # font for measuring text width

        # Dynamically set dropdown height based on number of options
        numOptions = max(1, len(self.options))
        if numOptions < 5:
            self.dropdown_height = 40 * numOptions + 25
        else: # Max height for 5 rows  displayed
            self.dropdown_height = 200 + 25

        self.configure(border_width=1, border_color=self.border_color)

        self.selected_text_var = tk.StringVar(value=self.default_text)

        ### Main Container (Rounded) ###
        self.main_container = ctk.CTkFrame(self,
                                           width=self.width,
                                           height=self.height,
                                           corner_radius=self.corner_radius,
                                           fg_color=self.fg_color)
        self.main_container.pack(fill="x")
        self.main_container.pack_propagate(False)

        self.dropdown_icon = ctk.CTkLabel(self.main_container,
                                          text="▼",
                                          font=self.font,
                                          text_color=self.text_color)
        self.dropdown_icon.pack(side="right", padx=(0, 25), pady=(4,10))

        self.main_label = ctk.CTkLabel(self.main_container,
                                       textvariable=self.selected_text_var,
                                       font=self.font,
                                       text_color=self.text_color,
                                       anchor="w")
        self.main_label.pack(side="left", fill="x", expand=True, padx=(27, 0), pady=(4,10))

        ### Click binding to open/close the dropdown ###
        self.main_container.bind("<Button-1>", self._toggle_menu) # left click
        self.dropdown_icon.bind("<Button-1>", self._toggle_menu)
        self.main_label.bind("<Button-1>", self._toggle_menu)

        self.popup = None
        self.inner_frame = None
        self.is_menu_open = False

        ### Build Dropdown Popup ###
        self._create_menu_popup()

    def _create_menu_popup(self) -> None:
        """
        Private Method

        Creates the dropdown popup window and populates it with option frames, checkboxes, and labels.
        """
        self.popup = tk.Toplevel(self)
        self.popup.withdraw()
        self.popup.overrideredirect(True)
        self.popup.configure(bg=self.dropdown_bg_color)

        self.outer_frame = tk.Frame(self.popup, bg=self.dropdown_bg_color)
        self.outer_frame.pack(padx=0, pady=0, fill="both", expand=True)

        ### 'Require All Tags?' and 'None' Frame (Header) ###
        self.require_frame = ctk.CTkFrame(self.outer_frame, fg_color=self.selected_bg_color, height=25, corner_radius=0)
        self.require_frame.grid(row=0, column=0, columnspan=2, sticky="ew")

        # Left: Require All Tags? Checkbox
        self.require_all_var = tk.BooleanVar(value=False)
        self.require_checkbox = ctk.CTkCheckBox(self.require_frame,
                                                text="Require all tags?",
                                                variable=self.require_all_var,
                                                checkbox_height=15,
                                                checkbox_width=15,
                                                font=("Bahnschrift", 12),
                                                text_color=self.selected_text_color,
                                                fg_color=self.dropdown_bg_color,
                                                hover_color=self.text_color,
                                                border_color=self.text_color,
                                                checkmark_color='white',
                                                border_width=1,
                                                state="disabled",
                                                text_color_disabled="#9FA69C")
        self.require_checkbox.grid(row=0, column=0, sticky="w", padx=10, pady=0)

        # Right: None label and checkbox
        self.no_tags_var = tk.BooleanVar(value=False)
        self.no_tags_frame = ctk.CTkFrame(self.require_frame, fg_color="transparent", corner_radius=0)
        self.no_tags_frame.grid(row=0, column=1, sticky="e", padx=5, pady=0)

        self.no_tags_checkbox = ctk.CTkCheckBox(self.no_tags_frame,
                                                text="",
                                                variable=self.no_tags_var,
                                                checkbox_height=15,
                                                checkbox_width=15,
                                                width=0,
                                                fg_color=self.dropdown_bg_color,
                                                hover_color=self.text_color,
                                                border_color=self.text_color,
                                                checkmark_color='white',
                                                border_width=1,
                                                state="normal")
        self.no_tags_checkbox.pack(side="right", pady=(4,0))

        self.no_tags_label = ctk.CTkLabel(self.no_tags_frame,
                                          text="None",
                                          font=("Bahnschrift", 12),
                                          text_color=self.selected_text_color,
                                          bg_color="transparent",)
        self.no_tags_label.pack(side="right", pady=0, padx=(0,7.5))

        # Make the left column expand, right column hugs the edge
        self.require_frame.grid_columnconfigure(0, weight=1)
        self.require_frame.grid_columnconfigure(1, weight=0)

        ### Canvas and Scrollbar ###
        self.canvas = tk.Canvas(self.outer_frame,
                                bg=self.dropdown_bg_color,
                                highlightthickness=0,
                                width=self.width,
                                height=self.dropdown_height)
        scrollbar = ctk.CTkScrollbar(self.outer_frame, orientation="vertical", command=self.canvas.yview,
                                     fg_color="transparent", button_color="#658657", button_hover_color="#719662")

        self.canvas.grid(row=1, column=0, sticky="nsew")
        scrollbar.grid(row=1, column=1, sticky="ns")

        self.outer_frame.grid_rowconfigure(1, weight=1)
        self.outer_frame.grid_columnconfigure(0, weight=1)

        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.inner_frame = tk.Frame(self.canvas, bg=self.dropdown_bg_color, width=self.width)
        self.inner_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        ### Scroll Bindings ###
        self.canvas.bind("<Enter>", lambda e: self._bind_mousewheel())
        self.canvas.bind("<Leave>", lambda e: self._unbind_mousewheel())

        ### Create option rows with checkboxes and labels ###
        for i, option in enumerate(self.options):
            row_frame = tk.Frame(self.inner_frame, bg=self.dropdown_bg_color, width=self.width, height=40)
            row_frame.pack(fill="x", anchor="w", pady=0)
            row_frame.pack_propagate(False)

            # Truncate text if necessary
            max_label_width = self.width - 30
            truncated_text = self._truncate_text(option, max_label_width, self.measure_font)

            label = ctk.CTkLabel(row_frame,
                                 text=truncated_text,
                                 font=self.dropdown_font,
                                 text_color=self.text_color,
                                 anchor="w",
                                 justify="left",
                                 width=self.width - 20)
            label.pack(side="left", fill="x", expand=True, padx=10, pady=0)

            # Add tooltip if text was truncated
            if truncated_text != option:
                self._add_tooltip(label, option)

            def toggle_selection(idx=i):
                if idx in self.selected_indices:
                    self.selected_indices.remove(idx)
                else:
                    self.selected_indices.add(idx)
                self._update_option_visual(idx)
                self._on_select()

            # Bind click for selection
            row_frame.bind("<Button-1>", lambda e, idx=i: toggle_selection(idx))
            label.bind("<Button-1>", lambda e, idx=i: toggle_selection(idx))

            self.option_frames.append(row_frame)
            self.option_labels.append(label)

        # Focus out binding to close the popup
        self.popup.bind("<FocusOut>", self._on_popup_focus_out)

    def _update_option_visual(self, idx) -> None:
        """
        Private Method

        Updates the appearance of the option at index idx based on whether it is selected.
        - idx (int): The index of the option to update. Integer as it represents the position of the option in the list.
        """
        selected = idx in self.selected_indices
        frame = self.option_frames[idx]
        label = self.option_labels[idx]

        if selected:
            frame.configure(bg=self.selected_bg_color)
            label.configure(text_color=self.selected_text_color)
        else:
            frame.configure(bg=self.dropdown_bg_color)
            label.configure(text_color=self.text_color)

    def _bind_mousewheel(self) -> None:
        """
        Private Method

        Enables mouse wheel scrolling for the dropdown canvas.
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

        Handles mouse wheel scroll events for the dropdown canvas.
        - event (tk.Event): The mouse wheel event. Tkinter Event containing information about the scroll.
        """
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")

    def _toggle_menu(self, event=None) -> None:
        """
        Private Method

        Toggles the dropdown menu open or closed.
        - event (tk.Event): The event that triggered the toggle. Tkinter Event containing information about the toggle action.
        """
        if self.is_menu_open:
            self._hide_menu()
        elif not self.prevent_reopen:
            self._show_menu()

    def _show_menu(self) -> None:
        """
        Private Method

        Displays the dropdown menu and focuses the popup.
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

        Hides the dropdown menu and updates state.
        """
        self.popup.withdraw()
        self.is_menu_open = False
        self.dropdown_icon.configure(text="▼")

        # Call the close callback if provided
        if self.on_close_callback:
            if self.no_tags_var.get():
                self.on_close_callback(None)
            else:
                self.on_close_callback(self.get_selected())

        # Prevent immediate reopening (prevents flickering)
        self.prevent_reopen = True
        self.after(150, lambda: setattr(self, 'prevent_reopen', False))

    def _on_popup_focus_out(self, event=None) -> None:
        """
        Private Method

        Handles popup losing focus (closes menu).
        - event (tk.Event): The event that triggered the focus out. Tkinter Event containing information about the focus event.
        """
        if self.is_menu_open:
            self._hide_menu()

    def _on_select(self) -> None:
        """
        Private Method

        Updates selection state, visual feedback, and toggles checkboxes as needed.
        """
        count = len(self.selected_indices)

        # Update label text
        if count == 0:
            self.selected_text_var.set(self.default_text)
        elif count == 1:
            self.selected_text_var.set("1 tag selected...")
        else:
            self.selected_text_var.set(f"{count} tags selected...")

        # Enable or disable the checkbox
        if count == 0:
            # Disable require checkbox if no tags selected
            self.require_checkbox.configure(state="disabled")
            self.require_all_var.set(False)  # optional: uncheck when disabled

            # Enable "None" checkbox if no tags selected
            self.no_tags_checkbox.configure(state="normal")
            self.no_tags_label.configure(text_color='white')

        else: # count > 0
            # Enable require checkbox if any tags selected
            self.require_checkbox.configure(state="normal")

            # Disable "None" checkbox if any tags selected
            self.no_tags_checkbox.configure(state="disabled")
            self.no_tags_var.set(False)  # optional: uncheck when disabled
            self.no_tags_label.configure(text_color="#9FA69C")


    def _truncate_text(self, text: str, max_width_px: int, font) -> str:
        """
        Private Method

        Truncates text with ellipsis if it exceeds max_width_px in the given font. Returns string text either regular or truncated with ellipsis.
        - text (str): The text to truncate. String as it represents the content to be displayed.
        - max_width_px (int): The maximum width of the text to be truncated. Integer as it represents the width in pixels.
        - font (CTkFont): The font used for measuring text width. CTkFont as it represents the text styling.
        """
        ellipsis = "..."
        ellipsis_width = font.measure(ellipsis)

        if font.measure(text) <= max_width_px:
            return text

        for i in range(len(text), 0, -1):
            sub_text = text[:i]
            if font.measure(sub_text) + ellipsis_width <= max_width_px:
                return sub_text + ellipsis

        return ellipsis  # fallback if even a single char is too wide


    def _add_tooltip(self, widget, text) -> None:
        """
        Private Method

        Adds a tooltip to the given widget displaying the full text when hovered.
        - widget (CTk/Tk): The widget to attach the tooltip to. CTk/Tk as it represents the UI element which the tooltip will be attached to.
        - text (str): The text to display in the tooltip. String as it represents the content to be shown.
        """
        tooltip = tk.Toplevel(widget)
        tooltip.withdraw()
        tooltip.overrideredirect(True)
        label = tk.Label(tooltip, text=text, bg="#CDE8C0", fg=self.text_color, padx=6, pady=2)
        label.pack()

        def show_tooltip(event):
            """
            Show tooltip near the widget when hovered.
            """
            tooltip.geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
            tooltip.deiconify()

        def hide_tooltip(event):
            """
            Hide tooltip when mouse leaves the widget.
            """
            tooltip.withdraw()

        # Bind hover events to show/hide tooltip when entering/leaving the widget
        widget.bind("<Enter>", show_tooltip)
        widget.bind("<Leave>", hide_tooltip)

    def _on_enter_press(self, event=None) -> None:
        """
        Private Method

        Handles pressing Enter key to close dropdown.
        - event (tk.Event): The event that triggered the key press. Tkinter Event containing information about the key press.
        """
        if self.is_menu_open:
            self._hide_menu()

    def get_selected(self) -> list:
        """
        Public Method

        Returns a list of selected options as strings.
        """
        return [self.options[i].strip() for i in sorted(self.selected_indices)]

    def require_all_selected(self) -> bool:
        """
        Public Method

        Returns True if "Require all tags?" is checked, else False.
        """
        return self.require_all_var.get()

    def refresh_options(self) -> None:
        """
        Public Method

        Resizes the dropdown box if needed, refreshes the option list in the dropdown, preserving previous selection.
        """
        # Dynamically resize the dropdown height based on number of options
        numOptions = max(1, len(self.options))
        if numOptions < 5:
            self.dropdown_height = 40 * numOptions + 25
        else:  # Max height for 5 rows displayed
            self.dropdown_height = 200 + 25

        # Save current selected tags (indices)
        preserved_indices = set(self.selected_indices)
        preserved_require_all = self.require_all_var.get()

        # Clear visual dropdown content
        for frame in self.option_frames:
            frame.destroy()
        self.option_frames.clear()
        self.option_labels.clear()

        # Rebuild dropdown with new options
        for i, option in enumerate(self.options):
            row_frame = tk.Frame(self.inner_frame, bg=self.dropdown_bg_color, width=self.width, height=40)
            row_frame.pack(fill="x", anchor="w", pady=0)
            row_frame.pack_propagate(False)

            # Truncate text if necessary
            max_label_width = self.width - 25
            truncated_text = self._truncate_text(option, max_label_width, self.measure_font)

            label = ctk.CTkLabel(row_frame,
                                 text=truncated_text,
                                 font=self.dropdown_font,
                                 text_color=self.text_color,
                                 anchor="w",
                                 justify="left",
                                 width=self.width - 20)
            label.pack(side="left", fill="x", expand=True, padx=10, pady=0)

            # Add tooltip if text was truncated
            if truncated_text != option:
                self._add_tooltip(label, option)

            def toggle_selection(idx=i):
                """
                Toggle selection of the option at the given index.
                """
                if idx in self.selected_indices:
                    self.selected_indices.remove(idx)
                else:
                    self.selected_indices.add(idx)
                self._update_option_visual(idx)
                self._on_select()

            # Bind click for selection
            row_frame.bind("<Button-1>", lambda e, idx=i: toggle_selection(idx))
            label.bind("<Button-1>", lambda e, idx=i: toggle_selection(idx))

            self.option_frames.append(row_frame)
            self.option_labels.append(label)

            # Restore selection visuals if tag was selected before
            if i < len(self.options) and i in preserved_indices:
                self.selected_indices.add(i)
                self._update_option_visual(i)

        # Restore state of require all checkbox
        if self.selected_indices:
            self.require_checkbox.configure(state="normal")
            self.require_all_var.set(preserved_require_all)

            count = len(self.selected_indices)
            if count == 0:
                self.selected_text_var.set(self.default_text)
            elif count == 1:
                self.selected_text_var.set("1 tag selected...")
            else:
                self.selected_text_var.set(f"{count} tags selected...")
        else:
            self.require_checkbox.configure(state="disabled")
            self.require_all_var.set(False)
            self.selected_text_var.set(self.default_text)
    
    def reset_scroll(self) -> None:
        """
        Public Method

        Resets the dropdown's scroll position to the top. Intended to be called after drastic reductions in tag numbers. E.g. after mass deletion
        to avoid lingering at the bottom of the scrollable area which would be now empty.
        """
        if self.canvas is not None:
            self.canvas.yview_moveto(0)