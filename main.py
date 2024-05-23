from flask import render_template, request, session, redirect, url_for
from models import db
from database import create_app, get_user_by_name, add_user
import os

app = create_app()

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


def create_tables():
    if not os.path.exists("users.db"):
        with app.app_context():
            db.create_all()


@app.route("/")
def show_index():
    if "username" in session:
        return render_template("index.html", authorized=True)

    return render_template("index.html", not_authorised=True)


@app.route("/login", methods=["GET", "POST"])
def show_login():
    if request.method == "POST":
        entered_name = request.form["name"]
        entered_pass = request.form["pass"]

        user_data = get_user_by_name(entered_name)

        if user_data is None:
            return render_template("login.html", error=True)

        if entered_pass != user_data.get("password"):
            return render_template("login.html", error=True)
        # SUCCESSFULLY LOGIN
        else:
            session["username"] = entered_name
            return redirect(url_for("show_index"))

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def show_register():
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["pass"]
        rep_pass = request.form["rep_pass"]

        user_data = get_user_by_name(name)

        if user_data:
            return render_template("register.html", error=True)

        if password != rep_pass:
            return render_template("register.html", pass_error=True)

        add_user(username=name, password=password)
        return render_template("register.html", success=True)

    return render_template("register.html")


@app.route("/about")
def show_about():
    if "username" in session:
        return render_template("about.html", authorized=True)

    return render_template("about.html", not_authorised=True)


@app.route("/logout")
def logout():
    # remove the username from the session if it's there
    session.pop("username", None)
    return redirect(url_for("show_index"))


@app.route("/cheats")
def show_cheats():
    if "username" in session:
        return render_template("cheat.html", authorized=True)

    return render_template("cheat.html", not_authorised=True)


@app.route("/profile")
def show_profile():
    if "username" in session:
        return render_template("profile.html", username=session["username"])

    return redirect(url_for("show_index"))


if __name__ == "__main__":
    with app.app_context():
        create_tables()
    app.run(debug=True)
