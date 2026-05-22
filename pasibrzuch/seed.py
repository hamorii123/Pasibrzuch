import os
import json
from datetime import date, time

from app import app
from models import db, User, Restaurant, Table, Reservation, MenuItem

# db_path = os.path.join(app.root_path, 'instance', 'app.db')
# if os.path.exists(db_path):
#     os.remove(db_path)
#     print("Stary plik bazy danych został usunięty.")

with app.app_context():

    # db.drop_all()
    # db.create_all()
    # print("Tabele bazy danych zostały utworzone na nowo.")

    # ---------- 1. RESTAURANTS ----------
    # Dodajemy je na samym początku, bo użytkownicy, stoliki i menu ich potrzebują!
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

    # Commitujemy restauracje, aby zapisały się w bazie i ich ID były ważne dla kolejnych kroków
    db.session.commit()

    # ---------- 2. USERS ----------
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
            restaurant_id=1  # Teraz restauracja id=1 już istnieje, więc przejdzie gładko!
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
            restaurant_id=2  # Restauracja id=2 również istnieje
        )
    ]

    db.session.add_all(users)

    # ---------- 3. TABLES ----------
    tables = [
        Table(id=1, restaurant_id=1, number='1', seats=2, status='free', location='Przy oknie', x=100, y=100,
              shape='rectangle', width=80, height=120, rotation=0),
        Table(id=2, restaurant_id=1, number='2', seats=4, status='occupied', location='Centrum sali', x=250, y=150,
              shape='circle', radius=60, rotation=45),
        Table(id=3, restaurant_id=1, number='3', seats=2, status='free', location='Przy wejściu', x=450, y=200,
              shape='rectangle', width=100, height=80, rotation=0),
        Table(id=4, restaurant_id=1, number='4', seats=6, status='reserved', location='Centrum sali', x=650, y=300,
              shape='circle', radius=70, rotation=90),
        Table(id=5, restaurant_id=1, number='5', seats=2, status='cleaning', location='Przy barze', x=300, y=400,
              shape='rectangle', width=120, height=80, rotation=0),
        Table(id=6, restaurant_id=1, number='6', seats=4, status='occupied', location='Przy oknie', x=500, y=450,
              shape='circle', radius=50, rotation=30),
        Table(id=7, restaurant_id=1, number='7', seats=8, status='free', location='VIP', x=100, y=500,
              shape='rectangle', width=150, height=100, rotation=0),
        Table(id=8, restaurant_id=1, number='8', seats=4, status='reserved', location='Przy kominku', x=700, y=100,
              shape='circle', radius=40, rotation=0),

        Table(id=9, restaurant_id=2, number='1', seats=4, status='free', location='Taras', x=150, y=150,
              shape='rectangle', width=90, height=140, rotation=0),
        Table(id=10, restaurant_id=2, number='2', seats=6, status='occupied', location='Centrum', x=350, y=200,
              shape='circle', radius=65, rotation=0),
        Table(id=11, restaurant_id=2, number='3', seats=2, status='free', location='Przy kuchni', x=550, y=250,
              shape='rectangle', width=110, height=90, rotation=0),
        Table(id=12, restaurant_id=2, number='4', seats=8, status='reserved', location='VIP', x=750, y=350,
              shape='circle', radius=75, rotation=0),
    ]

    db.session.add_all(tables)
    db.session.commit()

    # ---------- 4. MENU ITEMS ----------
    menu_items = [
        MenuItem(restaurant_id=1, name='Pierogi ruskie', price=28.0, category='Dania główne',
                 description='Z cebulką i śmietaną'),
        MenuItem(restaurant_id=1, name='Żurek', price=18.0, category='Zupy', description='Tradycyjny polski żurek'),
        MenuItem(restaurant_id=1, name='Schabowy', price=42.0, category='Dania główne',
                 description='Ziemniaki + kapusta'),

        MenuItem(restaurant_id=2, name='Pizza Margherita', price=35.0, category='Pizza',
                 description='Sos, mozzarella, bazylia'),
        MenuItem(restaurant_id=2, name='Pasta Carbonara', price=39.0, category='Makarony',
                 description='Boczek, jajko, parmezan'),
        MenuItem(restaurant_id=2, name='Tiramisu', price=22.0, category='Desery', description='Klasyczny włoski deser')
    ]

    db.session.add_all(menu_items)
    db.session.commit()

    # ---------- 5. RESERVATIONS ----------
    reservations = [
        Reservation(
            user_id=1,
            restaurant_id=1,
            table_id=2,
            date=date(2026, 5, 6),
            time=time(18, 0),
            people=2,
            status='confirmed',
            notes='Urodziny'
        ),
        Reservation(
            user_id=1,
            restaurant_id=1,
            table_id=4,
            date=date(2026, 5, 6),
            time=time(19, 0),
            people=4,
            status='pending',
            notes='Randka'
        ),
        Reservation(
            user_id=1,
            restaurant_id=2,
            table_id=10,
            date=date(2026, 5, 7),
            time=time(20, 30),
            people=3,
            status='confirmed',
            notes='Biznesowe spotkanie'
        )
    ]

    db.session.add_all(reservations)
    db.session.commit()

    print("Baza została pomyślnie oczyszczona i wypełniona nowymi danymi.")