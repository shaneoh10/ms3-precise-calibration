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
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Check if username exits on DB, if not create
    new user and store in DB
    """
    if request.method == "POST":

        username_exists = mongo.db.users.find_one(
            {"username": request.form.get("username")})
        if username_exists:
            flash("Username taken, please try another.")
            return redirect(url_for("register"))

        new_user = {
            "first_name": request.form.get("first_name").title(),
            "last_name": request.form.get("last_name").title(),
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "is_supervisor": False
        }
        mongo.db.users.insert_one(new_user)
        first_name = request.form.get("first_name")
        session["user"] = request.form.get("username").lower()
        flash(f"Welcome {first_name}, you have successfully registered.")
        return redirect(url_for('get_cals_due'))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username_exists = mongo.db.users.find_one(
            {"username": request.form.get("username")})

        if username_exists:
            if check_password_hash(
              username_exists["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(request.form.get("username")))
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
    session.clear()
    flash("You have been successfully logged out")
    return redirect(url_for("home"))


@app.route("/get_cals_due")
def get_cals_due():
    cals_due = list(mongo.db.cals_due.find())
    return render_template("cals-due.html", cals_due=cals_due)


@app.route("/get_cals_complete")
def get_cals_complete():
    cals_complete = list(mongo.db.cals_complete.find())
    return render_template("dashboard.html", cals_complete=cals_complete)


@app.route("/search", methods=["GET", "POST"])
def search_cals():
    query = request.form.get("query")
    cals_due = list(mongo.db.cals_due.find({"$text": {"$search": query}}))
    return render_template("cals-due.html", cals_due=cals_due)


@app.route("/cal_signoff/<cal_due_id>", methods=["GET", "POST"])
def cal_signoff(cal_due_id):
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
        mongo.db.cals_due.remove({"_id": ObjectId(cal_due_id)})
        mongo.db.cals_complete.insert_one(cal)
        flash("Calibration Signed Off")
        return redirect(url_for("get_cals_due"))

    cal_due = mongo.db.cals_due.find_one({"_id": ObjectId(cal_due_id)})
    return render_template(
        "cal-signoff.html", cal_due=cal_due, date_today=date_today)


@app.route("/new_cal", methods=["GET", "POST"])
def new_cal():
    if request.method == "POST":
        cal = {
            "tag_id": request.form.get("tag_id"),
            "inst_type": request.form.get("inst_type"),
            "location": request.form.get("location"),
            "due_date": request.form.get("due_date")
        }
        mongo.db.cals_due.insert_one(cal)
        flash("New Calibration Added")
        return redirect(url_for("get_cals_due"))

    return render_template("new-cal.html")


@app.route("/edit_cal/<cal_due_id>", methods=["GET", "POST"])
def edit_cal(cal_due_id):
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
    mongo.db.cals_due.remove({"_id": ObjectId(cal_due_id)})
    flash("Calibration removed")
    return redirect(url_for("get_cals_due"))


@app.route("/remove_cal_complete/<cal_complete_id>")
def remove_cal_complete(cal_complete_id):
    mongo.db.cals_complete.remove({"_id": ObjectId(cal_complete_id)})
    flash("Calibration closed out and removed from list")
    return redirect(url_for("get_cals_complete"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
