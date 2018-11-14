def example_data():
    """Create some sample data."""

    # In case this is run more than once, empty out existing data
    User.query.delete()
    Invited.query.delete()
    Event.query.delete()

    # Add sample employees and departments
    u1 = User(id=1, email="soemthing@gmail.com", password="ab12", username="marry21", name="marry johnson")
    u2 = User(id=2, email="boom@gmail.com", password="ab12", username="sara23", name="sara johnson")
    u3 = User(id=3, email="heyyyy@gmail.com", password="ab12", username="kilie", name="kilie johnson")

    e1 = Event(id=1, host=1, is_active=False, name= "event1", description="event is happening",
               start_time="2018-11-14 19:00:00", end_time="2018-11-14 20:00:00", timeline="two weeks",
               duration=1, ealier=18, later=22
               )
    e2 = Event(id=2, host=2, is_active=False, name= "event2", description="event is happening",
               start_time="2018-11-15 19:00:00", end_time="2018-11-15 20:00:00", timeline="two weeks",
               duration=1, ealier=18, later=22
               ) 
    e3 = Event(id=2, host=3, is_active=False, name= "event3", description="event is happening",
               start_time="2018-11-16 19:00:00", end_time="2018-11-16 20:00:00", timeline="two weeks",
               duration=1, ealier=18, later=22
               )

    iu1 = Invited(id=1, user_id=1, event_id=1, is_accepted=True, is_declined=False, is_priority=True
               )
    iu2 = Invited(id=2, user_id=1, event_id=2, is_accepted=False, is_declined=False, is_priority=False
               ) 
    iu3 = Invited(id=2, user_id=1, event_id=3, is_accepted=False, is_declined=False, is_priority=True 
               )
    iu4 = Invited(id=4, user_id=2, event_id=1, is_accepted=False, is_declined=False, is_priority=True
               )
    iu5 = Invited(id=5, user_id=2, event_id=2, is_accepted=True, is_declined=False, is_priority=True
               ) 
    iu6 = Invited(id=6, user_id=2, event_id=3, is_accepted=False, is_declined=False, is_priority=False 
               )
    iu7 = Invited(id=7, user_id=3, event_id=1, is_accepted=False, is_declined=False, is_priority=False
               )
    iu8 = Invited(id=8, user_id=3, event_id=2, is_accepted=False, is_declined=False, is_priority=True
               ) 
    iu9 = Invited(id=9, user_id=3, event_id=3, is_accepted=True, is_declined=False, is_priority=True 
               )


    db.session.add_all([u1, u2, u3, e1, e2, e3, iu1, iu2, iu3, iu4, iu5, iu6, iu7, iu8, iu9])
    db.session.commit()


