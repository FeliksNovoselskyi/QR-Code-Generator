from customtkinter import CTkButton


class Button(CTkButton):
    def __init__(self, master, width, height, image, fg_color, hover_color, border_color, border_width, command):
        
        self.COMMAND_ARGS = None
        if isinstance(command[1], tuple) and len(command[1]) >= 1:
            self.COMMAND_ARGS = command[1]

        super().__init__(
            master = master,
            width = width,
            height = height,
            image = image,
            fg_color = fg_color,
            hover_color = hover_color,
            border_color = border_color,
            border_width = border_width,
            text = '',
            command = command[0]
        )
    
    def _clicked(self, event=None):
        if self._state != "disabled":

            self._on_leave()
            self._click_animation_running = True
            self.after(100, self._click_animation)

            if self._command is not None:
                if self.COMMAND_ARGS and isinstance(self.COMMAND_ARGS, tuple):
                    self._command(*self.COMMAND_ARGS)
                else:
                    self._command()