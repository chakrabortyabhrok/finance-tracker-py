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

    print("ID |   DATE   |     ITEM     |  AMOUNT  |    CATEGORY    |  PAYMENT  |     NOTES    ")
    print("-"*83)
    for e in expense_list:
        print(f"{e["id"]: <3} | {e["date"]: <10} | {e["item"]: <14} | {e["amount"]: >10.2f} | {e["category"]: <16} | {e["payment"]: <11} | {e["notes"]}")
        print("-"*83) 

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
    matches = (e for e in expense_list if e["category"].lower() == category.lower())

    if not matches:
        print(f"-- No expenses found for {category} --")

    print(f"Expenses for {category}: \n")
    for e in expense_list:
        print(f"{e["items"]:20} : ₹{e["amount"]:8.2f}")

def main(expense_list):
    MY_BUDGET = 3000




if __name__ == "__main__":
    main()