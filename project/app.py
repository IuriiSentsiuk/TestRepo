import math
from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from dateutil import relativedelta

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
db = SQL("sqlite:///database.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

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
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("must provide username", 400)

        if not username:
            return apology("must provide password", 400)

        if not username:
            return apology("must provide confirmation", 400)

        if password != confirmation:
            return apology("passwords not match", 400)

        hash = generate_password_hash(password)

        try:
            new_user = db.execute("INSERT INTO users(username, hash) VALUES(?, ?)", username, hash)
        except:
            return apology("username exist", 400)

        session["user_id"] = new_user

        return redirect("/")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]

    users_db = db.execute("SELECT * FROM users WHERE id = ?", user_id)

    return render_template("index.html", users_db = users_db)


@app.route("/add_cash", methods=["GET", "POST"])
@login_required
def add_cash():
    """add cash"""
    if request.method == "GET":
        return render_template("add.html")

    else:
        new_cash = int(request.form.get("new_cash"))

        if not new_cash:
            return apology("no cash value provided", 400)

        user_id = session["user_id"]
        user_cash_db = db.execute("SELECT * FROM users WHERE id = ?", user_id)
        user_cash = user_cash_db[0]["cash"]

        updated_cash = user_cash + new_cash

        db.execute("UPDATE users SET cash = ? WHERE id = ?", updated_cash, user_id)

        date = datetime.now()

        db.execute("INSERT INTO transactions(user_id, cash, date) VALUES(?, ?, ?)", user_id, new_cash, date)

        """add estimated_months"""
        user_desires_db = db.execute("SELECT * FROM desires WHERE is_purchased = 0")

        desire_ids = {}
        for i in user_desires_db:
            desire_ids[i['desire_id']] = i
            
        user_min_cash = int(user_cash_db[0]["min_cash"])
        salary = int(user_cash_db[0]["salary"])
        monthly_cash_expenses = int(user_cash_db[0]["monthly_cash_expenses"])
        monthly_pension_expenses = int(user_cash_db[0]["monthly_pension_expenses"])

        for i in desire_ids:
            free_cash = updated_cash - user_min_cash
            monthly_expenses_for_desire = salary - monthly_cash_expenses - monthly_pension_expenses
            if monthly_expenses_for_desire <= 0:
                estimated_months = math.ceil(desire_ids[i]['desire_price'] - free_cash)
            else:
                estimated_months = math.ceil((desire_ids[i]['desire_price'] - free_cash) / monthly_expenses_for_desire) 

            if estimated_months < 0:
                db.execute("UPDATE desires SET estimated_months = 0 WHERE desire_id = ?", desire_ids[i]['desire_id'])
            else:
                db.execute("UPDATE desires SET estimated_months = ? WHERE desire_id = ?", estimated_months, desire_ids[i]['desire_id'])

        return redirect("/")


@app.route("/add_money_info", methods=["GET", "POST"])
@login_required
def add_money_info():
    """add money"""
    if request.method == "GET":
        return render_template("money.html")

    else:
        user_id = session["user_id"]
        user_money_db = db.execute("SELECT min_cash, pension_savings, salary, monthly_cash_expenses, monthly_pension_expenses FROM users WHERE id = ?", user_id)

        new_min_cash = int(request.form.get("new_min_cash") or user_money_db[0]["min_cash"])
        new_pension_savings = int(request.form.get("new_pension_savings") or user_money_db[0]["pension_savings"])
        new_salary = int(request.form.get("new_salary") or user_money_db[0]["salary"])
        new_monthly_cash_expenses = int(request.form.get("new_monthly_cash_expenses") or user_money_db[0]["monthly_cash_expenses"])
        new_monthly_pension_expenses = int(request.form.get("new_monthly_pension_expenses") or user_money_db[0]["monthly_pension_expenses"])

        db.execute("UPDATE users SET min_cash = ?, pension_savings = ?, salary = ?, monthly_cash_expenses = ?, monthly_pension_expenses = ? WHERE id = ?", new_min_cash, new_pension_savings, new_salary, new_monthly_cash_expenses, new_monthly_pension_expenses, user_id)

        return redirect("/")


@app.route("/add_desire", methods=["GET", "POST"])
@login_required
def add_desire():
    """Add desire and desire_price"""
    if request.method == "POST":
        desire = request.form.get("desire")
        desire_price = int(request.form.get("desire_price"))

        if not desire:
            return apology("No desire provided", 400)

        if not desire_price or desire_price < 0:
            return apology("Price must be greater than 0", 400)

        user_id = session["user_id"]

        db.execute("INSERT INTO desires(user_id, desire, desire_price) VALUES(?, ?, ?)", user_id, desire, desire_price)

        return redirect("/")

    else:
        user_id = session["user_id"]

        desires_db = db.execute("SELECT * FROM desires WHERE user_id = ? and is_purchased = 0", user_id)

        return render_template("desires.html", desires_db = desires_db)
        

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    transactions_db = db.execute("SELECT * FROM transactions WHERE user_id = :id ORDER BY date DESC", id=user_id)
    return render_template("history.html", transactions = transactions_db)


@app.route("/buy_desire", methods=["POST"])
@login_required
def buy_desire(): 
    """buy_desire"""
    desire_id = request.form.get("desire_id")

    user_id = session["user_id"]

    user_cash_db = db.execute("SELECT * FROM users WHERE id = ?", user_id)
    user_cash = int(user_cash_db[0]["cash"])
    user_min_cash = int(user_cash_db[0]["min_cash"])
    
    user_desires_db = db.execute("SELECT desire_price, desire FROM desires WHERE desire_id = ?", desire_id)
    user_desire_price = int(user_desires_db[0]["desire_price"])
    user_desire_name = user_desires_db[0]["desire"]

    verification_sum = user_cash - user_desire_price

    if verification_sum < user_min_cash:
        return apology("Desire price is bigger than min cash", 400)

    updated_cash = user_cash - user_desire_price
    db.execute("UPDATE users SET cash = ? WHERE id = ?", updated_cash, user_id)

    date = datetime.now()

    db.execute("INSERT INTO transactions(user_id, cash, date, desire) VALUES(?, ?, ?, ?)", user_id, (-1)*user_desire_price, date, user_desire_name)

    db.execute("UPDATE desires SET is_purchased = 1 WHERE desire_id = ?", desire_id)

    """add estimated_months"""
    user_desires_db = db.execute("SELECT * FROM desires WHERE is_purchased = 0")
    
    desire_ids = {}
    for i in user_desires_db:
        desire_ids[i['desire_id']] = i

    user_min_cash = int(user_cash_db[0]["min_cash"])
    salary = int(user_cash_db[0]["salary"])
    monthly_cash_expenses = int(user_cash_db[0]["monthly_cash_expenses"])
    monthly_pension_expenses = int(user_cash_db[0]["monthly_pension_expenses"])

    for i in desire_ids:
        free_cash = updated_cash - user_min_cash
        monthly_expenses_for_desire = salary - monthly_cash_expenses - monthly_pension_expenses 
        estimated_months = math.ceil((desire_ids[i]['desire_price'] - free_cash) / monthly_expenses_for_desire) 

        if estimated_months < 0:
            db.execute("UPDATE desires SET estimated_months = 0 WHERE desire_id = ?", desire_ids[i]['desire_id'])
        else:
            db.execute("UPDATE desires SET estimated_months = ? WHERE desire_id = ?", estimated_months, desire_ids[i]['desire_id'])

    return redirect("/")
    

@app.route("/pension", methods=["GET", "POST"])
@login_required
def pension():
    if request.method == "GET":
        return render_template("pension.html")
    else:
        user_id = session["user_id"]
        user_money_db = db.execute("SELECT * FROM users WHERE id = ?", user_id)

        new_pension_savings = int(request.form.get("new_pension_savings") or user_money_db[0]["pension_savings"])  
        db.execute("UPDATE users SET pension_savings = ?", new_pension_savings)

        date_now = datetime.now()
        new_pension_date = request.form.get("new_pension_date") or user_money_db[0]["new_pension_date"] 
        db.execute("UPDATE users SET pension_date = ?", new_pension_date)
           
        d_pension = datetime.strptime(new_pension_date, "%Y-%m-%d") 
        
        delta = relativedelta.relativedelta(d_pension, date_now)
        
        delta_months = delta.months + (delta.years * 12)
        

        new_pension_start_savings = int(request.form.get("new_pension_start_savings") or user_money_db[0]["new_pension_start_savings"])
        db.execute("UPDATE users SET pension_start_savings = ?", new_pension_start_savings)
        
        new_monthly_pension_expenses = int((new_pension_start_savings - new_pension_savings)/ delta_months)
        
        db.execute("UPDATE users SET monthly_pension_expenses = ?", new_monthly_pension_expenses)

        return redirect("/")

