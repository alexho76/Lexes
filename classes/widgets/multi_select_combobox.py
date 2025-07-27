### Multi-Select Combobox Custom Widget
### Dropdown/Combobox widget which allows user to select multiple options.
### Naming Convention: snake_case

import tkinter as tk
import customtkinter as ctk

class MultiSelectComboBox(ctk.CTkFrame):
    def __init__(self, master, *,
                 options,
                 width=200,
                 height=50,
                 font=None,
                 dropdown_font=None,
                 fg_color="white",
                 border_color="gray",
                 text_color="black",
                 selected_bg_color="#cce5ff",
                 selected_text_color="#004085",
                 require_frame_color="#e6f0ff",
                 corner_radius=8,
                 default_text="Select options ▼",
                 dropdown_bg_color="#C6E1B8",
                 on_close_callback=None,
                 **kwargs):
        super().__init__(master, width=width, fg_color="transparent", corner_radius=corner_radius, **kwargs)

        self.options = options
        self.width = width
        self.height = height
        self.font = font or ("Arial", 14)
        self.dropdown_font = dropdown_font or ("Arial", 12)
        self.fg_color = fg_color
        self.border_color = border_color
        self.text_color = text_color
        self.selected_bg_color = selected_bg_color
        self.selected_text_color = selected_text_color
        self.require_frame_color = require_frame_color
        self.corner_radius = corner_radius
        self.default_text = default_text
        self.dropdown_bg_color = dropdown_bg_color
        self.on_close_callback = on_close_callback

        self.selected_indices = set()
        self.option_frames = []
        self.option_labels = []
        self.prevent_reopen = False

        self.measure_font = ctk.CTkFont(family=self.dropdown_font[0], size=self.dropdown_font[1])

        numOptions = len(self.options)
        if numOptions < 5: # sets the height of the dropdown
            self.dropdown_height = 40 * numOptions + 25
        else: # max of 5 rows displayed -> 200 pixels of height
            self.dropdown_height = 200 + 25

        self.configure(border_width=1, border_color=self.border_color)

        self.selected_text_var = tk.StringVar(value=self.default_text)

        # Main container with rounded corners
        self.main_container = ctk.CTkFrame(
            self,
            width=self.width,
            height=self.height,
            corner_radius=self.corner_radius,
            fg_color=self.fg_color,
        )
        self.main_container.pack(fill="x")
        self.main_container.pack_propagate(False)

        self.dropdown_icon = ctk.CTkLabel(
            self.main_container,
            text="▼",
            font=self.font,
            text_color=self.text_color
        )
        self.dropdown_icon.pack(side="right", padx=(0, 25), pady=(4,10))

        self.main_label = ctk.CTkLabel(
            self.main_container,
            textvariable=self.selected_text_var,
            font=self.font,
            text_color=self.text_color,
            anchor="w"
        )
        self.main_label.pack(side="left", fill="x", expand=True, padx=(27, 0), pady=(4,10))

        # Click binding
        self.main_container.bind("<Button-1>", self._toggle_menu) # left click
        self.dropdown_icon.bind("<Button-1>", self._toggle_menu)
        self.main_label.bind("<Button-1>", self._toggle_menu)

        self.popup = None
        self.inner_frame = None
        self.is_menu_open = False

        self._create_menu_popup()

    def _create_menu_popup(self):
        self.popup = tk.Toplevel(self)
        self.popup.withdraw()
        self.popup.overrideredirect(True)
        self.popup.configure(bg=self.dropdown_bg_color)

        self.outer_frame = tk.Frame(self.popup, bg=self.dropdown_bg_color)
        self.outer_frame.pack(padx=0, pady=0, fill="both", expand=True)

        # Require frame (header) with ctk.CTkFrame
        self.require_frame = ctk.CTkFrame(self.outer_frame, fg_color=self.selected_bg_color, height=25, corner_radius=0)
        self.require_frame.grid(row=0, column=0, columnspan=2, sticky="ew")

        # Left: Require all tags? checkbox
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

        # Canvas and scrollbar (main scroll area)
        self.canvas = tk.Canvas(
            self.outer_frame,
            bg=self.dropdown_bg_color,
            highlightthickness=0,
            width=self.width,
            height=self.dropdown_height,
        )
        scrollbar = ctk.CTkScrollbar(self.outer_frame, orientation="vertical", command=self.canvas.yview,
                                      fg_color="transparent", button_color="#658657", button_hover_color="#719662")

        self.canvas.grid(row=1, column=0, sticky="nsew")
        scrollbar.grid(row=1, column=1, sticky="ns")

        self.outer_frame.grid_rowconfigure(1, weight=1)
        self.outer_frame.grid_columnconfigure(0, weight=1)

        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.inner_frame = tk.Frame(self.canvas, bg=self.dropdown_bg_color, width=self.width)
        self.inner_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        self.canvas.bind("<Enter>", lambda e: self._bind_mousewheel())
        self.canvas.bind("<Leave>", lambda e: self._unbind_mousewheel())

        for i, option in enumerate(self.options):
            row_frame = tk.Frame(self.inner_frame, bg=self.dropdown_bg_color, width=self.width, height=40)
            row_frame.pack(fill="x", anchor="w", pady=0)
            row_frame.pack_propagate(False)

            # Truncate text if necessary
            max_label_width = self.width - 30
            truncated_text = self._truncate_text(option, max_label_width, self.measure_font)

            label = ctk.CTkLabel(
                row_frame,
                text=truncated_text,
                font=self.dropdown_font,
                text_color=self.text_color,
                anchor="w",
                justify="left",
                width=self.width - 20,
            )
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

            row_frame.bind("<Button-1>", lambda e, idx=i: toggle_selection(idx))
            label.bind("<Button-1>", lambda e, idx=i: toggle_selection(idx))

            self.option_frames.append(row_frame)
            self.option_labels.append(label)

        self.popup.bind("<FocusOut>", self._on_popup_focus_out)

    def _update_option_visual(self, idx):
        selected = idx in self.selected_indices
        frame = self.option_frames[idx]
        label = self.option_labels[idx]

        if selected:
            frame.configure(bg=self.selected_bg_color)
            label.configure(text_color=self.selected_text_color)
        else:
            frame.configure(bg=self.dropdown_bg_color)
            label.configure(text_color=self.text_color)

    def _bind_mousewheel(self):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)

    def _unbind_mousewheel(self):
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")

    def _on_mousewheel(self, event):
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")

    def _toggle_menu(self, event=None):
        if self.is_menu_open:
            self._hide_menu()
        elif not self.prevent_reopen:
            self._show_menu()



    def _show_menu(self):
        x = self.winfo_rootx()
        y = self.winfo_rooty() + self.winfo_height()
        self.popup.geometry(f"{self.width}x{self.dropdown_height}+{x}+{y}")
        self.popup.deiconify()
        self.popup.focus_set()
        self.popup.bind("<Return>", self._on_enter_press)
        self.is_menu_open = True
        self.dropdown_icon.configure(text="▲")

    def _hide_menu(self):
        self.popup.withdraw()
        self.is_menu_open = False
        self.dropdown_icon.configure(text="▼")

        if self.on_close_callback:
            if self.no_tags_var.get():
                self.on_close_callback(None)
            else:
                self.on_close_callback(self.get_selected())

        self.prevent_reopen = True
        self.after(150, lambda: setattr(self, 'prevent_reopen', False))

    def _on_popup_focus_out(self, event=None):
        if self.is_menu_open:
            self._hide_menu()

    def _on_select(self):
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
        ellipsis = "..."
        ellipsis_width = font.measure(ellipsis)

        if font.measure(text) <= max_width_px:
            return text

        for i in range(len(text), 0, -1):
            sub_text = text[:i]
            if font.measure(sub_text) + ellipsis_width <= max_width_px:
                return sub_text + ellipsis

        return ellipsis  # fallback if even a single char is too wide


    def _add_tooltip(self, widget, text):
        tooltip = tk.Toplevel(widget)
        tooltip.withdraw()
        tooltip.overrideredirect(True)
        label = tk.Label(tooltip, text=text, bg="#CDE8C0", fg=self.text_color, padx=6, pady=2)
        label.pack()

        def show_tooltip(event):
            tooltip.geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
            tooltip.deiconify()

        def hide_tooltip(event):
            tooltip.withdraw()

        widget.bind("<Enter>", show_tooltip)
        widget.bind("<Leave>", hide_tooltip)


    def get_selected(self):
        return [self.options[i].strip() for i in sorted(self.selected_indices)]

    def _on_enter_press(self, event=None):
        if self.is_menu_open:
            self._hide_menu()

    def require_all_selected(self):
        return self.require_all_var.get()

    def refresh_options(self):
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

            label = ctk.CTkLabel(
                row_frame,
                text=truncated_text,
                font=self.dropdown_font,
                text_color=self.text_color,
                anchor="w",
                justify="left",
                width=self.width - 20,
            )
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
        
    
