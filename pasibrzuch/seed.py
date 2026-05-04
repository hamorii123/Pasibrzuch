import json

from app import app
from models import db, User, Restaurant


with app.app_context():

    # Wyczyść stare dane
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
        floor_plan=json.dumps({
            'width': 800,
            'height': 600,
            'background_color': '#f8f9fa',

            'tables': [
                {
                    'id': 1,
                    'x': 100,
                    'y': 100,
                    'rotation': 0,
                    'shape': 'rectangle',
                    'width': 80,
                    'height': 120
                },

                {
                    'id': 2,
                    'x': 250,
                    'y': 150,
                    'rotation': 45,
                    'shape': 'circle',
                    'radius': 60
                },

                {
                    'id': 3,
                    'x': 450,
                    'y': 200,
                    'rotation': 0,
                    'shape': 'rectangle',
                    'width': 100,
                    'height': 80
                },

                {
                    'id': 4,
                    'x': 650,
                    'y': 300,
                    'rotation': 90,
                    'shape': 'circle',
                    'radius': 70
                },

                {
                    'id': 5,
                    'x': 300,
                    'y': 400,
                    'rotation': 0,
                    'shape': 'rectangle',
                    'width': 120,
                    'height': 80
                },

                {
                    'id': 6,
                    'x': 500,
                    'y': 450,
                    'rotation': 30,
                    'shape': 'circle',
                    'radius': 50
                },

                {
                    'id': 7,
                    'x': 100,
                    'y': 500,
                    'rotation': 0,
                    'shape': 'rectangle',
                    'width': 150,
                    'height': 100
                },

                {
                    'id': 8,
                    'x': 700,
                    'y': 100,
                    'rotation': 0,
                    'shape': 'circle',
                    'radius': 40
                }
            ]
        })
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
        floor_plan = json.dumps({
        'width': 900,
        'height': 700,
        'background_color': '#fff5e6',
        'tables': [
            {'id': 9, 'x': 150, 'y': 150, 'rotation': 0, 'shape': 'rectangle', 'width': 90, 'height': 140},
            {'id': 10, 'x': 350, 'y': 200, 'rotation': 0, 'shape': 'circle', 'radius': 65},
            {'id': 11, 'x': 550, 'y': 250, 'rotation': 0, 'shape': 'rectangle', 'width': 110, 'height': 90},
            {'id': 12, 'x': 750, 'y': 350, 'rotation': 0, 'shape': 'circle', 'radius': 75}
        ]
        })
    )

    db.session.add(restaurant1)
    db.session.add(restaurant2)

    db.session.commit()

    print("Baza została wypełniona.")