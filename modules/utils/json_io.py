import json
import os

def read_json(json_path):
    data = {"color_theme": "resources/themes/aqua.json"}
    
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding = 'utf-8') as f:
            data = json.loads(f.read())
    else:
        with open(json_path, 'w', encoding = 'utf-8') as f:
            json.dump(data, f, indent = 4)
            
    return data



def write_to_json(json_path, data):
    prev_json_data = read_json(json_path)
    
    with open(json_path, 'w', encoding = 'utf-8') as f:
        json.dump(prev_json_data | data, f, indent = 4)