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
    name = db.Column(db.String(64), nullable=True)
    events = db.relationship("Invited", back_populates="user")

    # ensure username and email are unique when registering before adding to the table. 
    # Doesn't just throw them to login page.
    # __table_args__ = (UniqueConstraint('email', 'username'))


    def __repr__(self):
        """provide helpful representation when printed"""

        return f"<User(id={self.id})>"

class Invited(db.Model):
    """list of invitees and priority of invitee."""

    __tablename__ = "invites"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), primary_key=True)
    is_accepted = db.Column(db.Boolean, default=False)
    is_declined = db.Column(db.Boolean, default=False)
    is_priority = db.Column(db.Boolean, default=False)
    user = db.relationship("User", back_populates="events")
    event = db.relationship("Event", back_populates="users")

    def __repr__(self):
        """provide helpful representation when printed"""

        return f"<Invited(id={self.id})>"
 

class Event(db.Model):
    """event of calendar website."""
 
    __tablename__ = "events"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    host = db.Column(db.Integer, db.ForeignKey('users.id'))  
    is_active = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(64), nullable=True)
    description = db.Column(db.String(360), nullable=True)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    timeline = db.Column(db.String(86), nullable=True)
    duration = db.Column(db.String(86), nullable=True)
    ealier = db.Column(db.String(86), nullable=True)
    later = db.Column(db.String(86), nullable=True)
    users = db.relationship("Invited", back_populates="event")

    def __repr__(self):
        """provide helpful representation when printed"""

        return f"<Event(id={self.id})>"

#table ties event id with user id. One event can have many users and one user can have many events. 

# user_events = db.Table('user_events',
#     db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
#     db.Column('event_id', db.Integer, db.ForeignKey('events.id')))

    




##############################################################################
# Helper functions-

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cal'
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