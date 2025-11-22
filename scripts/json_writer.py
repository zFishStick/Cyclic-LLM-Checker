import json as js
import os

def write_json_to_file(data: dict) -> None:
    """Writes a dictionary to a JSON file."""
    json_file = "method_steps.json"
    
    if not os.path.exists("json"):
        os.makedirs("json")
        with open(json_file, 'w') as f:
            f.write("{}")
        json_file = os.path.join("json", json_file)
    
    with open(json_file, 'w') as json_file:
        js.dump(data, json_file, indent=4)
        
