import os
import json
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_NAME = os.path.join(BASE_DIR, "finance_data.json")

def load_data():
    if not os.path.exists(FILE_NAME):
        return []
    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []
    
def save_data(expense_list):
    with open(FILE_NAME, "w") as file:
        json.dump(expense_list, file, indent=4)

def get_new_id(expense_list):
    if not expense_list:
        return 1
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

        if cat in category_breakdown:
            category_breakdown[cat] += price
        else:
            category_breakdown[cat] = price

        if method in payment_breakdown:
            payment_breakdown[method] += price
        else:
            payment_breakdown[method] = price

    return total_spent, category_breakdown, payment_breakdown

MENU = """
a - Add Expense
v - View All Expenses
s - Statistics & Summaries
f - Filter by Category
d - Delete Expense
e - Exit
"""

def print_expense(expense_list):
    if not expense_list:
        print("-- No expense recorded --")
        return

    print("ID  |    DATE    |           ITEM            |   AMOUNT   |       CATEGORY       |     PAYMENT     |     NOTES    ")
    print("-"*120)
    for e in expense_list:
        print(f"{e['id']: <3} | {e['date']: <10} | {e['item']: <25} | ₹{e['amount']: >10.2f} | {e['category']: <20} | {e['payment_method']: <15} | {e['notes']}")
    print("-"*120) 

def display_stats(total_spent, category_breakdown, payment_breakdown, budget_limit):
    print(f"\nTotal spent: ₹{total_spent:.2f}")
    print(f"Remaining Budget: ₹{budget_limit - total_spent:.2f}")
    
    if total_spent > budget_limit:
        print("-- WARNING: OVER BUDGET !! --")

    print("\nCategory Breakdown:")
    for category, amount in category_breakdown.items():
        print(f"{category:20}   ₹{amount:8.2f}")

    print("\nPayment Breakdown:")
    for method, amount in payment_breakdown.items():
        print(f"{method:15}   ₹{amount:8.2f}")

def filter_category(expense_list, category_name):
    return [e for e in expense_list if e["category"].lower() == category_name.lower()]

def main():
    MY_BUDGET = 5000
    expense = load_data()
    print("-- Welcome to the Finance Manager !! --")
    print(f"Current Budget: {MY_BUDGET}")

    while True:
        print(MENU)
        choice = input("Enter your choice: ").lower().strip()

        if choice == "a":
            user_date = input("Input date (YYYY-MM-DD) or ENTER for today: ").strip()
            date = user_date if user_date else datetime.today().strftime("%Y-%m-%d")
            item = input("Enter item name: ").capitalize()
            
            while True:
                try:
                    amount = float(input("Enter amount: ").strip())
                    if amount > 0: break
                    print("-- Enter a positive amount --")
                except ValueError:
                    print("-- Enter a valid number --")

            category = input("Enter category: ").capitalize()
            method = input("Enter payment method: ").capitalize()
            notes = input("Enter note: ").capitalize()
            
            add_expense(expense, date, item, amount, category, method, notes)
            save_data(expense)
            print("-- Expense added --")

        elif choice == "v":
            print_expense(expense)

        elif choice == "s":
            if not expense:
                print("-- No Expenses --")
            else:
                total, cat_map, pay_map = calculate_expense(expense)
                display_stats(total, cat_map, pay_map, MY_BUDGET)

        elif choice == "f":
            cat_name = input("Enter category: ").lower()
            print_expense(filter_category(expense, cat_name))

        elif choice == "d":
            try:
                id_to_del = int(input("Enter ID to delete: "))
                if delete_expense(expense, id_to_del):
                    save_data(expense)
                    print("-- Deleted --")
                else:
                    print("-- ID not found --")
            except ValueError:
                print("-- Invalid ID --")

        elif choice == "e":
            print("-- Goodbye --")
            break

if __name__ == "__main__":
    main()