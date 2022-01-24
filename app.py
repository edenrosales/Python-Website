from flask import Flask, render_template, url_for, session, request, redirect, flash
from datetime import timedelta
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key= "hello"
app.permanent_session_lifetime = timedelta(minutes=15)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db= SQLAlchemy(app)

class users(db.Model): #users is going to be the model, as well as the class
    _id = db.Column("id",db.Integer, primary_key=True)
    name = db.Column("name", db.String(100))
    email = db.Column("email", db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email

@app.route('/')
def printx():
    return render_template("printx.html")

@app.route('/redirect')
def sendTo():
    return redirect(url_for("printx"))

@app.route("/login/", methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        session.permenant= True
        user= request.form["nm"]  #returns the information from the website in the form of a dictionary key and info
        session["user"]=user

        found_user = users.query.filter_by(name=user).first()
        if found_user:
            session["email"] = found_user.email
        else:
            usr = users(user, "")
            db.session.add(usr)
            db.session.commit()

        flash("You were logged in!")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("You were already logged in")
            return redirect(url_for("user"))
        return render_template("login.html")


@app.route("/user/", methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]

        if request.method== "POST":
            email= request.form["email"]
            session["email"]=email
            found_user = users.query.filter_by(name=user).first()
            found_user.email=email
            db.session.commit()
            flash("Email was saved")
        else:
            if "email" in session:
                email= session["email"]
        return render_template("user.html", user=user, email=email)
    else:
        flash("You are not logged in right now")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    if "user" in session:
        session.pop("user", None)
        session.pop("email", None)
        flash("Logged out successfully.")
        return redirect(url_for("login"))
    else:
        flash("Cannot logout. Need to log in first", "error")
        return redirect(url_for("login"))

@app.route("/view")
def view():
    return render_template("viewall.html", values= users.query.all())

@app.route("/deleteuser", methods =["POST", "GET"])
def deleteuser():
    if request.method == "POST":
        delete_user_name = users.query.filter_by(name= request.form["usr"]).first()
        if delete_user_name:
            delete_user_name = users.query.filter_by(name=request.form["usr"]).delete()
            db.session.commit()
            flash("The user was deleted")
        else:
            flash("The user did not exist","error")
    return render_template("deleteuser.html")

@app.route("/image")
def image():
    return render_template('image.html')


if __name__ =="__main__":
    db.create_all()
    app.run(debug=True)










































# @app.route("/")
# def index():
#     return render_template('index.html')
# @app.route("/login/", methods=["POST", "GET"])
# def login():
#     if request.method == "POST":
#         session.permanent =True
#         user = request.form["name"]
#         session["user"] = user
#         return redirect(url_for("userlogin"))
#     else:
#         if "user" in session:
#             return redirect(url_for("userlogin"))
#         else:
#             return render_template("login.html")
#
# @app.route("/userlogin")
# def userlogin():
#     if "user" in session:
#         user = session["user"]
#         return f"<h1>{user}</h1>"
#     else:
#         return redirect(url_for("login"))
#
# @app.route("/logout/")
# def logout():
#     if "user" in session:
#         session.pop("user", None)
#         return redirect(url_for("userlogin"))
#     else:
#         return redirect(url_for("userlogin"))
#
# if __name__ == "__main__":
#     app.run(debug=True)
#
# engine = create_engine("sqlite+psyqlite:///:memory:", echo =True, future = True)
