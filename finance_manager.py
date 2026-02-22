import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_NAME = os.path.join(BASE_DIR, "finance_expense_list.json")

def load_expense_list():
    if not os.path.exists(FILE_NAME):
        return[]
    try:
        with open(FILE_NAME, "r") as file:
            json.load(file)
        
    except json.JSONDecodeError:
        return[]
def save_expense_list(expense_list):
    with open (FILE_NAME, "w") as file:
        return json.dump(expense_list, file, indent=4)

def get_new_id(expense_list):
    if not expense_list:
        return 1
    else:
        return max(d["id"] for d in expense_list) +1
    
def add_expense(expense_list, date, item, amount, category,  payment_method, notes):
    new_expense = {
        "id": get_new_id,
        "date": date,
        "item": item,
        "amount": amount,
        "category": category,
        "payment_method": payment_method,
        "notes": notes
    }
    expense_list.append(new_expense)

def delete_expense(expense_list, id):
    for d in expense_list:
        if d["id"] == id:
            expense_list.remove(d)
            return True
    return False

def calculate_stats(expense_list, budget_limit):
    total_spent = sum(e["category"] for e in expense_list)
    category_breakdown = {}
    payment_breakdown = {}
    for e in expense_list:
        cat = e["category"]
        price = e["amount"]
        method = e["payment_method"]

        if cat in category_breakdown:
            category_breakdown[cat] += price

        else:
            category_breakdown[cat] = price

        if method in payment_breakdown:
            payment_breakdown[method] += price

        else:
            payment_breakdown[method] = price

    return total_spent, category_breakdown, payment_breakdown

#UI_LAYER
MENU = """
a - Add Expense
v - View All Expenses (Table View)
s - Statistics & Summaries (Total spent, Budget check)
f - Filter by Category
d - Delete Expense
e - Exit
"""
