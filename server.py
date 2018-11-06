"""Calendar Events."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session,
                   Markup)
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Event, Invited

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

    is_user = User.query.filter_by(email=email).first()

    if is_user:
        if is_user.password == password:
            # activate session with user id set to variable
            session["user_id"] = is_user.id
            # welcome user by name
            name = is_user.name
            message = Markup(f"Welcome back, {name}.")
            flash(message)
            return render_template("homepage.html")
        else:
            message = Markup("password incorrect.")
            flash(message)
            return render_template("login.html")
    else:
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

    check_email = User.query.filter_by(email=email).first()

    if check_email == None:
        user = User(email=email, password=password, username=username)
        db.session.add(user)
        db.session.commit()
        #activate session with user id set to variable 
        session["user_id"] = user.id

        message = Markup("You are now registered!")
        flash(message)
        return render_template("homepage.html")
    else:
        message = Markup("This email already exists in our database. Please, log in.")
        flash(message)
        return render_template("login.html")


@app.route('/inbox')
def notifications():
    """Event invite notifications."""


    return render_template("inbox.html")

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
    """Create event and invitations to event with suggested event time, based on user inputs and prioirity users' schedule."""

    # get emails and usernames from invite.html  
    priority_users = request.form.get("priority_users").split(',')

    user_objects = []
   # convert user's email/username into a user object stored in user_object list
    for a in priority_users:
        a = a.replace(" ", "")
        if "@" in a:   
            user = User.query.filter_by(email=a).first()
            user_objects.append(user)
        else:
            user = User.query.filter_by(username=a).first()
            user_objects.append(user)


    # if the request.form returns incorrect user data ie. typo, this should 
    # catch it and return an error, so the user can adjust accordingly.
    if None in user_objects:
        message = Markup("A username or email does not exist, please check the data and try again.")
        flash(message)
        return render_template("invite.html")

    # start and end dates of each event priority users are invited to and havent
    # declined.
    all_events = []
    #get all events for every user object and add event ids to list all_events
    for user in user_objects:
        invited_event_ids = []
        user_invites = Invited.query.filter_by(user_id=user.id).all()

        for ui in user_invites:
            if ui.is_declined == False:
                invited_event_ids.append(ui.event_id)

            #add each event start and end times to the set 'all_events'
            for e_id in invited_event_ids:
                # using same event_id from Invited table to get content from 
                # Event table
                event = Event.query.filter_by(id=e_id).first()
                tup_of_event = (event.start_time, event.end_time)
                all_events.append(tup_of_event)

    # get timeline start and end   
    timeline = request.form["timeline"]

   # set time to quarter hour intervals 
    def get_start_time():
        """gets start time rounded up to the nearest quarter hour starting at now()"""

        start = datetime.now()
        start = start.replace(second=0, microsecond=0)

        if start.minute > 45:
            if start.hour == 23:
                start = start + timedelta(days=1)
                start = start.replace(hour=0, minute=0)
                return start
            else:
                start = start.replace(hour=start.hour+1, minute=0)
                return start
        elif 0 < start.minute < 15:
            start = start.replace(minute=15)
            return start
        elif 15 < start.minute < 30:
            start = start.replace(minute=30)
            return start
        elif 30 < start.minute < 45:
            start = start.replace(minute=45)
            return start
        else:
            return start

    start = get_start_time()

    # add time to list start_times, for use in comparison with user events. 
    if timeline == 'two weeks':

        end = start + timedelta(days=14)
        start_times = []

        while start < end:
            start_times.append(start)
            if start.minute == 45:
                start = start + timedelta(hours=1)
                start = start.replace(minute=0)
            else:
                start = start + timedelta(minutes=15)


    elif timeline == 'month':

        end = start + timedelta(days=30)
        start_times = []

        while start < end:
            start_times.append(start)
            if start.minute == 45:
                start = start + timedelta(hours=1)
                start = start.replace(minute=0)
            else:
                start = start + timedelta(minutes=15)

    elif timeline == 'six months':
        end = start + timedelta(days=180)
        start_times = []

        while start < end:
            start_times.append(start)
            if start.minute == 45:
                start = start + timedelta(hours=1)
                start = start.replace(minute=0)
            else:
                start = start + timedelta(minutes=15)

    elif timeline == 'year':
        end = start + timedelta(days=365)
        start_times = []

        while start < end:
            start_times.append(start)
            if start.minute == 45:
                start = start + timedelta(hours=1)
                start = start.replace(minute=0)
            else:
                start = start + timedelta(minutes=15) 


    # get intended duration of event

    duration = request.form["duration"]

    if duration == '15':
        duration = timedelta(minutes=15)
    elif duration == '30':
        duration = timedelta(minutes=30)
    elif duration == '1':
        duration = timedelta(hours=1)
    elif duration == '2':
        duration = timedelta(hours=2)
    elif duration == '3':
        duration = timedelta(hours=3)
    elif duration == '4':
        duration = timedelta(hours=4)
    elif duration == '5':
        duration = timedelta(hours=5)
    elif duration == '6':
        duration = timedelta(hours=6)
    elif duration == '7':
        duration = timedelta(hours=7)
    elif duration == '8':
        duration = timedelta(hours=8)

    ## create list of dates within timeline range (start_times) at 15 min intervals for start time
    #  end times = start + duration (user input)  
    
    all_time_in_range = []
 
    for i in start_times:
        all_time_in_range.append((i, i + duration))

    ## remove all_time outside of user input time of day

    no_earlier = request.form["no earlier than"]
    no_later = request.form["no later than"]

    all_time_in_range = [(dt, dt2) for dt, dt2 in all_time_in_range 
                          if dt.hour > int(no_earlier) and dt2.hour < int(no_later)]

    ## Compare all_events to times_in_range and suggest first time not 
    #  in times_in_range and not in all_events

    available_times = []

    for event in all_events:
        for time in all_time_in_range:
            if event[1] < time[0]:
                available_times.append((time[0],time[1]))      
            else:
                if time[0] < event[0] or time[0] < event[1]:
                    if time[1] <event[0] or time[1] < event[1]:
                        available_times.append((time[0],time[1]))

    suggested_event_time = available_times[0]
    suggested_start = suggested_event_time[0].strftime("%A, the %d of %B, %Y. Starting at %I:%M%p")
    suggested_end = suggested_event_time[1].strftime("%A, the %d of %B, %Y. Ending at %I:%M%p")

    event_name = request.form["event name"]
    event_description = request.form["description"]

    # add to event table as a deactivated event.
    event = Event(host=session["user_id"], 
                  name=event_name, 
                  description=event_description,
                  start_time=suggested_event_time[0],
                  end_time=suggested_event_time[1]
                  )
    db.session.add(event)
    db.session.commit()

    # add to invites table

    # user_objects at the top of function. Priority users.
    for invitee in user_objects:

        new_invite = Invited(user_id=invitee.id,
                        event_id=event.id,
                        is_priority=True
                        )

        db.session.add(new_invite)
        db.session.commit()


    invitees = request.form.get("invitees").split(',')


    invited = []

    # convert user's email or username into user's id 
    for i in invitees:
        i = i.replace(" ", "")
        if "@" in i:   
            user = User.query.filter_by(email=i).first()
            invited.append(user.id)
        else:
            user = User.query.filter_by(username=i).first()
            invited.append(user.id)

    for i in invited:
        invite = Invited(user_id=i,
                        event_id=event.id)
        db.session.add(invite)
        db.session.commit()

    #add invite to host's invited collumn and event render
    host = session["user_id"]
    host_invite = Invited(user_id=host,
                              event_id=event.id,
                              is_priority=True,
                              is_accepted=True)
    db.session.add(host_invite)
    db.session.commit()

    message = Markup("Your invitations have been sent and the event has been added to your calendar.")
    flash(message)
    return render_template("homepage.html")


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
