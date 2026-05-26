from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.String(200), nullable=False)

    role = db.Column(db.String(20), nullable=False)

    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=True)

    restaurant = db.relationship('Restaurant', backref='employees')

    def __repr__(self):
        return f"<User {self.name}>"


class Restaurant(db.Model):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    address = db.Column(db.String(200))

    cuisine = db.Column(db.String(100))

    rating = db.Column(db.Float)

    delivery = db.Column(db.Boolean, default=False)

    reservation = db.Column(db.Boolean, default=True)

    opening_hours = db.Column(db.String(50))

    delivery_time = db.Column(db.String(50))

    def __repr__(self):
        return f"<Restaurant {self.name}>"

class Table(db.Model):
    __tablename__ = 'tables'

    id = db.Column(db.Integer, primary_key=True)

    restaurant_id = db.Column(
        db.Integer,
        db.ForeignKey('restaurants.id'),
        nullable=False
    )

    number = db.Column(db.String(10), nullable=False)

    seats = db.Column(db.Integer)

    status = db.Column(db.String(20), default='free')

    location = db.Column(db.String(100))

    # PLAN SALI
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)

    shape = db.Column(db.String(20))

    width = db.Column(db.Integer, nullable=True)
    height = db.Column(db.Integer, nullable=True)

    radius = db.Column(db.Integer, nullable=True)

    rotation = db.Column(db.Integer, default=0)

    restaurant = db.relationship(
        'Restaurant',
        backref='tables'
    )


class ReservationItem(db.Model):
    __tablename__ = 'reservation_items'

    reservation_id = db.Column(db.Integer, db.ForeignKey('reservations.id', ondelete='CASCADE'), primary_key=True)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_items.id', ondelete='CASCADE'), primary_key=True)

    # Dodatkowa kolumna na ilość!
    quantity = db.Column(db.Integer, nullable=False, default=1)

    # Relacje pomocnicze, by łatwo wyciągać dane dania w pętli
    menu_item = db.relationship('MenuItem')

class Reservation(db.Model):
    __tablename__ = 'reservations'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    table_id = db.Column(db.Integer, db.ForeignKey('tables.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    people = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, cancelled
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='reservations')
    table = db.relationship('Table', backref='reservations')
    restaurant = db.relationship('Restaurant', backref='reservations')
    items = db.relationship('ReservationItem', backref='reservation', cascade="all, delete-orphan")

    @property
    def total_price(self):
        """Oblicza łączną wartość zamówionych dań do tej rezerwacji"""
        total = 0.0
        for item in self.items:
            # item to obiekt ReservationItem
            # item.menu_item to obiekt MenuItem, z którego bierzemy cenę
            if item.menu_item:
                total += item.quantity * item.menu_item.price
        return total

class MenuItem(db.Model):
    __tablename__ = 'menu_items'

    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    name = db.Column(db.String(100))
    price = db.Column(db.Float)
    category = db.Column(db.String(50))
    description = db.Column(db.Text)
    available = db.Column(db.Boolean, default=True)
    restaurant = db.relationship('Restaurant', backref='menu_items')

