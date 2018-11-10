"""Calendar Events."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session,
                   Markup)
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Event, Invited

from datetime import timedelta, datetime, date

import calendar

from ast import literal_eval



app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined

@app.route("/", methods=["GET", "POST"])
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


@app.route("/invite")
def create_invite():
    """Allows logged in user to create and send an invite to guests to attend an event."""

    return render_template("invite.html")

@app.route("/invitation", methods=["POST"])
def find_event_send_invitation():
    """Create event and invitations to event with suggested event time, based on user inputs and prioirity users' schedule."""


    def get_user_objects_from_priority_users_list(p_users_list):
        """ by inputing the list of users for an event, this will clean the list 
            and return a new list of user objects per user. Or return an error 
            if the host input a name in an error.""" 
        user_objects = []
       # convert user's email/username into a user object stored in user_object list
        for a in p_users_list:
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

        return user_objects

    def get_events_from_user_objects(u_objs):
        """ using the list of user objects, create a list of tuples where the
            start and end tuple is the duration of each event."""

        all_events = []
        # get all events for every user object and add event start and end times 
        # to list all_events
        for user in u_objs:
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

        return all_events

    def get_start_time():
        """ rounds up the current time to the nearest quarter hour"""

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

    def get_listed_timeline_intervals_of_qtr_hr(timeline):
        """ using the timeline input by user, break that down into quarter hour 
            intervals and place each into a list. This list will be used for the 
            "start times" of the suggested time, tuple."""

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

        return start_times

    def get_all_time_in_range_from_duration(duration):
        """ accounting for the length of the meeting == duration. And accounting
            for the time of day the host would like the meeting to take place.
            Return a list of times the meeting is able to take place."""

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

        return all_time_in_range

    def suggeted_event_time(possible_events_list):

        ## Compare all_events to times_in_range and suggest first time not 
        #  in times_in_range and not in all_events

        available_times = []

        for event in all_events:
            for time in possible_events_list:
                if event[1] < time[0]:
                    available_times.append((time[0],time[1]))      
                else:
                    if time[0] < event[0] or time[0] < event[1]:
                        if time[1] <event[0] or time[1] < event[1]:
                            available_times.append((time[0],time[1]))

        suggested_event_time = available_times[0]

        return suggested_event_time

    def send_invites(user_objs_list, invitees, event):

        # add to invites table

        # user_objects at the top of function. Priority users.
        for invitee in user_objs_list:

            new_invite = Invited(user_id=invitee.id,
                            event_id=event.id,
                            is_priority=True
                            )

            db.session.add(new_invite)
            db.session.commit()


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

    # get emails and usernames from invite.html  
    priority_users = request.form.get("priority_users").split(",")

    user_objects = get_user_objects_from_priority_users_list(priority_users)

    all_events = get_events_from_user_objects(user_objects)

    start = get_start_time()

    # how soon event should take place  
    timeline = request.form["timeline"]

    start_times = get_listed_timeline_intervals_of_qtr_hr(timeline)

    # get intended duration of event
    duration = request.form["duration"]

    all_time_in_range = get_all_time_in_range_from_duration(duration)

    suggested_event_time = suggested_event_time(all_time_in_range)
    
    event_name = request.form["event name"]
    event_description = request.form["description"]

    # add event to Event table, as a deactivated event.
    event = Event(host=session["user_id"], 
                  name=event_name, 
                  description=event_description,
                  start_time=suggested_event_time[0],
                  end_time=suggested_event_time[1],
                  timeline=timeline,
                  duration=duration
                  )
    db.session.add(event)
    db.session.commit()

    invitees = request.form.get("invitees").split(',')

    send_invites(user_objects, invites, event)


@app.route('/inbox')
def notifications():
    """
       Render invitation if user has an unanswered invitation or send them to 
       the mainpage if not.
    """
    invites = Invited.query.filter_by(user_id=session["user_id"]).all()

    for i in invites:
        if i.is_declined == False and i.is_accepted == False:
                #get event info with i.id
                event = Event.query.filter_by(id=i.event_id).first()
                name = event.name
                description = event.description
                start = event.start_time.strftime("%A, the %d of %B, %Y. Starting at %I:%M%p")
                end = event.end_time.strftime("%A, the %d of %B, %Y. Ending at %I:%M%p")
                e_id = event.id
                return render_template("invitation.html", 
                                       event_name=name, 
                                       event_description=description,
                                       start_time=start,
                                       end_time=end,
                                       event_id=e_id
                                       )

    message = Markup("You have no invitations at this time.")
    flash(message)
    return render_template("homepage.html")



@app.route("/process-invitation", methods=["POST"])
def process_invitation():
    """process user input (accept or decline) of event invititation"""
    
    responce = request.form.get('attend')
    e_id = request.form.get("event_id")

    #handling the responce
    if responce == None:
        message = Markup("Please mark either attend or decline.")
        flash(message)
        return render_template("invitation.html")
    elif responce == "yes":
        #get all invites for this event
        invite_objs = Invited.query.filter_by(event_id=e_id).all()
        #all priority user ids for the event
        event_user_objs = []
        count_prioirty_users = 0
        for i in invite_objs:
            #if Invited user is session user
            if i.user_id == session["user_id"]:
                i.is_accepted = True
                db.session.commit()

            if i.is_priority == True:
                event_user_objs.append(i.user_id)
                for user in event_user_objs:
                    if i.user_id == user:
                        #count if each priority user has accepted the invite
                        if i.is_priority == True and i.is_accepted == True:
                            count_prioirty_users += 1
                            #if all priority user's have accepted change the 
                            #event status to active
                            if count_prioirty_users == len(event_user_objs):
                                event = Event.query.filter_by(id=e_id).first()
                                event.is_active = True
                                db.session.commit()

    elif responce == "no":
        #get all invites for this event
        invite_objs = Invited.query.filter_by(event_id=e_id).all()

        inv_ids = [invite.id for invite in invite_objs]

        for i in invite_objs:
            if i.user_id == session['user_id']:
                if i.is_priority == True:
                    start_time = request.form.get("start_time")
                    end_time = request.form.get("end_time")
                    return render_template("priority.html", 
                                            event_id=e_id,
                                            inv_ids=inv_ids,
                                            start_time=start_time,
                                            end_time=end_time
                                          )
                # ask user if she would like to be removed as priority user to
                # let event continue without her/him. Or look for a new time for
                # the event to take place.
                # if new event time ->
                # -> cancel event and invites
                # -> make a new event with same host and suggested_time[1]
                # -> send new invites. 
    

    message = Markup("You made it")
    flash(message)
    return render_template("homepage.html")

@app.route("/assess-priority", methods=["POST"])
def priority_user_declined_invite():
    """assessesing the reson why a priority user delined an invite and 
       responding accordingly."""

    #get event id from form.
    e_id = request.form.get("event_id")

    # get event obj
    e_obj = Event.query.filter_by(id=e_id).first()
    print("aaaaaaaaaaaaaa", e_id)
    #get list of all Invited objects (all invites related to event). 
    invite_ids = request.form.get("inv_ids")
    print("AHHHHHH", invite_ids)



    # FIIIIIIIIXXXXXX invites ids/objs omg



    le = literal_eval(invite_ids)
    print(le)

    #why'd you decline bro?
    reason = request.form.get("reason")
    print(reason)

    invite_objs = [Invited.query.get(inv_id) for inv_id in invite_ids]

    if reason == "new_time":
        p_users = []
        non_p_users = []

        for i in invite_objs:
            i = i[1,-1]
            print(i)
            if i.is_priority == True:
                p_users.append(i) 
            elif i.is_priority == False:
                non_p_users.append(i) 

        user_objects = get_user_objects_from_priority_users_list(p_users)

        all_events = get_events_from_user_objects(user_objects)

        # ensure the event time that is declined is added to event list so, the 
        # user doesn't run into the same issue.
        all_events.append((e_obj.start_time, e_obj.end_time))

        start = get_start_time()
        print(start)

        timeline = e_obj.timeline
        print(timeline)

        start_times = get_listed_timeline_intervals_of_qtr_hr(timeline)

        # get intended duration of event
        duration = e_obj.duration

        all_time_in_range = get_all_time_in_range_from_duration(duration)

        suggested_event_time = suggested_event_time(all_time_in_range)

        name = e_obj.name
        description = e_obj.description
        host = e_obj.host

        # add event to Event table, as a deactivated event.
        event = Event(host=session["user_id"], 
                      name=name, 
                      description=description,
                      start_time=suggested_event_time[0],
                      end_time=suggested_event_time[1],
                      timeline=timeline,
                      duration=duration
                      )
        db.session.add(event)
        db.session.commit()

        send_invites(user_objects, non_p_users, event)

        #delete depricated event and invites.
        Invited.delete().where(event_id=e_obj.id)
        Event.delete().where(id=e_obj.id)
        db.session.commit()

    elif reason == "not_priority":
        for i in inv_objs:
                if i.user_id == session['user_id']:
                    if i.is_priority == True:
                        i.is_priority = False
                        i.is_declined = True
                        db.session.commit()
    else:
        message = Markup("You must select one of the options")
        flash(message)                      
        return render_template("priority.html")    

    message = Markup("decline prcessed")
    flash(message)                      
    return render_template("homepage.html")




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
