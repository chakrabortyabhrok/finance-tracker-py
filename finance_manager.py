import os
import json
from datetime import datetime

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

def get_new_id(expense_list):
    if not expense_list:
        return 1
    else:
        return max(e["id"] for e in expense_list) + 1

def add_expense(expense_list, date, item, amount, category, payment_method, notes):
    new_expense = {
        "id" : get_new_id(expense_list),
        "date" : date,
        "item" : item,
        "amount": amount,
        "category" : category,
        "payment_method": payment_method,
        "notes" : notes
    }
    expense_list.append(new_expense)

def delete_expense(expense_list, delete_id):
    for e in expense_list:
        if delete_id == e["id"]:
            expense_list.remove(e)
            return True
    return False

def calculate_expense(expense_list):
    total_spent = sum(e["amount"] for e in expense_list)
    category_breakdown = {}
    payment_breakdown = {}
    for e in expense_list:
        cat = e["category"]
        price = e["amount"]
        method = e["payment_method"]

        if category_breakdown[cat]:
            category_breakdown += category_breakdown[price]
        else:
            category_breakdown[cat] = price

        if payment_breakdown[method]:
            payment_breakdown += payment_breakdown[price]
        else:
            payment_breakdown = price

    return total_spent, category_breakdown, payment_breakdown

MENU = """
c - Current Balance
u - Update Current Budget
a - Add Expense
v - View All Expenses (Table View)
s - Statistics & Summaries (Total spent, Budget check)
f - Filter by Category
d - Delete Expense
e - Exit
"""
def print_expense(expense_list):
    if not expense_list:
        print("-- No expense recorded --")

    print("ID |    DATE    |         ITEM         |   AMOUNT   |      CATEGORY      |      PAYMENT      |    NOTES  ")
    print("-"*125)
    for e in expense_list:
        print(f"{e["id"]: <3} | {e["date"]: <12} | {e["item"]: <20} | {e["amount"]: <8} | {e["category"]: <20} | {e["payment"]: <15} | {e["notes"]}")
    print("-" * 125)

def display_stats(total_spent, category_breakdown, payment_breakdown, budget_limit):
    print(f"Total Spent: ₹{total_spent:.2f}")
    remaining_budget = total_spent - budget_limit
    print(f"Remaining Budget: ₹{remaining_budget}")

    print("\nCategory Breakdown: \n")
    for category, amount in category_breakdown:
        print(f"{category: 20}   ₹{amount: 8.2f}")

    print("\nPayment Breakdown: \n")
    for method, amount in payment_breakdown:
        print(f"{method: 15}   ₹{amount: 8.2f}")

def filter_category(expense_list, category_name):
    matches = [e for e in expense_list if e["category"].lower() == category_name.lower()]
    return matches
