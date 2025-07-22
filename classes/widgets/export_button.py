### Export Button Custom Widget
### A button that toggles appearance to have an inverted appearance upon active vs inactive states.
### Naming Convention: snake_case

import customtkinter as ctk
from PIL import ImageTk

class ExportButton(ctk.CTkFrame):
    def __init__(self, master, *,
                 neutral_text,
                 active_text,
                 width=212,
                 height=65,
                 corner_radius=5,
                 font=("League Spartan", 36),

                 image_neutral=None,
                 image_active=None,
                 image_size,

                 fg_color_neutral,
                 fg_color_active,

                 text_color_neutral,
                 text_color_active,

                 bg_color="transparent",
                 border_color,

                 callback_command=None,
                 **kwargs):
        super().__init__(master, width=width, height=height,
                         corner_radius=corner_radius, fg_color=bg_color, **kwargs)
        self.pack_propagate(False)

        self.border_color = border_color
        self.border_width = 2.5

        self.state_active = False
        self.callback_command = callback_command

        # Store images and config
        self._image_neutral = ctk.CTkImage(light_image=image_neutral, dark_image=image_neutral, size=image_size) if image_neutral else None
        self._image_active = ctk.CTkImage(light_image=image_active, dark_image=image_active, size=image_size) if image_active else None
        self._fg_color_neutral = fg_color_neutral
        self._fg_color_active = fg_color_active
        self._text_color_neutral = text_color_neutral
        self._text_color_active = text_color_active
        self.neutral_text = neutral_text
        self.active_text = active_text

        # Button Frame (clickable area)
        self.button_frame = ctk.CTkFrame(self, corner_radius=corner_radius,
                                         fg_color=self._fg_color_neutral, border_color=self.border_color, border_width=self.border_width)
        self.button_frame.pack(fill="both", expand=True)

        # Icon
        self.image_label = ctk.CTkLabel(self.button_frame, text="", image=self._image_neutral,
                                        fg_color="transparent")
        self.image_label.pack(side="left", padx=10)

        # Text
        self.text_label = ctk.CTkLabel(self.button_frame, text=self.neutral_text, font=font,
                                       text_color=self._text_color_neutral, fg_color="transparent")
        self.text_label.pack(side="left", padx=0, pady=(4,10))

        # Bind clicks to all subcomponents
        for widget in (self, self.button_frame, self.image_label, self.text_label):
            widget.bind("<Button-1>", self._on_click)

    def _on_click(self, event=None):
        self.toggle_command()
        return "break"

    def toggle(self):
        self.state_active = not self.state_active
        self._update_appearance()
    
    def toggle_command(self):
        if self.callback_command:
            self.callback_command(self.active_text)

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
