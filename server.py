"""Calendar Events."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session,
                   Markup)
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Event

from datetime import timedelta, datetime, date

import calendar




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


@app.route("/invite")
def create_invite():
    """Allows logged in user to create and send an invite to guests to attend an event."""

    return render_template("invite.html")

@app.route("/invitation", methods=["POST"])
def find_event_send_invitation():
    """If all email addresses invited are memebers of OurCalendar send invitation. Else: invite to app."""

    #get emails from invite html 
    emails = request.form.get("emails").split(',')

    users_ids = []

    # convert emails into user ids
    for email in emails:
        email = email.replace(" ", "")
        user = User.query.filter_by(email=email).first()
        users_ids.append(user.id)
    
    all_events = set()

    for user in users_ids:
        #get user events by their user id
        users_events = Event.query.filter_by(user_id=user).all()

        #add each event start and end times to the set 'all_events'
        for event in users_events:
            events = Event.query.filter_by(id=event.id).all()
            tup_of_event = (event.start_time, event.end_time)
            all_events.add(tup_of_event)

    ######### get timeline start and end  ############# 

    timeline = request.form["timeline"]
    duration = request.form["duration"]
    
   
    #round start to the nearest quarter hour
    def get_start_time():
        """gets start time rounded to the nearest quarter hour starting at now"""

        start = datetime.now()
        start.replace(second=0, microsecond=0)


        if start.minute < 45:
            if start.hour == 23:
                start.replace(day=start.day+1, hour=0, second=0, microsecond=0)
            else:
                start.replace(hour=start.hour + 1, second=0, microsecond=0)
            return start
        elif 00 >= start.minute <= 15:
            start.replace(minute=15, second=0, microsecond=0)
            print(start)
            return start
        elif 15 >= start.minute <= 30:
            start.replace(minute=30, second=0, microsecond=0)
            return start
        elif 30 >= start.minute <= 45:
            start.replace(minute=45, second=0, microsecond=0)
            return start

    start = get_start_time()
    print("XXXXXXXXXXXXXxxxxXXXX")
    print(get_start_time())

    date_range = set()

    if timeline == 'two weeks':
        end = start.replace(day=start.day + 1)
        print("Helllllllllllllo", end)
        for n in range(int ((end - start).days)):
            date_range.add(start + timedelta(n)) 

    elif timeline == 'month':

        end = start.replace(month=start.month + 1)

        start_times = []

        while start < end:
            start_times.append(start)
            print(start_times)
            if start.minute == 45:
                start.replace(hour=start.hour +1, minute=0)
                print("if", start)
            elif start.minute < 45:
                break
            else:
                start = start.replace(minute=start.minute+15)
                print("else", start)

        print(start_times)

    elif timeline == 'six months':
        end = start + timedelta(days=180)
        when = (start, end)

    elif timeline == 'year':
        end = start + timedelta(days=365)
        when = (start, end)


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
