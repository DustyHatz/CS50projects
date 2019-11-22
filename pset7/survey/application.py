import cs50
import csv

from flask import Flask, jsonify, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")


@app.route("/form", methods=["POST"])
def post_form():
    # Validate that all form fields are filled out
    if not request.form.get("name_owner") or not request.form.get("name_dog") or not request.form.get("age_dog") or not request.form.get("gender") or not request.form.get("breed"):
        return render_template("error.html", message="You must complete the form!")
    else:
        # Write form information to csv file and redirect to /sheet URL
        with open("survey.csv", "a") as file:
            writer = csv.writer(file)
            writer.writerow((request.form.get("name_owner"), request.form.get("name_dog"),
                             request.form.get("age_dog"), request.form.get("gender"), request.form.get("breed")))
        return redirect("/sheet")


@app.route("/sheet", methods=["GET"])
def get_sheet():
    # Read data from csv file into a new list
    with open("survey.csv", "r") as file:
        reader = csv.reader(file)
        cust_info = list(reader)
    return render_template("success.html", cust_info=cust_info)
