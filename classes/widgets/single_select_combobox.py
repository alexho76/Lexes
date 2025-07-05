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
                 text_color="black",
                 selected_bg_color="#cce5ff",
                 selected_text_color="#004085",
                 hover_color="#e6f0ff",
                 corner_radius=8,
                 default_text="Select option ▼",
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
        self.hover_color = hover_color
        self.corner_radius = corner_radius
        self.default_text = default_text

        self.selected_index = None  # Single selection index, None if nothing selected
        self.option_frames = []
        self.option_labels = []
        self.prevent_reopen = False

        numOptions = len(self.options)
        if numOptions < 5:
            self.dropdown_height = 40 * numOptions
        else:
            self.dropdown_height = 200

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
        self.dropdown_icon.pack(side="right", padx=(0, 20), pady=(6,10) )

        self.main_label = ctk.CTkLabel(
            self.main_container,
            textvariable=self.selected_text_var,
            font=self.font,
            text_color=self.text_color,
            anchor="w"
        )
        self.main_label.pack(side="left", fill="x", expand=True, padx=(20, 0), pady=(4,10))

        # Click binding
        self.main_container.bind("<Button-1>", self._toggle_menu)
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
        self.popup.configure(bg=self.fg_color)

        outer_frame = tk.Frame(self.popup, bg=self.fg_color)
        outer_frame.pack(padx=0, pady=0)

        self.canvas = tk.Canvas(
            outer_frame,
            bg=self.fg_color,
            highlightthickness=0,
            width=self.width,
            height=self.dropdown_height,
        )
        self.canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(outer_frame, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.inner_frame = tk.Frame(self.canvas, bg=self.fg_color, width=self.width)
        self.inner_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        self.canvas.bind("<Enter>", lambda e: self._bind_mousewheel())
        self.canvas.bind("<Leave>", lambda e: self._unbind_mousewheel())

        for i, option in enumerate(self.options):
            row_frame = tk.Frame(self.inner_frame, bg=self.fg_color, width=self.width, height=40)
            row_frame.pack(fill="x", anchor="w", pady=0)
            row_frame.pack_propagate(False)

            label = ctk.CTkLabel(
                row_frame,
                text=option,
                font=self.dropdown_font,
                text_color=self.text_color,
                anchor="w",
                justify="left",
                width=self.width - 20,
            )
            label.pack(side="left", fill="x", expand=True, padx=10, pady=0)

            def select_option(idx=i):
                # Set single selected index
                self.selected_index = idx
                # Update visuals
                self._update_all_options()
                # Update label
                self._on_select()
                # Close menu after selection
                self._hide_menu()

            row_frame.bind("<Button-1>", lambda e, idx=i: select_option(idx))
            label.bind("<Button-1>", lambda e, idx=i: select_option(idx))

            self.option_frames.append(row_frame)
            self.option_labels.append(label)

        self.popup.bind("<FocusOut>", self._on_popup_focus_out)

    def _update_option_visual(self, idx):
        selected = (self.selected_index == idx)
        frame = self.option_frames[idx]
        label = self.option_labels[idx]

        if selected:
            frame.configure(bg=self.selected_bg_color)
            label.configure(text_color=self.selected_text_color)
        else:
            frame.configure(bg=self.fg_color)
            label.configure(text_color=self.text_color)

    def _update_all_options(self):
        for idx in range(len(self.options)):
            self._update_option_visual(idx)

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
        self.is_menu_open = True
        self.dropdown_icon.configure(text="▲")

    def _hide_menu(self):
        self.popup.withdraw()
        self.is_menu_open = False
        self.dropdown_icon.configure(text="▼")

        print("Selected option:", self.get_selected())

        self.prevent_reopen = True
        self.after(150, lambda: setattr(self, 'prevent_reopen', False))

    def _on_popup_focus_out(self, event=None):
        if self.is_menu_open:
            self._hide_menu()

    def _on_select(self):
        if self.selected_index is None:
            self.selected_text_var.set(self.default_text)
        else:
            self.selected_text_var.set(self.options[self.selected_index])

    def get_selected(self):
        if self.selected_index is None:
            return None
        return self.options[self.selected_index]
