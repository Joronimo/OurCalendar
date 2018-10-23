"""Model and database functions for OurCalendar project"""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()

##############################################################################
# Model definitions

class User(db.Model):
    """User of ratings website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)

    def __repr__(self):
        """provide helpful representation when printed"""

        return f"<User user_id={self.user_id} email={self.email}>"

class Event(db.Model):
    """User of ratings website."""

    __tablename__ = "events"

    event_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    host = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)

    def __repr__(self):
        """provide helpful representation when printed"""

        return f"<User user_id={self.user_id} email={self.email}>"

class Invite(db.Model): 
    """Movie ratings  by user"""

    __tablename__ = "invites"

    invite_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    accepted = db.Column(db.Boolean, nullable=True)

    user = db.relationship("User", backref=db.backref("invites",
                                                      order_by=invite_id))

    event = db.relationship("Event", backref=db.backref("invites",
                                                        order_by=invite_id))

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
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ratings'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")