import csv
import os
from datetime import datetime

FILE = "transactions.csv"


# Create CSV file if it does not exist
def create_file():
    if not os.path.exists(FILE):
        with open(FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Type", "Category", "Amount"])


# Add Income or Expense
def add_transaction(transaction_type):

    print("\n----- ADD", transaction_type.upper(), "-----")

    category = input("Enter category: ").strip()

    if not category:
        print("Category cannot be empty!")
        return

    try:
        amount = float(input("Enter amount: "))

        if amount <= 0:
            print("Amount must be greater than zero!")
            return

    except ValueError:
        print("Invalid amount!")
        return

    date = input("Enter date (YYYY-MM-DD): ")

    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date!")
        return

    with open(FILE, "a", newline="") as f:

        writer = csv.writer(f)

        writer.writerow([
            date,
            transaction_type,
            category,
            amount
        ])

    print("\nTransaction saved successfully!")
    if transaction_type == "Expense":
        total_spent = 0

        with open(FILE, "r", newline="") as f:
            reader = csv.DictReader(f)
            for record in reader:
                if (record["Category"].strip().lower() == category.lower()
                    and record["Date"][:7] == date[:7]
                    and record["Type"] == "Expense"):
                    total_spent += float(record["Amount"])
                    
        with open("budgets.csv", "r", newline="") as f:
            reader = csv.reader(f)
            for row in reader:
                if row and row[0].strip().lower() == category.lower():
                    budget = float(row[1])
                    percentage = (total_spent / budget) * 100

                    if percentage >= 100:
                        print("ALERT! Monthly budget exceeded!")
                    elif percentage >= 80:
                        print("WARNING! You have used 80% of your budget!")
                    break

# View All Transactions
def view_transactions():

    print("\n----- ALL TRANSACTIONS -----")

    with open(FILE, "r", newline="") as f:
        reader = csv.DictReader(f)
        records = list(reader)

    if not records:
        print("No transactions found!")
        return

    for i, record in enumerate(records, start=1):

        print("\nTransaction:", i)
        print("Date:", record["Date"])
        print("Type:", record["Type"])
        print("Category:", record["Category"])
        print("Amount: Rs.", record["Amount"])

    print("\nTotal Transactions:", len(records))
    # Search Transactions
def search_transactions():

    search = input("Enter category to search: ").lower()

    found = False

    with open(FILE, "r", newline="") as f:
        reader = csv.DictReader(f)

        for record in reader:

            if search in record["Category"].lower():

                print("\nDate:", record["Date"])
                print("Type:", record["Type"])
                print("Category:", record["Category"])
                print("Amount: Rs.", record["Amount"])

                found = True

    if not found:
        print("No transaction found!")
        # Delete Transaction
def delete_transaction():
    with open(FILE, "r", newline="") as f:
        reader = csv.DictReader(f)
        records = list(reader)

    if not records:
        print("No transactions to delete!")
        return

    print("\n----- ALL TRANSACTIONS -----")
    for i, record in enumerate(records, start=1):
        print(i, record["Date"], record["Type"],
              record["Category"], record["Amount"])

    try:
        choice = int(input("\nEnter transaction number to delete: "))
        if choice < 1 or choice > len(records):
            print("Invalid transaction number!")
            return
    except ValueError:
        print("Please enter a valid number!")
        return

    records.pop(choice - 1)

    with open(FILE, "w", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=["Date", "Type", "Category", "Amount"]
        )
        writer.writeheader()
        writer.writerows(records)

    print("Transaction deleted successfully!")
    # Set Monthly Budget
def set_budget():
    category = input("Enter category: ").strip()

    try:
        amount = float(input("Enter monthly budget: "))
        if amount <= 0:
            print("Budget must be greater than zero!")
            return
    except ValueError:
        print("Invalid budget amount!")
        return

    with open("budgets.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([category, amount])

    print("Monthly budget saved successfully!")
    # Monthly Analysis
def monthly_analysis():
    month = input("Enter month (YYYY-MM): ")

    income = 0
    expense = 0
    categories = {}

    with open(FILE, "r", newline="") as f:
        reader = csv.DictReader(f)

        for record in reader:
            if record["Date"][:7] == month:
                amount = float(record["Amount"])

                if record["Type"] == "Income":
                    income += amount
                else:
                    expense += amount
                    category = record["Category"]
                    categories[category] = categories.get(category, 0) + amount

    print("\n----- MONTHLY ANALYSIS -----")
    print("Total Income: Rs.", income)
    print("Total Expense: Rs.", expense)
    print("Remaining Balance: Rs.", income - expense)

    print("\nCategory-wise Expenses:")
    for category, amount in categories.items():
        print(category, ": Rs.", amount)
        # Generate Monthly Report
def generate_report():
    month = input("Enter month (YYYY-MM): ")

    income = 0
    expense = 0

    with open(FILE, "r", newline="") as f:
        reader = csv.DictReader(f)

        for record in reader:
            if record["Date"][:7] == month:
                amount = float(record["Amount"])

                if record["Type"] == "Income":
                    income += amount
                else:
                    expense += amount

    balance = income - expense

    os.makedirs("reports", exist_ok=True)

    filename = f"reports/report_{month}.txt"

    with open(filename, "w") as f:
        f.write("----- SPENDWISE MONTHLY REPORT -----\n")
        f.write(f"Month: {month}\n")
        f.write(f"Total Income: Rs. {income}\n")
        f.write(f"Total Expense: Rs. {expense}\n")
        f.write(f"Remaining Balance: Rs. {balance}\n")

    print("Monthly report generated successfully!")
    print("Saved at:", filename)
# Main Program
create_file()

while True:

    print("\n================================")
    print("          SPENDWISE")
    print(" Smart Expense & Budget Analyzer")
    print("================================")

    print("1. Add Income")
    print("2. Add Expense")
    print("3. View Transactions")
    print("4. Search Transactions")
    print("5. Delete Transaction")
    print("6. Set Monthly Budget")
    print("7. Monthly Analysis")
    print("8. Generate Monthly Report")
    print("9. Exit")

    choice = input("\nEnter your choice: ")

    if choice == "1":
        add_transaction("Income")

    elif choice == "2":
        add_transaction("Expense")

    elif choice == "3":
        view_transactions()

    elif choice == "4":
        search_transactions()

    elif choice == "5":
        delete_transaction()

    elif choice == "6":
        set_budget()
    elif choice == "7":
        monthly_analysis()

    elif choice == "8":
     generate_report()


    elif choice == "9":
        print("Thank you for using SpendWise!")
        break

    else:
        print("Invalid choice! Try again.")