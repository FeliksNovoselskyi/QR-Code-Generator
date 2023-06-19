import os

import modules.utils.json_io as json_io


SETTINGS = json_io.read_json(
    json_path = os.path.abspath('settings.json')
)
THEME = json_io.read_json(
    os.path.abspath(SETTINGS["color_theme"])
)