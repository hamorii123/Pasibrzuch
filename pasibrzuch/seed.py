import json

from app import app
from models import db, User, Restaurant, Table


with app.app_context():

    # Wyczyść stare dane
    Table.query.delete()
    User.query.delete()
    Restaurant.query.delete()

    # ---------- USERS ----------

    users = [
        User(
            id=1,
            name='Jan Kowalski',
            email='klient@example.com',
            password='klient123',
            role='client'
        ),

        User(
            id=2,
            name='Anna Nowak',
            email='kelner@example.com',
            password='kelner123',
            role='waiter',
            restaurant_id=1
        ),

        User(
            id=3,
            name='Piotr Wiśniewski',
            email='manager@example.com',
            password='manager123',
            role='manager'
        ),

        User(
            id=4,
            name='Michał Kowalczyk',
            email='kelner2@example.com',
            password='kelner123',
            role='waiter',
            restaurant_id=2
        )
    ]

    db.session.add_all(users)

    # ---------- RESTAURANTS ----------

    restaurant1 = Restaurant(
        id=1,
        name='13 Muz',
        address='ul. Restauracyjna 13, Szczecin',
        rating=4.7,
        cuisine='Polska',
        delivery=True,
        reservation=True,
        opening_hours='12:00-22:00',
        delivery_time='30-45 min',

    )

    restaurant2 = Restaurant(
        id=2,
        name='La Bella Italia',
        address='ul. Włoska 5, Szczecin',
        rating=4.5,
        cuisine='Włoska',
        delivery=True,
        reservation=True,
        opening_hours='11:00-23:00',
        delivery_time='25-40 min',
    )

    db.session.add(restaurant1)
    db.session.add(restaurant2)

    tables = [

        # =========================
        # RESTAURANT 1 - 13 Muz
        # =========================

        Table(
            id=1,
            restaurant_id=1,
            number='1',
            seats=2,
            status='free',
            location='Przy oknie',

            x=100,
            y=100,

            shape='rectangle',

            width=80,
            height=120,

            rotation=0
        ),

        Table(
            id=2,
            restaurant_id=1,
            number='2',
            seats=4,
            status='occupied',
            location='Centrum sali',

            x=250,
            y=150,

            shape='circle',

            radius=60,

            rotation=45
        ),

        Table(
            id=3,
            restaurant_id=1,
            number='3',
            seats=2,
            status='free',
            location='Przy wejściu',

            x=450,
            y=200,

            shape='rectangle',

            width=100,
            height=80,

            rotation=0
        ),

        Table(
            id=4,
            restaurant_id=1,
            number='4',
            seats=6,
            status='reserved',
            location='Centrum sali',

            x=650,
            y=300,

            shape='circle',

            radius=70,

            rotation=90
        ),

        Table(
            id=5,
            restaurant_id=1,
            number='5',
            seats=2,
            status='cleaning',
            location='Przy barze',

            x=300,
            y=400,

            shape='rectangle',

            width=120,
            height=80,

            rotation=0
        ),

        Table(
            id=6,
            restaurant_id=1,
            number='6',
            seats=4,
            status='occupied',
            location='Przy oknie',

            x=500,
            y=450,

            shape='circle',

            radius=50,

            rotation=30
        ),

        Table(
            id=7,
            restaurant_id=1,
            number='7',
            seats=8,
            status='free',
            location='VIP',

            x=100,
            y=500,

            shape='rectangle',

            width=150,
            height=100,

            rotation=0
        ),

        Table(
            id=8,
            restaurant_id=1,
            number='8',
            seats=4,
            status='reserved',
            location='Przy kominku',

            x=700,
            y=100,

            shape='circle',

            radius=40,

            rotation=0
        ),

        # =========================
        # RESTAURANT 2 - La Bella Italia
        # =========================

        Table(
            id=9,
            restaurant_id=2,
            number='1',
            seats=4,
            status='free',
            location='Taras',

            x=150,
            y=150,

            shape='rectangle',

            width=90,
            height=140,

            rotation=0
        ),

        Table(
            id=10,
            restaurant_id=2,
            number='2',
            seats=6,
            status='occupied',
            location='Centrum',

            x=350,
            y=200,

            shape='circle',

            radius=65,

            rotation=0
        ),

        Table(
            id=11,
            restaurant_id=2,
            number='3',
            seats=2,
            status='free',
            location='Przy kuchni',

            x=550,
            y=250,

            shape='rectangle',

            width=110,
            height=90,

            rotation=0
        ),

        Table(
            id=12,
            restaurant_id=2,
            number='4',
            seats=8,
            status='reserved',
            location='VIP',

            x=750,
            y=350,

            shape='circle',

            radius=75,

            rotation=0
        )
    ]

    db.session.add_all(tables)

    db.session.commit()

    print("Baza została wypełniona.")