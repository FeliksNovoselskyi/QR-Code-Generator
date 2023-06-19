import customtkinter as ctk 
import sys
import os

import modules.utils.json_io as json_io


class SelectTheme(ctk.CTkOptionMenu):
    def __init__(self, *args, **kwargs):
        super().__init__(
            master = kwargs['master'],
            width = kwargs['width'],
            height = kwargs['height'],
            fg_color = kwargs['fg_color'],
            button_color = kwargs['button_color'],
            button_hover_color = kwargs['button_hover_color'],
            command = self.change_theme,
            values = self.get_values(),
        )
        
    def get_values(self):
        values = []
        
        themes_path = os.path.abspath('resources/themes')
        for theme in os.listdir(themes_path):
            # theme_path = os.path.join(themes_path, theme)
            theme_name = theme.split('.')[0]
            values.append(theme_name)

        values = sorted(values)
        cur_theme = os.path.split(json_io.read_json(
            json_path = os.path.abspath("settings.json")
        )['color_theme'])[1].split('.')[0]

        prev_index = values.index(cur_theme)
        temp = values[0]
        values[0] = cur_theme
        values[prev_index] = temp
        return values
    
    def change_theme(self, theme):
            json_io.write_to_json(
                data = {"color_theme": f'resources/themes/{theme}.json'},
                json_path = os.path.abspath('settings.json')
            )
            os.execl(sys.executable, sys.executable, '"' + sys.argv[0] + '"')