### Locked Button Custom Widget
### Toggleable button which can be disabled or enabled with contrasting appearance by methods.
### Naming Convention: snake_case

import customtkinter as ctk
from PIL import ImageTk

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
        super().__init__(master, width=width, height=height, fg_color="transparent", **kwargs)
        self.pack_propagate(False)

        self._command = command
        self._is_locked = True

        # Assets
        self._neutral_icon = ctk.CTkImage(light_image=neutral_icon, dark_image=neutral_icon, size=icon_size)
        self._active_icon = ctk.CTkImage(light_image=active_icon, dark_image=active_icon, size=icon_size)
        self._fg_color_neutral = fg_color_neutral
        self._fg_color_active = fg_color_active
        self._hover_color_active = hover_color_active

        # Button
        self.button = ctk.CTkButton(
            self,
            width=width,
            height=height,
            image=self._neutral_icon,
            text=text,
            corner_radius=corner_radius,
            anchor=anchor,
            fg_color=self._fg_color_neutral,
            hover_color=self._fg_color_neutral,  # no hover when locked
            command=self._on_click,
            state="disabled"  # starts locked
        )
        self.button.pack(fill="both", expand=True)

    def _on_click(self):
        if not self._is_locked and self._command:
            self._command()

    def unlock(self):
        self._is_locked = False
        self.button.configure(
            image=self._active_icon,
            fg_color=self._fg_color_active,
            hover_color=self._hover_color_active,
            state="normal"
        )

    def lock(self):
        self._is_locked = True
        self.button.configure(
            image=self._neutral_icon,
            fg_color=self._fg_color_neutral,
            hover_color=self._fg_color_neutral,
            state="disabled"
        )

    def set_command(self, command):
        self._command = command
