"""Model and database functions for OurCalendar project"""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()

import datetime
import calendar



##############################################################################
# Model definitions

class User(db.Model):
    """User of website."""

    __tablename__ = "users"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=True)
    username = db.Column(db.String(64), unique=True, nullable=False)

    # ensure username and email are unique when registering before adding to the table. 
    # Doesn't just throw them to login page.
    # __table_args__ = (UniqueConstraint('email', 'username'))


    def __repr__(self):
        """provide helpful representation when printed"""

        return f"<User user_id={self.id} email={self.email}>"

# events_invites = db.Table('events_guests', db.metadata,
#     db.Column('event_id', db.Integer, db.ForeignKey('events.id')), 
#     db.Column('invite_id', db.Integer, db.ForeignKey('invites.id')),
#     )

#table ties event id with user id. an event can have many users, one user can have many events. 
user_events = db.Table('user_events',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('event_id', db.Integer, db.ForeignKey('events.id'))
)

class Event(db.Model):
    """event of calendar website."""

    __tablename__ = "events"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # host_id = db.Column(db.Integer, db.ForeignKey('users.id'))  
    activate = db.Column(db.Boolean, default=False)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)

    user_events = db.relationship('User', secondary=user_events, lazy='subquery',
        backref=db.backref('ue', lazy=True))
    # e_type = db.Column(db.String(64), nullable=True)

    # user = db.relationship("User", backref=db.backref("events",
    #                                                   order_by=id))


    def __repr__(self):
        """provide helpful representation when printed"""

        return f"<Event id={self.id} date={self.date}>"




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
    db.create_all()
    print("Connected to DB.")