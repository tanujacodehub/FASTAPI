import json
import os 
FILE = "data.json"

def read_data():
    if not os.path.exists(FILE):
        return []

    with open("data.json", "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

# WRITE JSON
def write_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)