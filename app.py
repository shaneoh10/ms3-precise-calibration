import os
from datetime import datetime
from flask import (
    Flask, flash, request, session,
    redirect, url_for, render_template)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import (
    generate_password_hash, check_password_hash)
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
def home():
    """
    Renders the home page teplate
    """
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Allows users to register a new account. Checks if username
    already exits on DB and if password inputs match. Creates a
    new user and stores in DB.
    """
    if request.method == "POST":

        username_exists = mongo.db.users.find_one(
            {"username": request.form.get("reg-username")})
        if username_exists:
            flash("Username taken, please try another.")
            return redirect(url_for("register"))

        new_user = {
            "first_name": request.form.get("first_name").title(),
            "last_name": request.form.get("last_name").title(),
            "username": request.form.get("reg-username").lower(),
            "password": generate_password_hash(request.form.get(
                "reg-password")),
            "is_supervisor": False
        }
        if request.form.get("reg-password") == request.form.get(
                "password-check"):
            mongo.db.users.insert_one(new_user)
            first_name = request.form.get("first_name")
            flash(f"Welcome {first_name}, you have successfully registered.\
                Log in to access the application")
            return redirect(url_for('home'))
        else:
            flash("Passwords must match.")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Allows users with a registered account to log in. Checks if username
    exists on DB and if password is correct. If successful, adds user to
    the current session and redirects to the application.
    """
    if request.method == "POST":
        user_exists = mongo.db.users.find_one(
            {"username": request.form.get("username")})

        if user_exists:
            if check_password_hash(
              user_exists["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                session["is_supervisor"] = user_exists["is_supervisor"]
                session["name"] = ("{} {}").format(
                    user_exists["first_name"], user_exists["last_name"])
                flash("Welcome, {}".format(user_exists["first_name"]))
                if session["is_supervisor"]:
                    return redirect(url_for('get_cals_complete'))
                else:
                    return redirect(url_for('get_cals_due'))
            else:
                flash("Incorrect Username or Password")
                return redirect(request.referrer)
        else:
            flash("Incorrect Username or Password")
            return redirect(request.referrer)

    return redirect(request.referrer)


@app.route("/logout")
def logout():
    """
    Clears the session cookies, logging out current user
    and redirects user to home page.
    """
    if session["user"]:
        session.clear()
        flash("You have been successfully logged out")
    return redirect(url_for("home"))


@app.route("/get_cals_due")
def get_cals_due():
    """
    Queries the DB for all calibrations in the cals_due collection
    and renders the cals_due template presenting the calibrations
    to the user.
    """
    cals_due = list(mongo.db.cals_due.find())
    return render_template("cals-due.html", cals_due=cals_due)


@app.route("/get_cals_complete")
def get_cals_complete():
    """
    Queries the DB for all calibrations in the cals_complete
    collection and calibration totals in cal_totals collection
    collection and renders the cals_complete template presenting the
    data to the user.
    """
    cals_complete = list(mongo.db.cals_complete.find())
    cal_totals = list(mongo.db.cal_totals.find())
    return render_template(
        "dashboard.html", cals_complete=cals_complete, cal_totals=cal_totals)


@app.route("/search", methods=["GET", "POST"])
def search_cals():
    """
    Allows user to search for calibrations due on the cals-due page.
    """
    query = request.form.get("query")
    cals_due = list(mongo.db.cals_due.find({"$text": {"$search": query}}))
    return render_template("cals-due.html", cals_due=cals_due)


@app.route("/cal_signoff/<cal_due_id>", methods=["GET", "POST"])
def cal_signoff(cal_due_id):
    """
    Allows users to sign off a calibration as completed. When the calibration
    is signed off the current users name and the current date are attached with
    the existing calibration information, along with a pass or fail as input by
    the user. This is added to the DB as a complete calibration. The relevant
    cal_totals are also incremented in the DB.
    """
    date_today = datetime.now().strftime("%d %B %Y")
    if request.method == "POST":
        cal = {
            "tag_id": request.form.get("tag_id"),
            "inst_type": request.form.get("inst_type"),
            "location": request.form.get("location"),
            "due_date": request.form.get("due_date"),
            "signoff_user": request.form.get("signoff_user"),
            "signoff_date": date_today,
            "pass_or_fail": request.form.get("pass_or_fail")
        }
        cal_result = request.form.get("pass_or_fail").lower()
        mongo.db.cals_due.remove({"_id": ObjectId(cal_due_id)})
        mongo.db.cals_complete.insert_one(cal)
        mongo.db.cal_totals.update_one(
            {"_id": ObjectId("60b9de44da37adc68f38a3f7")},
            {"$inc": {"total_due": -1, f"total_{cal_result}": 1}})
        flash("Calibration Signed Off")
        return redirect(url_for("get_cals_due"))

    cal_due = mongo.db.cals_due.find_one({"_id": ObjectId(cal_due_id)})
    return render_template(
        "cal-signoff.html", cal_due=cal_due, date_today=date_today)


@app.route("/new_cal", methods=["GET", "POST"])
def new_cal():
    """
    Allows the user to add a new calibration to the DB. This gets added
    to the cals_due collection and the relevant cal totals are incremented
    on the DB.
    """
    if request.method == "POST":
        cal = {
            "tag_id": request.form.get("tag_id"),
            "inst_type": request.form.get("inst_type"),
            "location": request.form.get("location"),
            "due_date": request.form.get("due_date")
        }
        mongo.db.cals_due.insert_one(cal)
        mongo.db.cal_totals.update_one(
            {"_id": ObjectId("60b9de44da37adc68f38a3f7")},
            {"$inc": {"total_due": 1, "total_open": 1}})
        flash("New Calibration Added")
        return redirect(url_for("get_cals_due"))

    return render_template("new-cal.html")


@app.route("/edit_cal/<cal_due_id>", methods=["GET", "POST"])
def edit_cal(cal_due_id):
    """
    Allows users to make changes to any of the calibrations that
    are in the cals_due collection.
    """
    if request.method == "POST":
        cal = {
            "tag_id": request.form.get("tag_id"),
            "inst_type": request.form.get("inst_type"),
            "location": request.form.get("location"),
            "due_date": request.form.get("due_date")
        }
        mongo.db.cals_due.update({"_id": ObjectId(cal_due_id)}, cal)
        flash("Calibration Updated")
        return redirect(url_for("get_cals_due"))

    cal_due = mongo.db.cals_due.find_one({"_id": ObjectId(cal_due_id)})
    return render_template("edit-cal.html", cal_due=cal_due)


@app.route("/remove_cal/<cal_due_id>")
def remove_cal(cal_due_id):
    """
    Allows users to remove a calibration from the cals_due collection.
    This also increments the relevant cal_totals in the DB.
    """
    mongo.db.cals_due.remove({"_id": ObjectId(cal_due_id)})
    mongo.db.cal_totals.update_one(
            {"_id": ObjectId("60b9de44da37adc68f38a3f7")},
            {"$inc": {"total_due": -1, "total_open": -1}})
    flash("Calibration removed")
    return redirect(url_for("get_cals_due"))


@app.route("/remove_cal_complete/<cal_complete_id>")
def remove_cal_complete(cal_complete_id):
    """
    Allows users to remove a calibration from the cals_complete collection.
    This also increments the relevant cal_totals in the DB.
    """
    mongo.db.cals_complete.remove({"_id": ObjectId(cal_complete_id)})
    mongo.db.cal_totals.update_one(
            {"_id": ObjectId("60b9de44da37adc68f38a3f7")},
            {"$inc": {"total_open": -1}})
    flash("Calibration removed")
    flash("Calibration closed out and removed from list")
    return redirect(url_for("get_cals_complete"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
