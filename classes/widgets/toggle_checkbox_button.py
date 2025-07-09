### Toggle Checkbox Button Custom Widget
### Toggleable button which can be disabled or enabled with contrasting appearance by clicking.
### Naming Convention: snake_case

import customtkinter as ctk
from PIL import ImageTk

class ToggleCheckboxButton(ctk.CTkFrame):
    def __init__(self, master, *,
                 neutral_text="Toggle",
                 active_text="Toggle",
                 width=100,
                 height=50,
                 corner_radius=5,
                 font=("League Spartan", 36),

                 image_neutral=None,
                 image_active=None,

                 fg_color_neutral="gray",
                 fg_color_active="green",

                 text_color_neutral="white",
                 text_color_active="white",

                 bg_color="transparent",

                 command=None,
                 **kwargs):
        super().__init__(master, width=width, height=height,
                         corner_radius=corner_radius, fg_color=bg_color, **kwargs)
        self.pack_propagate(False)

        self.state_active = False
        self.command = command

        # Store images and config
        self._image_neutral = ctk.CTkImage(light_image=image_neutral, dark_image=image_neutral, size=(24,24)) if image_neutral else None
        self._image_active = ctk.CTkImage(light_image=image_active, dark_image=image_active, size=(24,24)) if image_active else None
        self._fg_color_neutral = fg_color_neutral
        self._fg_color_active = fg_color_active
        self._text_color_neutral = text_color_neutral
        self._text_color_active = text_color_active
        self.neutral_text = neutral_text
        self.active_text = active_text

        # Button Frame (clickable area)
        self.button_frame = ctk.CTkFrame(self, corner_radius=corner_radius,
                                         fg_color=self._fg_color_neutral)
        self.button_frame.pack(fill="both", expand=True)

        # Icon
        self.image_label = ctk.CTkLabel(self.button_frame, text="", image=self._image_neutral,
                                        fg_color="transparent")
        self.image_label.pack(side="left", padx=13)

        # Text
        self.text_label = ctk.CTkLabel(self.button_frame, text=self.neutral_text, font=font,
                                       text_color=self._text_color_neutral, fg_color="transparent")
        self.text_label.pack(side="left", padx=(9,0), pady=(4,10))

        # Bind clicks to all subcomponents
        for widget in (self, self.button_frame, self.image_label, self.text_label):
            widget.bind("<Button-1>", self._on_click)

    def _on_click(self, event=None):
        self.toggle()
        return "break"

    def toggle(self):
        self.state_active = not self.state_active
        self._update_appearance()
        if self.command:
            self.command()

    def _update_appearance(self):
        if self.state_active:
            self.button_frame.configure(fg_color=self._fg_color_active)
            self.text_label.configure(text=self.active_text, text_color=self._text_color_active)
            self.image_label.configure(image=self._image_active)
        else:
            self.button_frame.configure(fg_color=self._fg_color_neutral)
            self.text_label.configure(text=self.neutral_text, text_color=self._text_color_neutral)
            self.image_label.configure(image=self._image_neutral)

    def get_state(self):
        return self.state_active

    def set_state(self, active: bool):
        self.state_active = active
        self._update_appearance()
