import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_NAME = os.path.join(BASE_DIR, "finance_data.json")

def load_data():
    if not os.path.exists(FILE_NAME):
        return[]
    try:
        with open(FILE_NAME, "r") as file:
            json.load(file)
        
    except json.JSONDecodeError:
        return[]
def save_data(data):
    with open (FILE_NAME, "w") as file:
        return json.dump(data, file, indent=4)
