import os
from flask import (
    Flask, flash, request, session, 
    redirect, url_for, render_template)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
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


@app.route("/get_cals_due")
def get_cals_due():
    cals_due = mongo.db.cals_due.find()
    return render_template("cals-due.html", cals_due=cals_due)


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
    cal_due = mongo.db.cals_due.find_one({"_id": ObjectId(cal_due_id)})
    return render_template("edit-cal.html", cal_due=cal_due)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)