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

    print("ID  |    DATE    |           ITEM            |   AMOUNT   |       CATEGORY       |     PAYMENT     |     NOTES    ")
    print("-"*120)
    for e in expense_list:
        print(f"{e["id"]: <3} | {e["date"]: <10} | {e["item"]: <25} | {e["amount"]: >10.2f} | {e["category"]: <20} | {e["payment_method"]: <15} | {e["notes"]}")
    print("-"*120) 

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

def main():
    MY_BUDGET = 5000
    expense = load_data()
    print("-- Welcome to the Finance Manager !! --")
    print(f"Current Budget: {MY_BUDGET}")

    while True:
        print(MENU)
        choice = input("- Please Enter your choice: \n").lower().strip()

        if choice == "a":
            print("-- Add Expense --\n")
            user_date = input("Input the date(YYYY-MM-DD) | ENTER FOR TODAY : \n").strip()
            if user_date == "":
                date = datetime.today().strftime("%Y-%m-%d")
            else:
                date = user_date

            item = input("Enter the item name: \n").capitalize()

            while True:
                try:
                    amount = float(input("Enter the amount: \n").strip())
                    if amount > 0:
                        break                      
                    else:
                        print("-- Please enter a positive amount --\n")
                except ValueError:
                    print("-- Please enter a number --")

            category = input("Enter category: \n").capitalize()
            payment_method = input("Enter the payment method: \n").capitalize()
            notes = input("Enter note: \n").capitalize()
            add_expense(expense, date, item, amount, category, payment_method, notes)
            save_data(expense)
            print("-- Task added --")

        elif choice == "v":
            print_expense(expense)

        elif choice== "s":
            if not expense:
                print("-- No Expenses --")
            else:
                total_spent, category_breakdown, payment_breakdown = calculate_expense(expense)
                display_stats(total_spent, category_breakdown, payment_breakdown, MY_BUDGET)

        elif choice == "d"

        elif choice == "e":
            print("-- Goodbye --")
            break

        else:
            print("Invalid choice, try again.")




if __name__ == "__main__":
    main()