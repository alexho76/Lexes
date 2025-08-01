"""
File: classes/widgets/dictionary_list.py

Purpose:
    Defines the DictionaryList widget for displaying and managing a list of dictionary entries within the Lexes app.
    This widget allows for viewing, selecting, and interacting with entries, including tag display, checkbox select, lazy loading, and row click callbacks.
    Handles dynamic row rendering, scrolling, and user selection callbacks.

Contains:
    - DictionaryList class, a CTkFrame-based widget for entry display and selection.
    - Private methods for widget setup, row creation, tag rendering, truncation, and popup/overflow handling.
    - Public methods for populating the list with entries, selecting all entries, unselecting all entries.

Naming Conventions:
    - Class names: PascalCase (DictionaryList).
    - Public method names: snake_case (populate, select_all, unselect_all).
    - Private method names: snake_case, prefixed with an underscore (e.g., _setup_widgets, _create_row).
    - Attributes: snake_case (entries, self.on_selection_change, row_height).
    - General code: snake_case. NOTE: Custom widgets use snake_case while the rest of the codebase uses camelCase.

Usage:
    Use DictionaryList to display a list of dictionary entries with interactive features like selection, tag display, and row click handling
    with ability for integration with complex operations like lazy loading and dynamic row rendering, and search/sort/filter.
    DictionaryList used for dictionary list display in Main Window.
"""

### Module Imports ###
import tkinter as tk
import customtkinter as ctk

### Local Class Imports ###
from classes.entry import Entry
from classes.selected_list import SelectedList
from classes.display_list import DisplayList

class DictionaryList(ctk.CTkFrame):
    
    def __init__(self, master=None,
                 entries: list[Entry] = [],
                 selectedList: SelectedList = None,
                 width: int = 1920,
                 height: int = 644,
                 row_height: int = 100,
                 term_font_size: int = 36,
                 definition_font_size: int = 20,
                 tag_font_size: int = 30,
                 header_bg_color: str = "#F2FFDD",
                 header_text_color: str = "#658657",
                 row_bg_color_1: str = "#D4EAC7",
                 row_bg_color_2: str = "#E2F6D5",
                 selected_row_color_1: str = "#DFFEE2",
                 selected_row_color_2: str = "#DCF4DE",
                 divider_color: str = "86AA77",
                 main_text_color: str = "black",
                 checkbox_color: str = "#86AA77",
                 tag_box_bg_color: str = "#F2FFDD",
                 tag_text_color: str = "#658657",
                 scroll_speed: int = 2,
                 overflow_icon: str = None,
                 select_icon: str = None,
                 term_icon: str = None,
                 definition_icon: str = None,
                 tag_icon: str = None,
                 on_selection_change = None,
                 on_row_click = None,
                 empty_message: ctk.CTkLabel = None,
                 **kwargs):
        """
        Initialise the DictionaryList frame and UI config.
            - Sets up fonts, colors, icons, dimensions, and other UI elements.
            - Builds all widgets and binds events.
            - Populates the list with entries on start.
        """
        super().__init__(master, width=width, height=height+1.5, fg_color=header_bg_color, corner_radius=0, **kwargs)
        super().pack_propagate(False)
        self.on_selection_change = on_selection_change
        self.on_row_click = on_row_click

        ### Entry and SelectedList setup ###
        self.entries = entries
        self.selectedList = selectedList if selectedList is not None else SelectedList()

        ## Layout, Font, Dimensions, and Colour setup ###
        self.width = width
        self.height = height
        self.row_height = row_height
        self.term_font_size = term_font_size
        self.definition_font_size = definition_font_size
        self.tag_font_size = tag_font_size

        self.header_bg_color = header_bg_color
        self.header_text_color = header_text_color
        self.row_bg_color_1 = row_bg_color_1
        self.row_bg_color_2 = row_bg_color_2
        self.selected_row_color_1 = selected_row_color_1
        self.selected_row_color_2 = selected_row_color_2
        self.divider_color = divider_color
        self.row_bg_colors = [self.row_bg_color_1, self.row_bg_color_2]
        self.main_text_color = main_text_color
        self.checkbox_color = checkbox_color
        self.tag_box_bg_color = tag_box_bg_color
        self.tag_text_color = tag_text_color

        self.scroll_speed = scroll_speed
        self.empty_message = empty_message

        ### Icon Images ###
        self.overflow_icon = ctk.CTkImage(light_image=overflow_icon, dark_image=overflow_icon, size=(34,9))
        self.select_icon = ctk.CTkImage(light_image=select_icon, dark_image=select_icon, size=(31,31))
        self.term_icon = ctk.CTkImage(light_image=term_icon, dark_image=term_icon, size=(33,19))
        self.definition_icon = ctk.CTkImage(light_image=definition_icon, dark_image=definition_icon, size=(26,28))
        self.tag_icon = ctk.CTkImage(light_image=tag_icon, dark_image=tag_icon, size=(28,28))

        ### Internal Tracking Variables ###
        self.selected_vars = {}
        self.visible_rows = {}

        ### Font Setup ###
        self.font_term = ctk.CTkFont(family="League Spartan", size=self.term_font_size)
        self.font_definition = ctk.CTkFont(family="Bahnschrift", size=self.definition_font_size)
        self.font_tag = ctk.CTkFont(family="League Spartan", size=self.tag_font_size)
        self.header_font = ctk.CTkFont(family="League Spartan", size=28)

        ### Column Widths ###
        self.checkbox_width = 45
        self.term_width = 558
        self.definition_width = 552
        self.tags_width = 765

        # Widget Setup ###
        self._setup_widgets()
        self._bind_mousewheel_all()
        self.pack_propagate(False)
        self.populate()

        ### Bind Events ###
        self.canvas.bind("<Configure>", self._on_canvas_resize)


    def _bind_mousewheel_all(self) -> None:
        """
        Private Method
        Binds mousewheel events to the canvas and all children widgets for scrolling.
        Uses the root window (toplevel) for global event binding.
        """
        toplevel = self.winfo_toplevel()
        self.bind("<Enter>", lambda e: toplevel.bind_all("<MouseWheel>", self._on_mousewheel))
        self.bind("<Leave>", lambda e: toplevel.unbind_all("<MouseWheel>"))
        for child in self.winfo_children():
            child.bind("<Enter>", lambda e: toplevel.bind_all("<MouseWheel>", self._on_mousewheel))
            child.bind("<Leave>", lambda e: toplevel.unbind_all("<MouseWheel>"))

    def _setup_widgets(self) -> None:
        """
        Private Method
        Build and pack all main UI widgets: header, canvas, scrollbar, and row frame.
        """
        ### Header Row ###
        self.header_frame = ctk.CTkFrame(self, fg_color=self.header_bg_color, height=42, corner_radius=0)
        self.header_frame.pack(fill="x", side="top", padx=0, pady=0)
        self.header_frame.pack_propagate(False)

        self.header_divider = ctk.CTkFrame(self, fg_color=self.divider_color, height=1.5, corner_radius=0)
        self.header_divider.pack(fill="x", side="top", padx=0, pady=0)
        self.header_divider.pack_propagate(False)

        self.checkbox_header = ctk.CTkLabel(self.header_frame, text="", width=self.checkbox_width, fg_color=self.header_bg_color, image=self.select_icon)
        self.checkbox_header.pack(side="left", padx=0, pady=0)
        self.checkbox_term_header_divider = ctk.CTkFrame(self.header_frame, fg_color=self.divider_color, width=1.5)
        self.checkbox_term_header_divider.pack(side="left",padx=0,pady=0,fill="y")

        self.term_header_icon = ctk.CTkLabel(self.header_frame, image=self.term_icon, text="")
        self.term_header_icon.pack(side="left", padx=(10,8), pady=(5,0))
        self.term_header = ctk.CTkLabel(self.header_frame, text="Term", font=self.header_font, width=self.term_width - self.term_icon._size[0],
                                        anchor="w", fg_color=self.header_bg_color, text_color=self.header_text_color)
        self.term_header.pack(side="left", padx=0, pady=(0,4))

        self.definition_header_icon = ctk.CTkLabel(self.header_frame, image=self.definition_icon, text="")
        self.definition_header_icon.pack(side="left", padx=(13,8), pady=(5,0))
        self.definition_header = ctk.CTkLabel(self.header_frame, text="Definition", font=self.header_font, width=self.definition_width - self.definition_icon._size[0],
                                              anchor="w", fg_color=self.header_bg_color, text_color=self.header_text_color)
        self.definition_header.pack(side="left", padx=0, pady=(0,4))

        self.tags_header_icon = ctk.CTkLabel(self.header_frame, image=self.tag_icon, text="")
        self.tags_header_icon.pack(side="left", padx=(10,8), pady=(5,0))
        self.tags_header = ctk.CTkLabel(self.header_frame, text="Tags", font=self.header_font, width=self.tags_width,
                                        anchor="w", fg_color=self.header_bg_color, text_color=self.header_text_color)
        self.tags_header.pack(side="left", padx=(0,0), pady=(0,4))

        ### Main Canvas and Scrollbar ###
        self.canvas_frame = ctk.CTkFrame(self, fg_color=self.header_bg_color,corner_radius=0)
        self.canvas_frame.pack(fill="both", expand=True, padx=0, pady=(0,0))

        self.canvas = tk.Canvas(self.canvas_frame, bg=self.header_bg_color, highlightthickness=0,
                                height=self.height - self.row_height)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar = ctk.CTkScrollbar(self.canvas_frame, orientation="vertical", command=self._on_scroll, corner_radius=50, bg_color="#C6E1B8",
                                          fg_color='transparent', button_color=self.tag_text_color, button_hover_color="#719662")
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        ### Rows Frame inside Canvas ###
        self.rows_frame = ctk.CTkFrame(self.canvas, fg_color=self.header_bg_color, corner_radius=0)
        self.rows_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.rows_frame, anchor="nw")

        ### Mousewheel binding for scrolling in Canvas ###
        self.canvas.bind("<Enter>", lambda e: self.canvas.bind_all("<MouseWheel>", self._on_mousewheel))
        self.canvas.bind("<Leave>", lambda e: self.canvas.unbind_all("<MouseWheel>"))

    def _on_mousewheel(self, event) -> None:
        """
        Private Method
        Handles mouse wheel scrolling event for the canvas. Destroys popups if open so that popups close upon scroll.
        """
        direction = -1 if event.delta > 0 else 1
        scroll_units = int(direction * self.scroll_speed)
        if scroll_units == 0:
            scroll_units = direction
        self.canvas.yview_scroll(scroll_units, "units")
        self._update_visible_rows()

        # Remove popup if open
        if hasattr(self, "popup") and self.popup.winfo_exists():
            self._safe_destroy_popup()

    def _on_scroll(self, *args) -> None:
        """
        Private Method
        Handles manual scrollbar scrolling event for the canvas.
        """
        self.canvas.yview(*args)
        self._update_visible_rows()

    def _on_frame_configure(self, event) -> None:
        """
        Private Method
        Updates scroll region of the canvas to encompass the entire rows frame when it is resized (new rows added).
        """
        total_height = len(self.entries) * self.row_height

        self.canvas.update_idletasks()
        frame_height = max(total_height, self.canvas.winfo_height())
        self.canvas.configure(scrollregion=(0, 0, self.width, frame_height))

        self._update_visible_rows()
    
    def _on_canvas_resize(self, event) -> None:
        """
        Private Method
        Updates the visible rows when the canvas is resized by the user.
        """
        self._update_visible_rows()

    def _update_visible_rows(self) -> None:
        """
        Private Method
        Lazy-loads visible rows only in canvas viewport, destroying rows that leave the frame of view and creating new ones for those that come into view.
        """
        y0 = self.canvas.canvasy(0)
        y1 = y0 + self.canvas.winfo_height()
        first_row = max(0, int(y0 // self.row_height))
        last_row = min(len(self.entries), int(y1 // self.row_height) + 1)

        # Remove rows not visible
        for idx in list(self.visible_rows.keys()):
            if idx < first_row or idx >= last_row:
                info = self.visible_rows.pop(idx)
                info['frame'].destroy()
                self.canvas.delete(info['canvas_window_id'])

        # Add newly visible rows
        for idx in range(first_row, last_row):
            if idx not in self.visible_rows:
                entry = self.entries[idx]
                row_frame = self._create_row(idx + 1, entry, visible_mode=True, selected_var=self.selected_vars[idx])
                canvas_window_id = self.canvas.create_window(0, idx * self.row_height,
                                                             window=row_frame,
                                                             anchor="nw",
                                                             width=self.width)
                self.visible_rows[idx] = {'frame': row_frame, 'canvas_window_id': canvas_window_id}

    def _create_row(self, row_num: int, entry: Entry, visible_mode=False, selected_var=None) -> ctk.CTkFrame:
        """
        Private Method
        Creates a single row widget for an entry, including checkbox, term, definition, and tags.
        Handles selection state, click events, and dynamic row colour.
        """
        row_type = (row_num - 1) % 2
        if selected_var is None:
            selected_var = tk.IntVar(value=0)
            if not visible_mode:
                self.selected_vars.append(selected_var)

        # Set initial bg color based on selection state and row type
        is_selected = selected_var.get() == 1
        if is_selected:
            bg_color = self.selected_row_color_1 if row_type == 0 else self.selected_row_color_2
        else:
            bg_color = self.row_bg_colors[row_type]

        # Build the row frame and columns
        row_frame = ctk.CTkFrame(self.canvas, fg_color=bg_color, height=self.row_height, corner_radius=0)
        row_frame.pack_propagate(False)
        if not visible_mode:
            row_frame.pack(fill="x", padx=0)

        checkbox_column_frame = ctk.CTkFrame(row_frame, width=self.checkbox_width, height=self.row_height, fg_color=bg_color, corner_radius=0)
        checkbox_column_frame.pack_propagate(False)
        checkbox_column_frame.pack(side="left", padx=0, pady=0)

        checkbox = ctk.CTkCheckBox(checkbox_column_frame, variable=selected_var, width=25, height=25, text="", border_color=self.checkbox_color,
                                hover_color="#719662", checkmark_color=self.header_bg_color, fg_color=self.checkbox_color, corner_radius=5, border_width=3)
        checkbox.place(relx=0.55, rely=0.5, anchor="center")

        checkbox_term_divider = ctk.CTkFrame(row_frame, fg_color=self.divider_color, width=1.5)
        checkbox_term_divider.pack(side="left", padx=0, pady=0, fill="y")

        # Term Column (truncated)
        term_label = ctk.CTkLabel(row_frame,
                                  text=self._truncate_text(entry.term, self.term_width, self.font_term),
                                  font=self.font_term,
                                  width=self.term_width,
                                  fg_color=bg_color,
                                  text_color=self.main_text_color,
                                  anchor="w")
        term_label.pack(side="left", padx=10, pady=(0, 7))

        # Definition column (multi-line truncation)
        lines = self._truncate_multiline_text(entry.definition, self.definition_width, self.font_definition, 3).split("\n")
        definition_frame = ctk.CTkFrame(row_frame, fg_color=bg_color, width=self.definition_width, height=self.row_height, corner_radius=0)
        definition_frame.pack_propagate(False)
        definition_frame.pack(side="left", padx=10, pady=5)

        ctkLines = []
        for line in lines:
            label = ctk.CTkLabel(definition_frame,
                                 text=line,
                                 font=("Bahnschrift", 24),
                                 fg_color=bg_color,
                                 text_color=self.main_text_color,
                                 anchor="w")
            label.pack(anchor="w", pady=0)
            ctkLines.append(label)

        # Tags Column
        tags_frame = ctk.CTkFrame(row_frame, fg_color=bg_color, height=self.row_height, width=self.tags_width, corner_radius=5)
        tags_frame.pack_propagate(False)
        tags_frame.pack(side="left", padx=(10, 0), pady=0)

        tags_list = entry.tags.split()
        self._render_tags(tags_frame, tags_list)

        def update_row_colors():
            """
            Updates colors for all background widgets in a row when selection is toggled (based on row type).
            """
            selected = selected_var.get() == 1

            if selected:
                new_bg = self.selected_row_color_1 if row_type == 0 else self.selected_row_color_2
            else:
                new_bg = self.row_bg_colors[row_type]

            widgets_to_update = [row_frame, checkbox_column_frame, term_label, definition_frame, tags_frame, *ctkLines] # include all widgets in the row and unpacks ctkLines

            for widget in widgets_to_update:
                try:
                    if widget and widget.winfo_exists():
                        widget.configure(fg_color=new_bg)
                except Exception as e:
                    print(f"[WARN] Failed to update color for widget: {e}")

        def on_checkbox_toggle(*args):
            """
            Called when the checkbox is toggled. Updates selection state and triggers callbacks.
            """
            is_selected = selected_var.get() == 1
            if is_selected:
                entry.select(self.selectedList)
            else:
                entry.unselect(self.selectedList)
            
            update_row_colors()

            if self.on_selection_change:
                self.on_selection_change()

        selected_var.trace_add("write", on_checkbox_toggle)


        def toggle_checkbox(event):
            """
            Toggles the checkbox state when the checkbox column is clicked.
            """
            selected_var.set(0 if selected_var.get() else 1)
            return "break"

        # Bind click events to the row and checkbox
        checkbox_column_frame.bind("<Button-1>", toggle_checkbox)
        checkbox.bind("<Button-1>", lambda e: None)  # Prevent checkbox from toggling on click

        def on_row_click(event):
            """
            Handles click events for the row (excluding checkbox).
            Triggers the on_row_click callback, which is later used for displaying the sidebar popup for individual entries.
            """
            if self.on_row_click:
                self.on_row_click(row_num, entry)

        def bind_click_recursive(widget):
            """
            Recursively binds click events to all child widgets in the row frame except checkboxes and buttons.
            """
            for child in widget.winfo_children():
                if isinstance(child, (ctk.CTkCheckBox, ctk.CTkButton)):
                    continue
                child.bind("<Button-1>", on_row_click)
                bind_click_recursive(child)

        row_frame.bind("<Button-1>", on_row_click) # Bind row click to the row frame
        bind_click_recursive(row_frame) # Bind click events to all child widgets

        update_row_colors()
        return row_frame # Return the row frame for future packing into the canvas

    def _truncate_text(self, text: str, max_width_px: int, font) -> str:
        """
        Private Method
        Truncates text with ellipsis if it exceeds the maximum pixel width.
        """
        ellipsis = "..."
        ellipsis_width = font.measure(ellipsis)

        if font.measure(text) <= max_width_px:
            return text

        for i in range(len(text), 0, -1):
            sub_text = text[:i]
            if font.measure(sub_text) + ellipsis_width <= max_width_px:
                return sub_text + ellipsis

        return ellipsis  # fallback if even a single character is too big

    def _truncate_multiline_text(self, text: str, max_width_px: int, font, max_lines: int = 3) -> str:
        """
        Private Method
        Truncates multi-line text to fit within a specified width and maximum number of lines, adding ellipsis if it overflows.
        Handles word splitting for long words that single-handedly exceed the width of a line.
        Returns the truncated text as a single string with newline characters.
        """
        ellipsis = "..."
        ellipsis_w = font.measure(ellipsis)
        lines = []
        current = ""
        words = text.split()
        
        i = 0
        while i < len(words) and len(lines) < max_lines:
            word = words[i]
            last_line = len(lines) + 1 == max_lines
            reserve = ellipsis_w if last_line else 0
            test = (current + " " + word).strip()

            if font.measure(test) + reserve <= max_width_px:
                current = test
                i += 1
            else:
                if not current:
                    # Word alone too long, split it with a hyphen
                    for j in range(len(word), 0, -1):
                        if font.measure(word[:j] + "-" + reserve * " ") <= max_width_px:
                            break_point = j
                            break
                    else:
                        break_point = 1  # just in case

                    lines.append(word[:break_point] + "-")
                    words[i] = word[break_point:]  # push remainder of the word back
                else:
                    lines.append(current)
                    current = ""

        if current:
            if len(lines) < max_lines:
                lines.append(current)
            else:
                last = lines[-1]
                while font.measure(last + ellipsis) > max_width_px and last:
                    last = last[:-1]
                lines[-1] = last + ellipsis

        # Add ellipsis if the entire text wasn't consumed
        if i < len(words):
            last = lines[-1]
            if not last.endswith(ellipsis):
                while font.measure(last + ellipsis) > max_width_px and last:
                    last = last[:-1]
                lines[-1] = last + ellipsis

        return "\n".join(lines)

    def _truncate_tag_text(self, text: str, max_width: int) -> str:
        """
        Private Method
        Truncates tag text with ellipsis if it exceeds the maximum width.
        Used when creating tag boxes to ensure they fit within the available space.
        Returns the truncated text string with ellipsis if necessary.
        """
        ellipsis = "..."
        font = ctk.CTkFont(family="League Spartan", size=16)
        if font.measure(text) <= max_width:
            return text
        for i in range(len(text), 0, -1):
            if font.measure(text[:i] + ellipsis) <= max_width:
                return text[:i] + ellipsis
        return ellipsis

    def _render_tags(self, container: ctk.CTkFrame, tags_list: list[str]) -> None:
        """
        Private Method
        Renders tag boxes into the tag column.
        Uses overflow boxes if tags exceed available width.
        """
        for w in container.winfo_children():
            w.destroy()

        available_width = self.tags_width - 36  # 16px scrollbar + 8px end padding + 8px buffer
        font = self.font_tag

        used_width = 0
        rendered_tags = 0
        tag_measured_widths = []

        for tag in tags_list:
            text_width = font.measure(tag)
            full_width = text_width + (8 * 2) + 8  # label padx=8 both sides + 8px between boxes
            tag_measured_widths.append((tag, full_width))

        unused_tags = []
        overflow_button_total_width = 30 + 8 + 8 + 8  # icon + between tags + right side + buffer
        scrollbar_width = 16

        overflow_created = False

        for i, (tag, width) in enumerate(tag_measured_widths):
            if used_width + width + overflow_button_total_width + scrollbar_width + 5 > available_width:
                unused_tags = tags_list[i:]  # these didn’t fit
                if used_width + overflow_button_total_width + scrollbar_width <= available_width:
                    self._create_overflow_tag_box(container, unused_tags)
                    overflow_created = True
                break
            self._create_tag_box(container, tag)
            used_width += width + 8  # 8px between tag boxes
            rendered_tags += 1

        if rendered_tags == 0 and tags_list and not overflow_created:
            self._create_overflow_tag_box(container, tags_list)


    def _create_tag_box(self, container: ctk.CTkFrame, text: str) -> None:
        """
        Private Method
        Creates a single tag box widget with a label inside.
        """
        tag_frame = ctk.CTkFrame(container, fg_color=self.tag_box_bg_color,
                                corner_radius=5)
        tag_frame.pack(side="left", padx=(0, 8), pady=(self.row_height - self.tag_font_size - 16)//2)
        tag_label = ctk.CTkLabel(tag_frame, text=text,
                                font=self.font_tag,
                                fg_color=self.tag_box_bg_color,
                                text_color=self.tag_text_color,
                                anchor="center")
        tag_label.pack(pady=(0, 6), padx=8)

    def _create_overflow_tag_box(self, container: ctk.CTkFrame, unused_tags: list[str]) -> None:
        """
        Private Method
        Creates an overflow tag box (button) that opens a dropdown with unused tags (tags that didn't fit in the tags column).
        """
        def on_button_click(event=None):
            self._toggle_overflow_popup(tag_button, unused_tags)
            return "break"

        tag_button = ctk.CTkButton(container,
                                   text="",
                                   image = self.overflow_icon,
                                   font=self.font_tag,
                                   fg_color=self.tag_box_bg_color,
                                   text_color=self.tag_text_color,
                                   corner_radius=5,
                                   hover_color="#E6F3D2",
                                   width=30,
                                   height=50)
        tag_button.pack(side="left", padx=0, pady=0)
        tag_button.bind("<Button-1>", on_button_click)

    def _create_overflow_tag_dropdown(self, unused_tags_list) -> None:
        """
        Private Method
        Creates a popup dropdown listing overflow (unused) tags when the overflow button is clicked.
        """
        self._safe_destroy_popup()

        self.popup = tk.Toplevel(self)
        self.popup.overrideredirect(True)
        self.popup.configure(bg=self.tag_box_bg_color)

        outer_frame = tk.Frame(self.popup, bg=self.tag_box_bg_color)
        outer_frame.pack(padx=0, pady=0)

        max_visible_tags = 8
        tag_height = 23
        popup_height = min(len(unused_tags_list), max_visible_tags) * tag_height

        self.popup_canvas = tk.Canvas(outer_frame,
                                      bg=self.tag_box_bg_color,
                                      highlightthickness=0,
                                      width=200,
                                      height=popup_height,
                                      bd=0,
                                      yscrollincrement=tag_height)
        self.popup_canvas.pack(side="left", fill="both", expand=True)

        self.inner_frame = tk.Frame(self.popup_canvas, bg=self.tag_box_bg_color, width=200)
        self.popup_canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        self.inner_frame.bind("<Configure>", lambda e: self.popup_canvas.configure(scrollregion=self.popup_canvas.bbox("all")))

        for tag in unused_tags_list:
            row_frame = tk.Frame(self.inner_frame, bg=self.tag_box_bg_color, width=200, height=tag_height)
            row_frame.pack(fill="x", anchor="w", pady=0)
            row_frame.pack_propagate(False)

            label = ctk.CTkLabel(row_frame,
                                 text=self._truncate_tag_text(tag, 180),
                                 font=("League Spartan", 16),
                                 text_color=self.tag_text_color,
                                 anchor="w",
                                 justify="left",
                                 width=180)
            if self._truncate_tag_text(tag, 180) != tag:
                self._add_tooltip(label, tag)
            label.pack(side="left", fill="x", expand=True, padx=10)

        def on_popup_mousewheel(event):
            """
            Handles mouse wheel scrolling in the popup canvas.
            Allows scrolling through the tag list using the mouse wheel.
            """
            direction = -1 if event.delta > 0 else 1
            self.popup_canvas.yview_scroll(direction, "units")
            return "break"

        # Bind mouse wheel events to the popup canvas
        self.popup_canvas.bind("<Enter>", lambda e: self.popup_canvas.bind_all("<MouseWheel>", on_popup_mousewheel))
        self.popup_canvas.bind("<Leave>", lambda e: self.popup_canvas.unbind_all("<MouseWheel>"))

        # Bind click outside to close the popup
        self._bind_popup_outside_click()

    def _toggle_overflow_popup(self, widget, unused_tags) -> None:
        """
        Private Method
        Toggles the overflow popup.
        Dynamically positions the popup either above or below depending on available space.
        """
        if hasattr(self, "popup") and self.popup.winfo_exists():
            self._safe_destroy_popup()
        else:
            self._create_overflow_tag_dropdown(unused_tags)

            self.update_idletasks()
            widget.update_idletasks()
            self.popup.update_idletasks()

            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()

            # Widget position and size
            widget_x = widget.winfo_rootx()
            widget_y = widget.winfo_rooty()
            widget_width = widget.winfo_width()
            widget_height = widget.winfo_height()

            # Popup size
            popup_width = self.popup.winfo_reqwidth()
            popup_height = self.popup.winfo_reqheight()

            # Try to open down and to the right (default)
            default_x = widget_x
            default_y = widget_y + widget_height

            # Try to open up and to the left (fallback)
            fallback_x = widget_x + widget_width - popup_width
            fallback_y = widget_y - popup_height

            # Check if default position would overflow off screen
            overflows_bottom = default_y + popup_height > screen_height
            overflows_right = default_x + popup_width > screen_width

            if overflows_bottom or overflows_right:
                # Use fallback position (up-left)
                final_x = max(0, fallback_x)
                final_y = max(0, fallback_y)
            else:
                # Use default position (down-right)
                final_x = default_x
                final_y = default_y

            self.popup.geometry(f"+{final_x}+{final_y}")    
            self.popup.deiconify()
            self.popup.lift()

    def _safe_destroy_popup(self) -> None:
        """
        Private Method
        Safely destroys the popup if it exists.
        """
        if hasattr(self, "popup") and self.popup.winfo_exists():
            self.popup.destroy()
        self._unbind_popup_outside_click()

    def _bind_popup_outside_click(self) -> None:
        """
        Private Method
        Binds a click event outside the popup to close it.
        """
        def on_click_outside(event):
            """
            Handles click events outside the popup.
            Destroys the popup if the click is outside its bounds.
            """
            if hasattr(self, "popup") and self.popup.winfo_exists():
                x1 = self.popup.winfo_rootx()
                y1 = self.popup.winfo_rooty()
                x2 = x1 + self.popup.winfo_width()
                y2 = y1 + self.popup.winfo_height()
                if not (x1 <= event.x_root <= x2 and y1 <= event.y_root <= y2):
                    self._safe_destroy_popup()
        self._outside_click_handler = on_click_outside
        self.winfo_toplevel().bind_all("<Button-1>", self._outside_click_handler)

    def _unbind_popup_outside_click(self) -> None:
        """
        Private Method
        Unbinds the click handler for outside the popup dropdown to prevent memory leaks.
        """
        if hasattr(self, "_outside_click_handler"):
            self.winfo_toplevel().unbind_all("<Button-1>")
            del self._outside_click_handler
        
    def _add_tooltip(self, widget, text) -> None:
        """
        Private Method
        Adds a tooltip to a widget that displays additional information when hovered over.
        Used for tag labels in overflow tag box dropdown to show full tag text if truncated even further.
        """
        tooltip = tk.Toplevel(widget)
        tooltip.withdraw()
        tooltip.overrideredirect(True)
        label = tk.Label(tooltip, text=text, bg="#E7F4D3", fg="#658657", padx=6, pady=2)
        label.pack()

        def show_tooltip(event):
            tooltip.geometry(f"+{event.x_root+10}+{event.y_root+10}")
            tooltip.deiconify()

        def hide_tooltip(event):
            tooltip.withdraw()

        widget.bind("<Enter>", show_tooltip)
        widget.bind("<Leave>", hide_tooltip)
    
    ### Public Methods ###
    def populate(self) -> None:
        """
        Public Method
        Populates the dictionary list with entries, destroying any existing rows and creating new ones.
        """
        for idx, info in self.visible_rows.items():
            info['frame'].destroy()
            self.canvas.delete(info['canvas_window_id'])
        self.visible_rows.clear()

        self.selected_vars = {i: tk.IntVar(value=0) for i in range(len(self.entries))}

        self.update_idletasks()
        canvas_height = self.canvas.winfo_height()
        total_height = len(self.entries) * self.row_height
        scrollregion_height = max(canvas_height, total_height)
        self.canvas.configure(scrollregion=(0, 0, self.width, scrollregion_height))

        self._update_visible_rows()

    def select_all(self) -> None:
        """
        Public Method
        Selects all entries in the dictionary list, updating their selection state and their row colours.
        """
        for idx, entry in enumerate(self.entries):
            if entry not in self.selectedList.entries:
                entry.select(self.selectedList)
            self.selected_vars[idx].set(1)
        self._update_visible_rows()

    def unselect_all(self) -> None:
        """
        Public Method
        Unselects all entries in the dictionary list, updating their selection state and their row colours.
        """
        for idx, entry in enumerate(self.entries):
            entry.unselect(self.selectedList)
            self.selected_vars[idx].set(0)
        self._update_visible_rows()

    def display_empty_message(self, entries_exist: bool) -> None:
        """
        Public Method
        Displays a message indicating that the database is empty or has no results meeting the current filters.
        """
        if entries_exist:
            self.empty_message = ctk.CTkLabel(self.canvas, text="No results match the current filters.",
                                              fg_color="transparent", font=self.font_term, text_color=self.row_bg_color_1)
            self.empty_message.place(relx=0.5, rely=0.5, anchor="center")
        else:
            self.empty_message = ctk.CTkLabel(self.canvas, text="Your dictionary is empty. Click 'Add' to create your first entry.",
                                              fg_color="transparent", font=self.font_term, text_color=self.row_bg_color_1)
            self.empty_message.place(relx=0.5, rely=0.5, anchor="center")

    def hide_empty_message(self) -> None:
        """
        Public Method
        Clears the empty message label from the canvas.
        """
        if self.empty_message is not None:
            self.empty_message.destroy()
            self.empty_message = None