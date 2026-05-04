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

    restaurant_id = db.Column(db.Integer, nullable=True)

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

    floor_plan = db.Column(db.Text)

    def __repr__(self):
        return f"<Restaurant {self.name}>"