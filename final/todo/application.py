import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from datetime import datetime
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import *

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


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///todo.db")



@app.route('/')
@login_required
def index():

    user_tasks = db.execute("SELECT * FROM tasks WHERE id=:id", id=session["user_id"])

    return render_template("index.html", butts=user_tasks)


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


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():

    if request.method == "POST":

        if not request.form.get("task"):
            return apology("Must enter a task!", 400)

        elif not request.form.get("date"):
            return apology("Must enter a due date!", 400)

        new_task = request.form.get("task")
        date_due = request.form.get("date")

        # Add task to tasks table
        db.execute("INSERT INTO tasks (id, task, date) VALUES(:id, :task, :date)",
                    id=session["user_id"], task=new_task, date=date_due)

        return redirect("/")
    else:
        return render_template("index.html")


@app.route("/delete", methods=["POST"])
@login_required
def delete():
    if request.method == "POST":

        db.execute("INSERT INTO completed (task, date_due) VALUES((SELECT task FROM tasks WHERE todo=?), (SELECT date FROM tasks WHERE todo=?))",
                   (request.form["task_to_delete"]), (request.form["task_to_delete"]))


        db.execute("UPDATE completed SET id=:id", id=session["user_id"])

        db.execute("DELETE FROM tasks WHERE todo=?", (request.form["task_to_delete"],))

        return redirect("/")


@app.route("/delete_completed", methods=["POST"])
@login_required
def delete_completed():

    if request.method == "POST":

        db.execute("DELETE FROM completed WHERE task_id=?", (request.form["id_to_delete"]))

        return redirect("/completed")


@app.route("/completed")
@login_required
def completed():

        completed_tasks = db.execute("SELECT * FROM completed WHERE id=:id", id=session["user_id"])

        return render_template("completed.html", completes=completed_tasks)


if __name__ == '__main__':
    app.run(debug=True)