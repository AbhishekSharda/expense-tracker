from flask import Flask, render_template, request, redirect
import csv
from datetime import datetime
import os

app = Flask(__name__)


@app.route("/")
def home():
    expenses = []
    total = 0
    category_summary = {}

    if os.path.exists("expenses.csv"):
        import pandas as pd

        df = pd.read_csv("expenses.csv")

        if not df.empty:
            total = df["Amount"].sum()
            category_summary = df.groupby("Category")["Amount"].sum().to_dict()

            expenses = df.values.tolist()

    return render_template(
        "index.html",
        expenses=expenses,
        total=total,
        category_summary=category_summary
    )


@app.route("/add", methods=["POST"])
def add():
    amount = request.form["amount"]
    category = request.form["category"]
    description = request.form["description"]

    date = datetime.now().strftime("%Y-%m-%d")

    # Create file with header if it doesn't exist
    file_exists = os.path.exists("expenses.csv")

    with open("expenses.csv", "a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Date", "Amount", "Category", "Description"])

        writer.writerow([date, amount, category, description])

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)