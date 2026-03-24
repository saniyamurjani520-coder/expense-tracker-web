from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def connect_db():
    return sqlite3.connect("expenses.db")

# 🔹 create table automatically
def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        amount REAL,
        category TEXT,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()

create_table()

# 🔹 home page
@app.route("/")
def index():
    return render_template("index.html")

# 🔹 add expense
@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    amount = request.form["amount"]
    category = request.form["category"]
    date = request.form["date"]

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO expenses (name, amount, category, date) VALUES (?, ?, ?, ?)",
        (name, amount, category, date)
    )

    conn.commit()
    conn.close()

    return redirect("/show")

# 🔹 show expenses
@app.route("/show")
def show():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM expenses")
    data = cursor.fetchall()

    conn.close()

    return render_template("show.html", expenses=data)

# 🔹 delete expense (NEW)
@app.route("/delete/<int:id>")
def delete(id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM expenses WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return redirect("/show")


if __name__ == "__main__":
    app.run(debug=True)