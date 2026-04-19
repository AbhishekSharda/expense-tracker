import csv
from datetime import datetime
import pandas as pd


def add_expense():
    amount = input("Enter amount: ")
    category = input("Enter category (food, travel, etc.): ")
    description = input("Enter description: ")

    date = datetime.now().strftime("%Y-%m-%d")

    # Create file with header if it doesn't exist
    try:
        with open("expenses.csv", "x", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Amount", "Category", "Description"])
    except FileExistsError:
        pass

    # Append data
    with open("expenses.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, amount, category, description])

    print("\nExpense saved successfully!")


def view_expenses():
    try:
        with open("expenses.csv", mode="r") as file:
            reader = csv.reader(file)
            print("\n--- Expense History ---")
            for row in reader:
                print(row)
    except FileNotFoundError:
        print("No expenses found yet.")


def analyze_expenses():
    import os

    if not os.path.exists("expenses.csv"):
        print("\nNo data found. Please add expenses first.")
        return

    try:
        print("\nAnalyzing expenses...\n")

        df = pd.read_csv("expenses.csv")

        if df.empty:
            print("No data available to analyze.")
            return

        df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
        df = df.dropna(subset=["Amount"])

        print("--- Expense Data ---")
        print(df.to_string(index=False))

        print(f"\nTotal Spending: {df['Amount'].sum()}")

        print("\nSpending by Category:")
        print(df.groupby("Category")["Amount"].sum())

    except Exception as e:
        print("Error during analysis:", e)


def main():
    while True:
        print("\n=== Expense Tracker ===")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Analyze Expenses")
        print("4. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            analyze_expenses()
        elif choice == "4":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()