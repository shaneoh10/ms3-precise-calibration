import os
import functools
from datetime import datetime, timedelta
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


def check_input(dict):
    """
    Checks if user input contains a valid string before uploading to DB.
    If user input is a string of blank spaces this function will return false.
    This function is used inside any functions where a user input is to be
    uploaded to the DB.
    """
    for value in dict.values():
        if isinstance(value, str):
            if not value.strip():
                return False
    return True


def check_date(date):
    """
    Checks date to ensure it matches the format that is used on the DB
    """
    try:
        datetime.strptime(date, "%d %B %Y")
        return True
    except ValueError:
        return False


def login_required(func):
    """
    Used as function decorator to only allow access to pages if
    user is logged in.
    https://blog.teclado.com/protecting-endpoints-in-flask-apps-by-requiring-login/
    """
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if "user" not in session:
            flash("Log in to view this page.")
            return redirect(url_for("home"))
        return func(*args, **kwargs)
    return secure_function


def supervisor_required(func):
    """
    Used as function decorator to only allow access to pages if
    user is logged in with supervisor access.
    https://blog.teclado.com/protecting-endpoints-in-flask-apps-by-requiring-login/
    """
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if "user" not in session or not session["is_supervisor"]:
            flash("Log in as a Supervisor to view this page.")
            return redirect(url_for("home"))
        return func(*args, **kwargs)
    return secure_function


@app.route("/")
def home():
    """
    Renders the home page teplate
    """
    return render_template("home.html")


# https://flask.palletsprojects.com/en/1.1.x/patterns/errorpages/
@app.errorhandler(404)
def page_not_found(e):
    """
    Renders 404 template if URL entered is not found.
    """
    return render_template('404.html'), 404


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
        if check_input(new_user):
            if request.form.get("reg-password") == request.form.get(
                    "password-check"):
                mongo.db.users.insert_one(new_user)
                first_name = request.form.get("first_name")
                flash(f"Welcome {first_name}, you have successfully registered.\
                    Log in to access the application.")
                return redirect(url_for('home'))
            else:
                flash("Passwords must match.")
        else:
            flash("Invalid input. Please complete all fields correctly.")
            return redirect(url_for("register"))

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
                flash("Welcome, {}.".format(user_exists["first_name"]))
                if session["is_supervisor"]:
                    return redirect(url_for('get_dashboard'))
                else:
                    return redirect(url_for('get_cals_due'))
            else:
                flash("Incorrect Username or Password.")
                return redirect(request.referrer)
        else:
            flash("Incorrect Username or Password.")
            return redirect(request.referrer)

    return redirect(request.referrer)


@app.route("/logout")
@login_required
def logout():
    """
    Clears the session cookies, logging out current user
    and redirects user to home page.
    """
    if session["user"]:
        session.clear()
        flash("You have been successfully logged out.")
    return redirect(url_for("home"))


@app.route("/get_cals_due")
@login_required
def get_cals_due():
    """
    Queries the DB for all calibrations in the cals_due collection
    and renders the cals_due template presenting the calibrations
    to the user. List of cals due is then sorted by due date in
    ascending order. If due date for calibration is 7 days or less
    a warning will be displayed to the user.
    """
    cals_due = list(mongo.db.cals_due.find())

    # Converts due_date list to datetime objects
    def get_date(list):
        date = list["due_date"]
        return datetime.strptime(date, "%d %B %Y")

    # Converts individual due_dates to datetime objects
    def get_date_string(string):
        return datetime.strptime(string, "%d %B %Y")

    today = datetime.now()
    delta = timedelta(days=7)
    cals_due.sort(key=get_date)
    return render_template(
        "cals-due.html", cals_due=cals_due, today=today,
        delta=delta, get_date_string=get_date_string)


@app.route("/get_dashboard")
@supervisor_required
def get_dashboard():
    """
    Queries the DB for all calibrations in the cals_complete
    collection and calibration totals in cal_totals collection
    collection and renders the dashboard template presenting the
    data to the user.
    """
    cals_complete = list(mongo.db.cals_complete.find())
    cal_totals = list(mongo.db.cal_totals.find())
    return render_template(
        "dashboard.html", cals_complete=cals_complete, cal_totals=cal_totals)


@app.route("/search", methods=["GET", "POST"])
@login_required
def search_cals():
    """
    Allows user to search for calibrations due on the cals-due page.
    Results are returned in order of due_date ascending. If due date
    for calibration is 7 days or less a warning will be displayed to the user.
    """
    query = request.form.get("query")
    cals_due = list(mongo.db.cals_due.find({"$text": {"$search": query}}))

    # Converts due_date list to datetime objects
    def get_date(list):
        date = list["due_date"]
        return datetime.strptime(date, "%d %B %Y")

    # Converts individual due_dates to datetime objects
    def get_date_string(string):
        return datetime.strptime(string, "%d %B %Y")

    today = datetime.now()
    delta = timedelta(days=7)
    cals_due.sort(key=get_date)
    return render_template(
        "cals-due.html", cals_due=cals_due, today=today,
        delta=delta, get_date_string=get_date_string)


@app.route("/cal_signoff/<cal_due_id>", methods=["GET", "POST"])
@login_required
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
        flash("Calibration successfully Signed Off.")
        return redirect(url_for("get_cals_due"))

    cal_due = mongo.db.cals_due.find_one({"_id": ObjectId(cal_due_id)})
    return render_template(
        "cal-signoff.html", cal_due=cal_due, date_today=date_today)


@app.route("/new_cal", methods=["GET", "POST"])
@supervisor_required
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
        if check_date(request.form.get("due_date")):
            if check_input(cal):
                mongo.db.cals_due.insert_one(cal)
                mongo.db.cal_totals.update_one(
                    {"_id": ObjectId("60b9de44da37adc68f38a3f7")},
                    {"$inc": {"total_due": 1, "total_open": 1}})
                flash("New Calibration Added.")
                return redirect(url_for("get_cals_due"))
            else:
                flash("Invalid input. Please complete all fields correctly.")
                return redirect(url_for("new_cal"))
        else:
            flash("Invalid date format. Please use the date picker to choose a\
                 due date.")

    return render_template("new-cal.html")


@app.route("/edit_cal/<cal_due_id>", methods=["GET", "POST"])
@supervisor_required
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
        if check_input(cal):
            mongo.db.cals_due.update({"_id": ObjectId(cal_due_id)}, cal)
            flash("Calibration details successfully updated.")
            return redirect(url_for("get_cals_due"))
        else:
            flash("Invalid input. Please complete all fields correctly.")
            return redirect(url_for("get_cals_due"))

    cal_due = mongo.db.cals_due.find_one({"_id": ObjectId(cal_due_id)})
    return render_template("edit-cal.html", cal_due=cal_due)


@app.route("/remove_cal/<cal_due_id>")
@supervisor_required
def remove_cal(cal_due_id):
    """
    Allows users to remove a calibration from the cals_due collection.
    This also increments the relevant cal_totals in the DB.
    """
    mongo.db.cals_due.remove({"_id": ObjectId(cal_due_id)})
    mongo.db.cal_totals.update_one(
            {"_id": ObjectId("60b9de44da37adc68f38a3f7")},
            {"$inc": {"total_due": -1, "total_open": -1}})
    flash("Calibration successfully deleted.")
    return redirect(url_for("get_cals_due"))


@app.route("/remove_cal_complete/<cal_complete_id>")
@supervisor_required
def remove_cal_complete(cal_complete_id):
    """
    Allows users to remove a calibration from the cals_complete collection.
    This also increments the relevant cal_totals in the DB.
    """
    mongo.db.cals_complete.remove({"_id": ObjectId(cal_complete_id)})
    mongo.db.cal_totals.update_one(
            {"_id": ObjectId("60b9de44da37adc68f38a3f7")},
            {"$inc": {"total_open": -1}})
    flash("Calibration closed out and removed from the system.")
    return redirect(url_for("get_dashboard"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=False)
