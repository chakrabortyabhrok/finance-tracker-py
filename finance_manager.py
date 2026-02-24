import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_NAME = os.path.join(BASE_DIR, "finance_data.json")

def load_expense_list():
    if not os.path.exists(FILE_NAME):
        return[]
    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return[]
    
def save_expense_list(expense_list):
    with open (FILE_NAME, "w") as file:
        json.dump(expense_list, file, indent=4)

def get_new_id(expense_list):
    if not expense_list:
        return 1
    else:
        return max(d["id"] for d in expense_list) +1
    
def add_expense(expense_list, date, item, amount, category,  payment_method, notes):
    new_expense = {
        "id": get_new_id(expense_list),
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
v - View All Expenses (Table View)
s - Statistics & Summaries (Total spent, Budget check)
f - Filter by Category
d - Delete Expense
e - Exit
"""

def print_expenses(expense_list):
    if not expense_list:
        print("-- No Expense Recorded --")

    print("ID  |    DATE    |           ITEM            |   AMOUNT   |       CATEGORY       |     PAYMENT     |     NOTES    ")
    print("-"*120)
    for e in expense_list:
        print(f"{e["id"]: <3} | {e["date"]: <10} | {e["item"]: <25} | {e["amount"]: >10.2f} | {e["category"]: <20} | {e["payment_method"]: <15} | {e["notes"]}")
    print("-"*120) 

def display_stats(total_spent, category_breakdown, budget_limit, payment_breakdown):
    print(f"Total spent: {total_spent:.2f}")
    print(f"Remaining Budget: {budget_limit - total_spent:.2f}")
    if total_spent > budget_limit:
        print("⚠️ WARNING: Over Budget!!")
    
    print("\nCategory Breakdown:\n")
    for category, amount in category_breakdown.items():
        print(f" {category:20}   ₹{amount: 8.2f}")
    print()

    print("\nPayment Breakdown:\n")
    for payment, amount in payment_breakdown.items():
        print(f"  {payment:20}  ₹{amount: 8.2f}")
    print()

def filter_by_category(expense_list, category):
    matches = [e for e in expense_list if e["category"].lower() == category.lower()]

    return matches

def main():
    MY_BUDGET = 500
    expense = load_expense_list()
    print("-- Welcome to the Finance manager !! --")
    print("Current Budget limit:", MY_BUDGET)

    while True:
        print(MENU)
        choice = input("Enter your choice: \n").lower().strip()

        if choice == "a":
            print("--- Add New Expense ---\n")
            user_date = input("Enter date (DD-MM-YYYY) or press Enter for today: ").strip()
            if user_date == "":
                date = datetime.today().strftime("%Y-%m-%d")
            else:
                date = user_date
            
            item = input("Name of the item: \n").capitalize()
            while True:
                try:
                    amount = float(input("Enter the amount: \n"))
                    if amount > 0:
                        break
                    else:
                        print("-- Please enter a positve amount --")
                except ValueError:
                    print("-- Invalid input. Please enter a number.--")
            category = input("Enter the category: \n").capitalize()
            payment_method = input("Enter the payment method: \n").capitalize()
            notes = input("Enter a note:\n").capitalize()
            add_expense(expense, date, item, amount, category, payment_method, notes)
            save_expense_list(expense)
            print("-- Expense Added --")

        elif choice == "v":
            print_expenses(expense)

        elif choice == "s":
            if not expense:
                print("-- No expense found --")
            else:
                total_spent, category_breakdown, payment_breakdown = calculate_stats(expense, MY_BUDGET)
                display_stats(total_spent, category_breakdown, MY_BUDGET, payment_breakdown)

        elif choice == "f":
            target_category = input("Enter the category name: \n")
            filtered = filter_by_category(expense, target_category)

            print(f"\nExpenses for {target_category}:")
            print_expenses(filtered)


        elif choice == "e":
            print("-- Goodbye --")
            break

        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()