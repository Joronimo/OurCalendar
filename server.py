"""Calendar Events."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session,
                   Markup)
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Event

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
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
            user_id = db.session.query(User.id).filter(User.email == email).all()
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
    username = request.form.get("username")

    email_users = db.session.query(User.email)
    emails = email_users.filter(User.email == email).all()

    print("LOOK FOR THIS!!!!", emails)

    if emails == []:
        user = User(email=email, password=password, username=username)
        db.session.add(user)
        db.session.commit()
        session["user_id"] = user.id
        message = Markup("You are now registered!")
        flash(message)
        return render_template("homepage.html")
    else:
        message = Markup("You already have an account. Please log in.")
        flash(message)
        return render_template("login.html")

@app.route("/calendar")
def view_calendar():
    """Show registration page to enter email and password."""

    return render_template("calendar.html")

# @app.route("/users/<int:user_id>")
# def show_user_info(id):
#     """from URL with user ID, get all user information and display user page"""

#     users = User.query.all()

#     for user in users:
#         if user.id == id:

#             event_and_invite_id = (
#             db.session.query(Invite.accepted, Event.host)
#             .join(Event).filter(Invite.id == user.id).all())

#             return render_template("user_info.html",
#                                    user=user,
#                                    movies_and_ratings=movie_and_rating_id)

@app.route("/invite")
def create_invite():
    """Allows logged in user to create and send an invite to guests to attend an event."""

    return render_template("invite.html")

@app.route("/invitation", methods=["POST"])
def find_event_send_invitation():
    """If all email addresses invited are memebers of OurCalendar send invitation. Else: invite to app."""

    #get emails from invite html 
    emails = request.form.get("emails").split(',')
    print(emails)

    users_ids = []

    for email in emails:
        #######need to strip email for whitespace ########
        user = User.query.filter_by(email=email).first()
        users_ids.append(user.id)
    for user in users_ids:
        event = Event.query.filter_by(user_id=user).all()
        print(event)
    return render_template("invitation.html")

@app.route("/event")
def create_event():
    """event gets added to database"""


    #is priority users accepted 
    pass



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
