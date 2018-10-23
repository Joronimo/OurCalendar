"""Calendar Events."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session,
                   Markup)
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Event, Invite

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def welcome():
    """Homepage."""

    logout = request.args.get("loggedOut")

    if logout:
        session.clear()
        message = Markup("You have been successfully logged out.")
        flash(message)


    return render_template("homepage.html")

@app.route("/login")
def login():
    """Show login page to enter email and password."""

    return render_template("login.html")

@app.route("/process-login", methods=["POST"])
def processed_login():

    email = request.form.get("email")
    password = request.form.get("password")

    emails = db.session.query(User.email).filter(User.email == email).all()

    for tup in emails:
        if email in tup:
            user_id = db.session.query(User.user_id).filter(User.email == email).all()
            user_id = user_id[0][0]
            session["user_id"] = user_id
            message = Markup("Logged In")
            flash(message)
            return redirect(f"/users/{user_id}")

    message = Markup("This email is not registered. Please register here.")
    flash(message)
    return render_template("registration.html")

@app.route("/registration")
def registration():
    """Show registration page to enter email and password."""

    return render_template("registration.html")

@app.route("/process-registration", methods=["POST"])
def processed_registration():

    email = request.form.get("email")
    password = request.form.get("password")

    email_users = db.session.query(User.email)
    emails = email_users.filter(User.email == email).all()

    print("LOOK FOR THIS!!!!", emails)

    if emails == []:
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        session["user_id"] = user.user_id
        message = Markup("You are now registered!")
        flash(message)
        return render_template("homepage.html")
    else:
        message = Markup("You already have an account. Please log in.")
        flash(message)
        return render_template("login.html")

@app.route("/users/<int:user_id>")
def show_user_info(user_id):
    """from URL with user ID, get all user information and display user page"""

    users = User.query.all()

    for user in users:
        if user.user_id == user_id:

            # user_ratings = Rating.query.filter(Rating.user_id == user.user_id).all()

            event_and_invite_id = (
            db.session.query(Invite.accepted, Event.host)
            .join(Movie).filter(Rating.user_id == user.user_id).all())

            return render_template("user_info.html",
                                   user=user,
                                   movies_and_ratings=movie_and_rating_id)

#generate database

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
