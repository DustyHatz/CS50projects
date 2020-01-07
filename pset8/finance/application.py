import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from datetime import datetime
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import *

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # Select symbol owned by user and its quantity
    portfolio = db.execute("SELECT shares, symbol FROM transactions WHERE id = :id", id=session["user_id"])

    tmp_total = 0

    # Update the portfolio
    for transactions in portfolio:
        symbol = transactions["symbol"]
        shares = transactions["shares"]
        stock = lookup(symbol)
        stock_price = shares * stock["price"]
        tmp_total += stock_price
        db.execute("UPDATE transactions SET price=:price, total=:total WHERE id=:id AND symbol=:symbol",
                   price=usd(stock["price"]), total=usd(stock_price), id=session["user_id"], symbol=symbol)

    # Select user's cash
    users_cash = db.execute("SELECT cash FROM users WHERE id=:id", id=session["user_id"])

    # Add shares' cash to user's cash
    tmp_total += users_cash[0]["cash"]

    # Select portfolio table
    updated_portfolio = db.execute("SELECT * from transactions WHERE id=:id", id=session["user_id"])

    # Print portfolio to index homepage
    return render_template("index.html", stocks=updated_portfolio, cash=usd(users_cash[0]["cash"]), grand_total=usd(tmp_total))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "GET":
        return render_template("buy.html")

    else:
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not shares.isdigit() or float(shares) < 1:
            return apology("Must enter a valid number of shares", 400)

        shares = int(shares)
        stock = lookup(symbol)

        # Check that the stock symbol is valid
        if stock is None or symbol == "":
            return apology("Stock does not exist", 400)

        # Check that user has enough money to buy shares
        stock_price = shares * stock["price"]
        user_cash = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])

        if not user_cash or user_cash[0]["cash"] < stock_price:
            return apology("You do not have enough money", 400)

        # Update user's cash
        db.execute("UPDATE users SET cash = cash - :cash WHERE id = :id", cash=stock["price"] * shares, id=session["user_id"])

        # Select user shares of specified symbol
        user_shares = db.execute("SELECT shares FROM transactions WHERE id = :id AND symbol = :symbol",
                                 id=session["user_id"], symbol=stock["symbol"])

        # Update history
        now = datetime.now().strftime('%m-%d-%Y %H:%M:%S')
        db.execute("INSERT INTO history (symbol, shares, price, id, time) VALUES(:symbol, :shares, :price, :id, :time)",
                   symbol=stock["symbol"], shares=shares, price=stock["price"], id=session["user_id"], time=now)

        # If user has no shares of symbol, create new stock
        if not user_shares:
            user_shares = db.execute("INSERT INTO transactions (name, symbol, shares, price, total, id) VALUES(:name, :symbol, :shares, :price, :total, :id)",
                                     name=stock["name"], symbol=stock["symbol"], shares=shares, price=stock["price"], total=usd(stock["price"] * shares), id=session["user_id"])

        # If user does, increment the shares count
        else:
            shares_count = user_shares[0]["shares"] + shares
            db.execute("UPDATE transactions SET shares = :shares WHERE symbol = :symbol AND id = :id",
                       shares=shares_count, symbol=stock["symbol"], id=session["user_id"])

        # Redirect user to index page after they make a purchase
        return redirect("/")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""

    username = request.args.get("username")

    if len(username) < 1:
        return jsonify(False)

    check_username = db.execute("SELECT username FROM users WHERE username = :un", un=username)

    if len(check_username) == 0:
        return jsonify(True)
    else:
        return jsonify(False)


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    histories = db.execute("SELECT * from history WHERE id=:id", id=session["user_id"])

    return render_template("history.html", history=histories)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Check that a username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Check that password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Select username from database
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Check that username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user is logged in
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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # User reached route via POST (as by form submit)
    if request.method == "POST":
        stock = lookup(request.form.get("symbol"))

        # Check that the symbol is valid
        if not stock:
            return apology("invalid stock symbol", 400)

        if stock is None:
            return apology("Stock name does not exist", 400)

        return render_template("quoted.html", stock=stock)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        # Ensure a username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure a password was created
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure both entered passwords match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match", 400)

        # Collect data from input form
        username = request.form.get("username")
        password = request.form.get("password")

        # Hash the password
        hashed_pass = generate_password_hash(password)

        # Add to database
        result = db.execute("INSERT INTO users (username, hash) VALUES(:username, :password)",
                            username=username, password=hashed_pass)

        if not result:
            return apology("Sorry! Username already taken!", 400)

        # Store user id in session and automatically log them in
        session["user_id"] = result
        return redirect("/")

    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    symbols = db.execute("SELECT symbol FROM transactions WHERE id = :id", id=session["user_id"])
    if request.method == "POST":

        if not request.form.get("symbol"):
            return apology("Please Provide a valid Stock Symbol", 400)

        stock = lookup(request.form.get("symbol"))

        # Ensure valid symbol
        if not stock:
            return apology("Stock Symbol Does Not Exist", 400)

        # Ensure valid number of shares
        try:
            shares = int(request.form.get("shares"))
            if shares < 0:
                return apology("Shares must be positive number", 400)
        except:
            return apology("Shares must be positive number", 400)

        # Select user's shares
        user_shares = db.execute("SELECT shares FROM transactions WHERE id = :id AND symbol = :symbol",
                                 id=session["user_id"], symbol=stock["symbol"])

        # Check if user has enough shares to sell
        if not shares or user_shares[0]["shares"] < shares:
            return apology("Amount provided exceeds amount of shares owned", 400)

        # Update history
        now = datetime.now().strftime('%m-%d-%Y %H:%M:%S')
        db.execute("INSERT INTO history (symbol, shares, price, id, time) VALUES(:symbol, :shares, :price, :id, :time)",
                   symbol=stock["symbol"], shares=-shares, price=stock["price"], id=session["user_id"], time=now)

        # Update user's cash
        db.execute("UPDATE users SET cash = cash + :cash WHERE id = :id", cash=stock["price"] * shares, id=session["user_id"])

        # Select user shares of specified symbol
        user_shares = db.execute("SELECT shares FROM transactions WHERE id = :id AND symbol = :symbol",
                                 id=session["user_id"], symbol=stock["symbol"])

        # Decrement amount of shares from user's portfolio
        shares_count = user_shares[0]["shares"] - shares

        # If user has no shares left, delete it
        if shares_count == 0:
            user_shares = db.execute("DELETE FROM transactions WHERE id=:id AND name=:name",
                                     name=stock["name"], id=session["user_id"])

        # If user still has shares, update the shares count
        else:
            db.execute("UPDATE transactions SET shares = :shares WHERE symbol = :symbol AND id = :id",
                       shares=shares_count, symbol=stock["symbol"], id=session["user_id"])

        # Redirect user to index page after they make a purchase
        return redirect("/")
    else:
        return render_template("sell.html", symbols=symbols)


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "GET":
        return render_template("changepw.html")
    else:
        password = request.form.get("password")

        if password == "":
            return apology("Password cannot be blank", 400)

        pass_hash = generate_password_hash(password)

        db.execute("UPDATE users SET hash = :pw WHERE id = :id",
                   pw=pass_hash, id=session["user_id"])

        return render_template("pwchanged.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code,)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
