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

    # Select user's first name from users database
    usernames = db.execute("SELECT name FROM users WHERE id=:id", id=session["user_id"])

    # Select user tasks and sort them by due date
    user_tasks = db.execute("SELECT * FROM tasks WHERE id=:id ORDER BY date", id=session["user_id"])

    # Pass in the name and tasks to index.html for display
    return render_template("index.html", butts=user_tasks, users=usernames)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Check that a username was submitted
        if not request.form.get("username"):
            flash("Please provide a username")

        # Check that password was submitted
        elif not request.form.get("password"):
            flash("Please provide a password")

        # Select username from database
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username").lower())

        # Check that username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("Invalid Username and/or Password")
            return render_template("login.html")

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
            flash("Please provide a username")

        # Ensure a password was created
        elif not request.form.get("password"):
            flash("Please provide a password")

        # Ensure both entered passwords match
        elif request.form.get("password") != request.form.get("confirmation"):
            flash("Passwords do not match")

        # Collect data from input form (username is converted to lowercase before storing in database)
        username = request.form.get("username").lower()
        password = request.form.get("password")
        name = request.form.get("name")

        # Hash the password
        hashed_pass = generate_password_hash(password)

        # Get all users from database
        users = db.execute("SELECT * FROM users")

        # Check if the username already exists
        for user in users:

            if user["username"] == username:
                flash("Username already taken")
                return render_template("register.html")
        else:
            # Add to database
            result = db.execute("INSERT INTO users (username, hash, name) VALUES(:username, :password, :name)",
                                username=username, password=hashed_pass, name=name)

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
        # Get new password from form input
        password = request.form.get("password")

        # Ensure a new password was entered
        if password == "":
            flash("Password cannot be blank")

        # Hash the password
        pass_hash = generate_password_hash(password)

        # Update user password in database
        db.execute("UPDATE users SET hash = :pw WHERE id = :id",
                   pw=pass_hash, id=session["user_id"])

        return render_template("pwchanged.html")


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():

    if request.method == "POST":

        # Ensure a task was entered
        if not request.form.get("task"):
            flash("Please enter a task")
            return render_template("index.html")

        # Ensure a due date was entered
        if not request.form.get("date"):
            flash("Please enter a due date")
            return render_template("index.html")

        # Get the task and due date from form input
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

        # Copy the selected task and due date from the tasks database and insert them into the completed database
        db.execute("INSERT INTO completed (task, date_due) VALUES((SELECT task FROM tasks WHERE todo=?), (SELECT date FROM tasks WHERE todo=?))",
                   (request.form["task_to_delete"]), (request.form["task_to_delete"]))

        # Update the user id in the completed database
        db.execute("UPDATE completed SET id=:id", id=session["user_id"])

        # Delete the task entirely from the tasks database
        db.execute("DELETE FROM tasks WHERE todo=?", (request.form["task_to_delete"],))

        return redirect("/")


@app.route("/delete_completed", methods=["POST"])
@login_required
def delete_completed():

    if request.method == "POST":

        # Delete the task entry entirely from the completed database
        db.execute("DELETE FROM completed WHERE task_id=?", (request.form["id_to_delete"]))

        return redirect("/completed")


@app.route("/completed")
@login_required
def completed():

        # Select all completed user specific tasks and sort them in the table by most recently completed
        completed_tasks = db.execute("SELECT * FROM completed WHERE id=:id ORDER BY date_complete ASC", id=session["user_id"])

        return render_template("completed.html", completes=completed_tasks)


if __name__ == '__main__':
    app.run(debug=True)