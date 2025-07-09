# dictionary_list.py

import tkinter as tk
import customtkinter as ctk
from dataclasses import dataclass
from typing import List, Union, Tuple

@dataclass
class Entry:
    term: str
    definition: str
    tags: str  # space-separated tags

class DictionaryList(ctk.CTkFrame):
    def __init__(self, master=None,
                 width: int = 1920,
                 height: int = 500,
                 row_height: int = 100,
                 term_font_size: int = 36,
                 definition_font_size: int = 20,
                 tag_font_size: int = 30,
                 padx: int = 0,
                 pady: Union[int, Tuple[int,int]] = (10, 0),
                 header_bg_color: str = "#F2FFDD",
                 header_text_color: str = "#658657",
                 row_bg_color_1: str = "#D4EAC7",
                 row_bg_color_2: str = "#E2F6D5",
                 main_text_color: str = "black",
                 checkbox_color: str = "#86AA77",
                 tag_box_bg_color: str = "#F2FFDD",
                 tag_text_color: str = "#658657",
                 scroll_speed: int = 2,
                 **kwargs):
        self.external_padx = padx
        self.external_pady = pady

        super().__init__(master, width=width, height=height, fg_color=header_bg_color, **kwargs)

        self.width = width
        self.height = height
        self.row_height = row_height
        self.term_font_size = term_font_size
        self.definition_font_size = definition_font_size
        self.tag_font_size = tag_font_size

        self.header_bg_color = header_bg_color
        self.header_text_color = header_text_color
        self.row_bg_colors = [row_bg_color_1, row_bg_color_2]
        self.main_text_color = main_text_color
        self.checkbox_color = checkbox_color
        self.tag_box_bg_color = tag_box_bg_color
        self.tag_text_color = tag_text_color

        self.scroll_speed = scroll_speed

        self.entries = []
        self.selected_vars = []

        self.font_term = ctk.CTkFont(family="League Spartan", size=self.term_font_size)
        self.font_definition = ctk.CTkFont(family="League Spartan", size=self.definition_font_size)
        self.font_tag = ctk.CTkFont(family="League Spartan", size=self.tag_font_size)
        self.header_font = ctk.CTkFont(family="League Spartan", size=28)

        self.checkbox_width = 40
        self.term_width = 450
        self.definition_width = 390
        self.tags_width = self.width - (self.checkbox_width + self.term_width + self.definition_width + 40)

        self._setup_widgets()
        self.pack_propagate(False)
        self.pack(padx=0, pady=self.external_pady, fill="both", expand=True)

    def _setup_widgets(self):
        self.header_frame = ctk.CTkFrame(self, fg_color=self.header_bg_color, height=self.row_height)
        self.header_frame.pack(fill="x", side="top", padx=0, pady=0)

        self.header_checkbox = ctk.CTkLabel(self.header_frame, text="", width=self.checkbox_width, fg_color=self.header_bg_color)
        self.header_checkbox.pack(side="left", padx=(10, 0), pady=0)

        self.header_term = ctk.CTkLabel(self.header_frame, text="Term", font=self.header_font, width=self.term_width,
                                        anchor="w", fg_color=self.header_bg_color, text_color=self.header_text_color)
        self.header_term.pack(side="left", padx=(10, 0), pady=0)

        self.header_definition = ctk.CTkLabel(self.header_frame, text="Definition", font=self.header_font, width=self.definition_width,
                                              anchor="w", fg_color=self.header_bg_color, text_color=self.header_text_color)
        self.header_definition.pack(side="left", padx=(10, 0), pady=0)

        self.header_tags = ctk.CTkLabel(self.header_frame, text="Tags", font=self.header_font, width=self.tags_width,
                                        anchor="w", fg_color=self.header_bg_color, text_color=self.header_text_color)
        self.header_tags.pack(side="left", padx=(10, 10), pady=0)

        self.canvas_frame = ctk.CTkFrame(self, fg_color=self.header_bg_color)
        self.canvas_frame.pack(fill="both", expand=True, padx=0, pady=(0, 10))

        self.canvas = tk.Canvas(self.canvas_frame, bg=self.header_bg_color, highlightthickness=0,
                                width=self.width, height=self.height - self.row_height)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar = ctk.CTkScrollbar(self.canvas_frame, orientation="vertical", command=self._on_scroll)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.rows_frame = ctk.CTkFrame(self.canvas, fg_color=self.header_bg_color)
        self.rows_frame.bind("<Configure>", self._on_frame_configure)

        self.canvas_window = self.canvas.create_window((0, 0), window=self.rows_frame, anchor="nw")

        self.rows_frame.bind("<Enter>", lambda e: self._bind_mousewheel())
        self.rows_frame.bind("<Leave>", lambda e: self._unbind_mousewheel())

    def _bind_mousewheel(self):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mousewheel(self):
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        delta = -event.delta * self.scroll_speed / 120  # Keep it float
        self.canvas.yview_scroll(int(delta), "units")

    def _on_scroll(self, *args):
        self.canvas.yview(*args)

    def _on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.itemconfig(self.canvas_window, width=self.width)

    def populate(self, entries: List[Entry]):
        for widget in self.rows_frame.winfo_children():
            widget.destroy()
        self.selected_vars.clear()
        self.entries = entries

        for idx, entry in enumerate(entries, start=1):
            self._create_row(idx, entry)

    def _create_row(self, row_num: int, entry: Entry):
        bg_color = self.row_bg_colors[(row_num - 1) % 2]

        row_frame = ctk.CTkFrame(self.rows_frame, fg_color=bg_color, height=self.row_height, corner_radius=0)
        row_frame.pack(fill="x", pady=0)
        row_frame.pack_propagate(False)

        selected_var = tk.IntVar(value=0)
        self.selected_vars.append(selected_var)

        # Create a frame to represent the entire checkbox column area
        checkbox_column_frame = ctk.CTkFrame(row_frame, width=self.checkbox_width, height=self.row_height, fg_color=bg_color)
        checkbox_column_frame.pack_propagate(False)
        checkbox_column_frame.pack(side="left", padx=(10, 0), pady=0)

        # Checkbox inside the checkbox column frame, centered vertically and horizontally
        checkbox = ctk.CTkCheckBox(checkbox_column_frame, variable=selected_var, width=20, height=20, text="", border_color=self.checkbox_color)
        checkbox.place(relx=0.5, rely=0.5, anchor="center")

        # Bind click on entire checkbox column area to toggle the checkbox
        def toggle_checkbox(event):
            selected_var.set(0 if selected_var.get() else 1)
            return "break"

        checkbox_column_frame.bind("<Button-1>", toggle_checkbox)
        # Also bind click on checkbox itself (to avoid interference)
        checkbox.bind("<Button-1>", lambda e: None)  # allow default checkbox toggle behavior

        # Rest of the columns

        term_label = ctk.CTkLabel(
            row_frame,
            text=self._truncate_text(entry.term, max_chars=25),
            font=self.font_term,
            width=self.term_width,
            fg_color=bg_color,
            text_color=self.main_text_color,
            anchor="w"
        )
        term_label.pack(side="left", padx=(10, 0), pady=(0,5))

        max_chars_per_line = len("Process used by plants and other organisms to")
        max_lines = 3
        lines = self._truncate_multiline_text(entry.definition, max_chars_per_line, max_lines).split("\n")

        definition_frame = ctk.CTkFrame(row_frame, fg_color=bg_color, width=self.definition_width, height=self.row_height)
        definition_frame.pack_propagate(False)
        definition_frame.pack(side="left", padx=(10, 0), pady=0)

        for line in lines:
            label = ctk.CTkLabel(
                definition_frame,
                text=line,
                font=self.font_definition,
                fg_color=bg_color,
                text_color=self.main_text_color,
                anchor="w"
            )
            label.pack(anchor="w", pady=0)

        tags_frame = ctk.CTkFrame(row_frame, fg_color=bg_color, height=self.row_height, width=self.tags_width)
        tags_frame.pack_propagate(False)
        tags_frame.pack(side="left", padx=(10, 10), pady=0)

        tags_list = entry.tags.split()
        self._render_tags(tags_frame, tags_list)


        def on_row_hover(event):
            print(f"Row {row_num} hovered")

        def on_row_click(event):
            print(f"Row {row_num} clicked")

        def bind_click_recursive(widget):
            for child in widget.winfo_children():
                if isinstance(child, ctk.CTkCheckBox):
                    continue
                child.bind("<Button-1>", on_row_click)
                bind_click_recursive(child)

        row_frame.bind("<Button-1>", on_row_click)
        bind_click_recursive(row_frame)

    def _truncate_text(self, text: str, max_chars: int) -> str:
        if len(text) <= max_chars:
            return text
        return text[:max_chars-3] + "..."

    def _truncate_multiline_text(self, text: str, max_chars_per_line: int, max_lines: int) -> str:
        lines = []
        words = text.split()
        current_line = ""
        for word in words:
            if len(current_line + " " + word) <= max_chars_per_line:
                if current_line:
                    current_line += " " + word
                else:
                    current_line = word
            else:
                lines.append(current_line)
                current_line = word
                if len(lines) == max_lines:
                    break
        if len(lines) < max_lines and current_line:
            lines.append(current_line)
        if len(lines) > max_lines:
            lines = lines[:max_lines]

        total_length = sum(len(line) for line in lines)
        if total_length < len(text):
            if len(lines[-1]) > 3:
                lines[-1] = lines[-1][:-3] + "..."
            else:
                lines[-1] += "..."

        return "\n".join(lines)

    def _render_tags(self, container: ctk.CTkFrame, tags_list: List[str]):
        for w in container.winfo_children():
            w.destroy()

        available_width = self.tags_width - 20
        avg_char_width = self.tag_font_size * 0.6

        used_width = 0
        rendered_tags = 0
        tag_widths = [len(t) * avg_char_width + 16 for t in tags_list]

        for i, (tag, width) in enumerate(zip(tags_list, tag_widths)):
            if used_width + width > available_width:
                if used_width + 50 <= available_width:
                    self._create_tag_box(container, "[...]", is_overflow=True)
                break
            self._create_tag_box(container, tag)
            used_width += width + 8
            rendered_tags += 1

        if rendered_tags == 0 and tags_list:
            self._create_tag_box(container, "[...]", is_overflow=True)

    def _create_tag_box(self, container: ctk.CTkFrame, text: str, is_overflow=False):
        tag_frame = ctk.CTkFrame(container, fg_color=self.tag_box_bg_color,
                                corner_radius=12)
        tag_frame.pack(side="left", padx=(0, 8), pady=(self.row_height - self.tag_font_size - 16)//2)

        tag_label = ctk.CTkLabel(tag_frame, text=text,
                                font=self.font_tag,
                                fg_color=self.tag_box_bg_color,
                                text_color=self.tag_text_color,
                                anchor="center")
        tag_label.pack(pady=(0, 6), padx=8)  # Asymmetric vertical padding on label

        if is_overflow:
            tag_label.configure(text_color="#999999")
