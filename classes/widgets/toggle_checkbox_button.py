"""
File: classes/widgets/toggle_checkbox_button.py

Purpose:
    Defines the ToggleCheckboxButton custom widget for the Lexes app. This widget provides a toggleable button
    with a contrasting appearance for enabled/disabled states, using icons and text. The button can be toggled
    by clicking, and can trigger a callback.

Contains:
    - ToggleCheckboxButton class: A CTkFrame-based widget with a clickable icon and label, toggling between active/neutral states.
    - Methods for click handling, toggling state, updating appearance, and retrieving/setting state.

Naming Conventions:
    - Class names: PascalCase (ToggleCheckboxButton)
    - Public method names: snake_case (get_state, set_state)
    - Private method names: snake_case, prefixed with an underscore (e.g., _on_click, _update_appearance, _toggle)
    - Attributes: snake_case (state_active, button_frame, text_label, etc.)
    - General code: snake_case. Custom widgets use snake_case for consistency.

Usage:
    Use ToggleCheckboxButton for toggleable controls with visually distinct active/inactive states and optional callback.
    ToggleCheckboxButton used for 'Select All' button on Main Window.
"""

### Module Imports ###
import customtkinter as ctk

class ToggleCheckboxButton(ctk.CTkFrame):
    def __init__(self, master, *,
                 neutral_text: str = "Toggle",
                 active_text: str = "Toggle",
                 width: int = 100,
                 height: int = 50,
                 corner_radius: int = 5,
                 font: tuple = ("League Spartan", 36),
                 image_neutral = None,
                 image_active = None,
                 fg_color_neutral: str = "gray",
                 fg_color_active: str = "green",
                 text_color_neutral: str = "white",
                 text_color_active: str = "white",
                 bg_color: str = "transparent",
                 command: callable = None,
                 **kwargs):
        """
        Initialise the ToggleCheckboxButton widget with styling, icons, state, and callback.
        - master (CTk): The parent widget for the ToggleCheckboxButton. CTk so it can use customTkinter features.
        - neutral_text (str): The text to display when the button is in the neutral state. String as it represents the label text.
        - active_text (str): The text to display when the button is in the active state. String as it represents the label text.
        - width (int): The width of the button. Integer as it represents the width in pixels.
        - height (int): The height of the button. Integer as it represents the height in pixels.
        - corner_radius (int): The corner radius of the button. Integer as it represents the radius in pixels.
        - font (tuple): The font to use for the button text. Tuple as it represents the font family and size.
        - image_neutral (Image): The image to display when the button is in the neutral state. Image as it represents the icon displayed.
        - image_active (Image): The image to display when the button is in the active state. Image as it represents the icon displayed.
        - fg_color_neutral (str): The foreground color of the button in the neutral state. String as it represents a color value.
        - fg_color_active (str): The foreground color of the button in the active state. String as it represents a color value.
        - text_color_neutral (str): The text color of the button in the neutral state. String as it represents a color value.
        - text_color_active (str): The text color of the button in the active state. String as it represents a color value.
        - bg_color (str): The background color of the button. String as it represents a color value.
        - command (callable): A callback function to be called when the button is clicked. Callable as it represents a callback function.
        """
        super().__init__(master, width=width, height=height,
                         corner_radius=corner_radius, fg_color=bg_color, **kwargs)
        self.pack_propagate(False)

        ### State & Callback ###
        self.state_active = False
        self.command = command

        ### Styling ###
        self._image_neutral = ctk.CTkImage(light_image=image_neutral, dark_image=image_neutral, size=(24,24)) if image_neutral else None
        self._image_active = ctk.CTkImage(light_image=image_active, dark_image=image_active, size=(24,24)) if image_active else None
        self._fg_color_neutral = fg_color_neutral
        self._fg_color_active = fg_color_active
        self._text_color_neutral = text_color_neutral
        self._text_color_active = text_color_active
        self.neutral_text = neutral_text
        self.active_text = active_text

        # Button Frame (Clickable Area) ###
        self.button_frame = ctk.CTkFrame(self, corner_radius=corner_radius,
                                         fg_color=self._fg_color_neutral)
        self.button_frame.pack(fill="both", expand=True)

        ### Icon ###
        self.image_label = ctk.CTkLabel(self.button_frame, text="", image=self._image_neutral,
                                        fg_color="transparent")
        self.image_label.pack(side="left", padx=13)

        ### Text ###
        self.text_label = ctk.CTkLabel(self.button_frame, text=self.neutral_text, font=font,
                                       text_color=self._text_color_neutral, fg_color="transparent")
        self.text_label.pack(side="left", padx=(9,0), pady=(4,10))

        ### Bind Click Events ###
        for widget in (self, self.button_frame, self.image_label, self.text_label):
            widget.bind("<Button-1>", self._on_click)

    def _on_click(self, event=None) -> str:
        """
        Private Method

        Handles click events, toggles state and prevents propagation.
        - event (tk.Event): The event object associated with the click. Tkinter Event so it can be used to identify the widget that triggered the click event.
        """
        self._toggle()
        return "break"

    def _toggle(self) -> None:
        """
        Private Method

        Toggles the button state (active/neutral), updates appearance, and triggers callback if set.
        """
        self.state_active = not self.state_active
        self._update_appearance()
        if self.command:
            self.command()

    def _update_appearance(self) -> None:
        """
        Private Method

        Updates the visual appearance (background, text, icon) based on current state.
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

        Returns the current active state of the button (True for active, False for neutral).
        """
        return self.state_active

    def set_state(self, active: bool) -> None:
        """
        Public Method

        Sets the button to active or neutral state and updates appearance.
        - active (bool): The desired active state of the button. Boolean as it represents the state (True for active, False for neutral).
        """
        self.state_active = active
        self._update_appearance()