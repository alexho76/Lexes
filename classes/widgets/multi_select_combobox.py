import tkinter as tk
import customtkinter as ctk

class MultiSelectComboBox(ctk.CTkFrame):
    def __init__(self, master, *,
                 options,
                 width=200,
                 dropdown_height=150,
                 font=None,
                 dropdown_font=None,
                 fg_color="white",
                 border_color="gray",
                 text_color="black",
                 selected_bg_color="#cce5ff",
                 selected_text_color="#004085",
                 hover_color="#e6f0ff",
                 corner_radius=8,
                 default_text="Select options ▼",
                 **kwargs):
        super().__init__(master, width=width, fg_color=fg_color, corner_radius=corner_radius, **kwargs)

        self.options = options
        self.width = width
        self.dropdown_height = dropdown_height
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

        self.selected_indices = set()

        self.configure(border_width=1, border_color=self.border_color)
        self.selected_text_var = tk.StringVar(value=self.default_text)

        # Main button showing selected summary
        self.main_button = ctk.CTkButton(
            self,
            textvariable=self.selected_text_var,
            font=self.font,
            fg_color=self.fg_color,
            hover_color=self.hover_color,
            border_width=0,
            corner_radius=self.corner_radius,
            text_color=self.text_color,
            command=self._toggle_menu,
            width=self.width,
            anchor="w",
        )
        self.main_button.pack(fill="x")

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
        outer_frame.pack(padx=6, pady=6)

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

        self.option_frames = []
        self.option_labels = []

        for i, option in enumerate(self.options):
            row_frame = tk.Frame(self.inner_frame, bg=self.fg_color, width=self.width, height=30)
            row_frame.pack(fill="x", anchor="w")
            row_frame.pack_propagate(False)

            label = tk.Label(
                row_frame,
                text=option,
                font=self.dropdown_font,
                bg=self.fg_color,
                fg=self.text_color,
                anchor="w",
                justify="left",
                width=25,
                wraplength=self.width - 20,
            )
            label.pack(side="left", fill="x", expand=True)

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

        self.popup.bind("<FocusOut>", lambda e: self._hide_menu())

    def _update_option_visual(self, idx):
        selected = idx in self.selected_indices
        frame = self.option_frames[idx]
        label = self.option_labels[idx]

        if selected:
            frame.configure(bg=self.selected_bg_color)
            label.configure(fg=self.selected_text_color, bg=self.selected_bg_color)
        else:
            frame.configure(bg=self.fg_color)
            label.configure(fg=self.text_color, bg=self.fg_color)

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

    def _toggle_menu(self):
        if self.is_menu_open:
            self._hide_menu()
        else:
            self._show_menu()

    def _show_menu(self):
        x = self.winfo_rootx()
        y = self.winfo_rooty() + self.winfo_height()
        self.popup.geometry(f"{self.width + 20}x{self.dropdown_height + 12}+{x}+{y}")
        self.popup.deiconify()
        self.popup.focus_set()
        self.is_menu_open = True

    def _hide_menu(self):
        self.popup.withdraw()
        self.is_menu_open = False

    def _on_select(self):
        count = len(self.selected_indices)
        if count == 0:
            self.selected_text_var.set(self.default_text)
        else:
            self.selected_text_var.set(f"{count} selected...")

    def get_selected(self):
        return [self.options[i] for i in sorted(self.selected_indices)]
