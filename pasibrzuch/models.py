from flask_sqlalchemy import SQLAlchemy
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