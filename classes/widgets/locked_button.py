"""
File: classes/widgets/locked_button.py

Purpose:
    Defines the LockedButton custom widget for the Lexes app. This widget provides a toggleable button
    that can be locked (disabled) or unlocked (enabled) with distinct appearance for each state.
    Useful for actions that should only be available after certain conditions are met.

Contains:
    - LockedButton class: A CTkFrame-based widget containing a CTkButton whose enabled/disabled state and appearance are managed.
    - Methods for locking/unlocking the button, setting its command callback, and handling clicks.

Naming Conventions:
    - Class names: PascalCase (LockedButton)
    - Public method names: snake_case (unlock, lock, set_command)
    - Private method names: snake_case, prefixed with an underscore (_on_click)
    - Attributes: snake_case (button, _is_locked, _command, _neutral_icon, _active_icon)
    - General code: snake_case. NOTE: Custom widgets use snake_case while the rest of the codebase uses camelCase.

Usage:
    Use LockedButton to provide a button with a visually distinct locked (disabled) and unlocked (enabled) state.
    Commonly used to gate actions until certain prerequisites are met.
    LockedButton used in Delete Selected button in Main Window.
"""

#### Module Imports ###
import customtkinter as ctk

class LockedButton(ctk.CTkFrame):
    def __init__(self, master, *,
                 neutral_icon,
                 active_icon,
                 icon_size=(47, 49),
                 width=60,
                 height=60,
                 corner_radius=5,
                 anchor='center',
                 fg_color_neutral="gray",
                 fg_color_active="red",
                 hover_color_active="tomato",
                 text="",
                 command=None,
                 **kwargs):
        """
        Initialise the LockedButton widget with custom icons, styles, and command.
        """
        super().__init__(master, width=width, height=height, fg_color="transparent", **kwargs)
        self.pack_propagate(False)

        self._command = command
        self._is_locked = True

        ### Assets and Styling ###
        self._neutral_icon = ctk.CTkImage(light_image=neutral_icon, dark_image=neutral_icon, size=icon_size)
        self._active_icon = ctk.CTkImage(light_image=active_icon, dark_image=active_icon, size=icon_size)
        self._fg_color_neutral = fg_color_neutral
        self._fg_color_active = fg_color_active
        self._hover_color_active = hover_color_active

        ### Button Setup ###
        self.button = ctk.CTkButton(self,
                                    width=width,
                                    height=height,
                                    image=self._neutral_icon,
                                    text=text,
                                    corner_radius=corner_radius,
                                    anchor=anchor,
                                    fg_color=self._fg_color_neutral,
                                    hover_color=self._fg_color_neutral,  # no hover when locked
                                    command=self._on_click,
                                    state="disabled") # starts locked
        self.button.pack(fill="both", expand=True)

    def _on_click(self) -> None:
        """
        Private Method
        Handles the button click event. If the button is unlocked, it executes the command.
        """
        if not self._is_locked and self._command:
            self._command()

    def unlock(self) -> None:
        """
        Public Method
        Unlocks (enables) the button, updates its appearance, and allows clicking.
        """
        self._is_locked = False
        self.button.configure(image=self._active_icon,
                              fg_color=self._fg_color_active,
                              hover_color=self._hover_color_active,
                              state="normal")

    def lock(self) -> None:
        """
        Public Method
        Locks (disables) the button, updates its appearance, and prevents clicking.
        """
        self._is_locked = True
        self.button.configure(image=self._neutral_icon,
                              fg_color=self._fg_color_neutral,
                              hover_color=self._fg_color_neutral,
                              state="disabled")

    def set_command(self, command) -> None:
        """
        Public Method
        Sets the callback function to be called when the button is clicked (if unlocked).
        """
        self._command = command