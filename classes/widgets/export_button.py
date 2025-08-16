"""
File: classes/widgets/export_button.py

Purpose:
    Defines the ExportButton custom widget for the Lexes app, providing a button with toggled/inverted appearance between active and inactive states.
    Used in the Export Window to display the two export options: Anki (.csv) and Database (.db).

Contains:
    - ExportButton class, a CTkFrame-based widget with custom styling, icons, and text for both states.
    - Methods for toggling state, updating appearance, and handling click events.

Naming Conventions:
    - Class names: PascalCase (ExportButton).
    - Public method names: snake_case (get_state, set_state).
    - Private method names: snake_case, prefixed with an underscore (e.g., _on_click, _update_appearance).
    - Attributes: snake_case (border_color, border_width, state_active, callback_command).
    - General code: snake_case. NOTE: Custom widgets use snake_case while the rest of the codebase uses camelCase.

Usage:
    Use ExportButton to provide a visually distinct export button with active/inactive styles and callback support.
    ExportButton used for export buttons (Anki Deck and Lexes DB) in Export Window.
"""

### Module Imports ###
import customtkinter as ctk

class ExportButton(ctk.CTkFrame):
    def __init__(self, master, *,
                 neutral_text: str,
                 active_text: str,
                 width: int = 212,
                 height: int = 65,
                 corner_radius: int = 5,
                 font: tuple = ("League Spartan", 36),
                 image_neutral = None,
                 image_active = None,
                 image_size: tuple = (32, 32),
                 fg_color_neutral: str = "transparent",
                 fg_color_active: str = "transparent",
                 text_color_neutral: str = "transparent",
                 text_color_active: str = "transparent",
                 bg_color: str = "transparent",
                 border_color: str = "transparent",
                 callback_command: callable = None,
                 **kwargs):
        """
        Initalise the ExportButton widget with custom styles, images, and text.
        - master (CTk): The parent widget for the ExportButton. CTk so it can use customTkinter features.
        - neutral_text (str): The text to display when the button is inactive. String as it represents the button label.
        - active_text (str): The text to display when the button is active. String as it represents the button label.
        - width (int): The width of the button. Integer as it represents the pixel width.
        - height (int): The height of the button. Integer as it represents the pixel height.
        - corner_radius (int): The corner radius of the button. Integer as it represents the pixel radius.
        - font (tuple): The font configuration for the button text. Tuple as it represents the font family and size.
        - image_neutral (Image): The image to display when the button is inactive. Image as it represents the button icon.
        - image_active (Image): The image to display when the button is active. Image as it represents the button icon.
        - image_size (tuple): The size of the button images. Tuple as it represents the width and height.
        - fg_color_neutral (str): The foreground color for the button when inactive. String as it represents a color value.
        - fg_color_active (str): The foreground color for the button when active. String as it represents a color value.
        - text_color_neutral (str): The text color for the button when inactive. String as it represents a color value.
        - text_color_active (str): The text color for the button when active. String as it represents a color value.
        - bg_color (str): The background color for the button. String as it represents a color value.
        - border_color (str): The border color for the button. String as it represents a color value.
        - callback_command (callable): The function to call when the button is clicked. Callable as it represents a callback function.
        """
        super().__init__(master, width=width, height=height,
                         corner_radius=corner_radius, fg_color=bg_color, **kwargs)
        self.pack_propagate(False)

        self.border_color = border_color
        self.border_width = 2.5
        self.state_active = False # initial state is inactive
        self.callback_command = callback_command # callback function to execute on click

        ### Store images and config ###
        self.neutral_text = neutral_text
        self.active_text = active_text
        self._image_neutral = ctk.CTkImage(light_image=image_neutral, dark_image=image_neutral, size=image_size) if image_neutral else None
        self._image_active = ctk.CTkImage(light_image=image_active, dark_image=image_active, size=image_size) if image_active else None
        self._fg_color_neutral = fg_color_neutral
        self._fg_color_active = fg_color_active
        self._text_color_neutral = text_color_neutral
        self._text_color_active = text_color_active

        ### Button Frame (clickable area) ###
        self.button_frame = ctk.CTkFrame(self, corner_radius=corner_radius,
                                         fg_color=self._fg_color_neutral, border_color=self.border_color, border_width=self.border_width)
        self.button_frame.pack(fill="both", expand=True)

        ### Icon ###
        self.image_label = ctk.CTkLabel(self.button_frame, text="", image=self._image_neutral,
                                        fg_color="transparent")
        self.image_label.pack(side="left", padx=10)

        ### Text ###
        self.text_label = ctk.CTkLabel(self.button_frame, text=self.neutral_text, font=font,
                                       text_color=self._text_color_neutral, fg_color="transparent")
        self.text_label.pack(side="left", padx=0, pady=(4,10))

        ### Bind clicks to all subcomponents recursively ###
        for widget in (self, self.button_frame, self.image_label, self.text_label):
            widget.bind("<Button-1>", self._on_click)

    def _on_click(self, event=None) -> str:
        """
        Private Method

        Handles button click event. Triggers the callback and toggles the button state.
        - event (tk.Event): The click event. Tkinter Event containing information about the click.
        """
        self._toggle_command()
        return "break"

    def toggle(self) -> None:
        """
        Public Method

        Toggles the button state between active and inactive, updating appearance accordingly.
        """
        self.state_active = not self.state_active
        self._update_appearance()
    
    def _toggle_command(self) -> None:
        """
        Private Method

        Executes the callback command with the active text.
        """
        if self.callback_command:
            self.callback_command(self.active_text)

    def _update_appearance(self) -> None:
        """
        Private Method

        Updates the button appearance based on the current state (active/inactive).
        """
        if self.state_active:
            self.button_frame.configure(fg_color=self._fg_color_active)
            self.text_label.configure(text=self.active_text, text_color=self._text_color_active)
            self.image_label.configure(image=self._image_active)
        else:
            self.button_frame.configure(fg_color=self._fg_color_neutral)
            self.text_label.configure(text=self.neutral_text, text_color=self._text_color_neutral)
            self.image_label.configure(image=self._image_neutral)

    def get_state(self) -> bool:
        """
        Public Method

        Returns bool (True if active, False if inactive) indicating the current state of the button.
        """
        return self.state_active

    def set_state(self, active: bool) -> None:
        """
        Public Method

        Sets the button state to active or inactive, updating appearance accordingly.
        - active (bool): Boolean as it represents the target state.
        """
        self.state_active = active
        self._update_appearance()