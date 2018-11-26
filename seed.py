
from faker import Faker
from model import connect_to_db, db, User, Event, Invited
from server import app
import random

import datetime

fake = Faker()


def seed():
    """seed ten users and ten events"""

    for _ in range(1,30):
        hour = random.randrange(0,23)
        day = random.randrange(3,29)

        u = User(email=fake.email(), 
               password='ab12', 
               username=fake.user_name(),
               name=fake.name())
        db.session.add(u)
        db.session.commit()

        e = Event(is_active=True, 
                name='1:1 me + thoughts',
                start_time=datetime.datetime(2018, 11, day, hour, 00, 00), 
                end_time=datetime.datetime(2018, 11, day, hour, 30, 00),
                description="meeting with my thoughts",
                host=u.id)
        db.session.add(e)
        db.session.commit()

        ee = Invited(user_id=u.id, event_id=e.id, is_accepted=True, is_priority=True)
        db.session.add(ee)
        db.session.commit()

    # for user in User.query.all()


if __name__ == "__main__":
    connect_to_db(app)
    seed()