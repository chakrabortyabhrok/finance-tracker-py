import os
import json
from datetime import datetime

#peristnce
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_NAME = os.path.join(BASE_DIR, "finance_data.json")

def load_data():
    if not os.path.exists(FILE_NAME):
        return[]
    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)
        
    except json.JSONDecodeError():
        return []
    
def save_data(expense_list):
    with open(FILE_NAME, "w") as file:
        json.dump(expense_list, file, indent=4)

