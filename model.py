"""Model and database functions for OurCalendar project"""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()

import datetime



##############################################################################
# Model definitions

class User(db.Model):
    """User of website."""

    __tablename__ = "users"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)

    def __repr__(self):
        """provide helpful representation when printed"""

        return f"<User user_id={self.user_id} email={self.email}>"


#table ties event id with invite id. One invite per guest, per event. 

# events_invites = db.Table('events_guests', db.metadata,
#     db.Column('event_id', db.Integer, db.ForeignKey('events.id')), 
#     db.Column('invite_id', db.Integer, db.ForeignKey('invites.id')),
#     )


class Event(db.Model):
    """event of calendar website."""

    __tablename__ = "events"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    host_id = db.Column(db.Integer, db.ForeignKey('users.id'))  
    activate = db.Column(db.Boolean, default=False)
    date = db.Column(db.DateTime)

    invites = db.relationship("Invite", backref="events")
    guests = db.relationship("User", secondary='invites', backref="events")


    def invite_guests(self, users_list):
        
        for user in users_list:
            #find user. query on email address. If email is registered = ok, if not, invite user to app.
            #create invitation for user, with acceptance button of event.
            pass

    def __repr__(self):
        """provide helpful representation when printed"""

        return f"<User user_id={self.user_id} email={self.email}>"


class Invite(db.Model): 
    """Invite user to event"""

    __tablename__ = "invites"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date = db.Column(db.DateTime)    
    accepted = db.Column(db.Boolean, default=False)

    def __repr__(self):
        """provide helpful representation when printed"""

        return f"<Rating ivite_id={self.invite_id}, \
                         event_id={self.event_id}, \
                         user_id={self.user_id}, \
                         accepted={self.accepted}>"

##############################################################################
# Helper functions-

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///calendar'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # run this module interactively and it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")