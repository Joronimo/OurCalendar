import sqlalchemy 

from faker import Faker
from model import connect_to_db, db, User, Event
from server import app
import random

import datetime

fake = Faker()


def seed():
    """seed ten users and ten events"""

    for i in range(10):
        hour = random.randrange(0,23)
        u_id = random.randrange(1,10)
        
        u = User(email=fake.email(), 
                 password='ab12', 
                 username=fake.name())
        e = Event(activate=True, 
                  start_time=datetime.datetime(2018, 10, 26, hour, 00, 00), 
                  end_time=datetime.datetime(2018, 10, 26, hour, 30, 00),
                  user_id=u_id)

        db.session.add_all([e, u])
    db.session.commit()



if __name__ == "__main__":
    connect_to_db(app)

seed()