import re
import urllib.parse


from sqlite3 import Error
from datetime import date
from cs50 import SQL
from flask import Flask, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/history", methods=["GET", "POST"])
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    transactions = db.execute("SELECT id, date, description, type, income, savings, expenses FROM new WHERE user_id=?", user_id)

    return render_template("history.html", transactions=transactions)

@login_required
@app.route('/delete', methods=['POST'])
def delete():
    user_id = session["user_id"]
    balances1 = db.execute("SELECT balance FROM users WHERE id = ?", user_id)
    expenses1 = db.execute("SELECT expenses FROM new WHERE id = ?",[request.form['transaction_to_delete']])
    savings1 = db.execute("SELECT savings FROM users WHERE id = ?", user_id)
    income1 = db.execute("SELECT income FROM new WHERE id = ?",[request.form['transaction_to_delete']])
    saving1 = db.execute("SELECT savings FROM new WHERE id = ?",[request.form['transaction_to_delete']])
    balance = balances1[0]["balance"]
    expenses = expenses1[0]["expenses"]
    savings = savings1[0]["savings"]
    income= income1[0]["income"]
    saving = saving1[0]["savings"]

    if saving > 0:
        new_savings = savings - saving
        db.execute("UPDATE users SET savings = ? WHERE id = ?", new_savings, user_id)
    if expenses > 0:
        new_balance = balance + expenses
        db.execute("UPDATE users SET balance = ? WHERE id = ?", new_balance, user_id)
    if income > 0:
        new_balance = balance - income
        db.execute("UPDATE users SET balance = ? WHERE id = ?", new_balance, user_id)

    db.execute('DELETE FROM new WHERE id = ?', [request.form['transaction_to_delete']])
    return redirect(url_for('history'))

@app.route("/tracker", methods=["GET", "POST"])
@login_required
def tracker():
    if request.method == "POST":
        date = request.form.get("date")
        description = request.form.get("description")
        expense_type = request.form.get("type").lower()
        amount = float(request.form.get("amount"))
        user_id = session["user_id"]

        balances = db.execute("SELECT balance FROM users WHERE id = ?", user_id)

        savings = db.execute("SELECT savings FROM users WHERE id = ?", user_id)

        balance = balances[0]["balance"]
        saving = savings[0]["savings"]

# Error if data is not ok
        if not expense_type:
            return apology("Must Provide a Type")

        if expense_type == "income":
            pass
        elif expense_type == "expense":
            pass
        elif expense_type == "saving":
            pass
        else:
            return apology("Not valid type")

        if not description:
            return apology("Must write description")

        if not amount:
            return apology("Must input amount")

        if not date:
            return apology("Must input date")


# Put data into database
        if expense_type == "income":
            new_balance = balance + amount
            db.execute("UPDATE users SET balance = ? WHERE id = ?", new_balance, user_id)
            db.execute("INSERT INTO new (user_id, description, type, savings, income, expenses, date) VALUES (?,?,?,?,?,?,?)",
                    user_id, description, expense_type, 0, amount, 0, date)
        elif expense_type == "expense":
            new_balance = balance - amount
            db.execute("UPDATE users SET balance = ? WHERE id = ?", new_balance, user_id)
            db.execute("INSERT INTO new (user_id, description, type, savings, income, expenses, date) VALUES (?,?,?,?,?,?,?)",
                    user_id, description, expense_type, 0, 0, amount, date)
        else:
            new_saving = saving + amount
            db.execute("UPDATE users SET savings = ? WHERE id = ?", new_saving, user_id)
            db.execute("INSERT INTO new (user_id, description, type, savings, income, expenses, date) VALUES (?,?,?,?,?,?,?)",
                    user_id, description, expense_type, amount, 0, 0, date)

        return render_template("tracker.html")
    else:
        return render_template("tracker.html")

@app.route("/")
@login_required
def index():
    user_id = session["user_id"]

    date_now = date.today()

    stocks = db.execute(
        "SELECT balance, savings FROM users WHERE id =  ?", user_id)


    return render_template("index.html", stocks=stocks, date = date_now)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Request
    if request.method == "GET":
        return render_template("register.html")

    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not username:
            return apology("Must Give Username")

        elif not password and len(password) > 8:
            return apology("Must Give Password")

        elif not confirmation:
            return apology("Must Fill Password Confirmation")

        if password != confirmation:
            return apology("Password Does Not Match")

        # Hash the user password
        hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        try:
            new_user = db.execute('INSERT INTO users (username, hash, balance, savings) VALUES (?, ?, ?, ?)', username, hash, 0, 0)
        except:
            return apology("User Already Exists", 401)

        session["user_id"] = new_user

        return redirect("/")