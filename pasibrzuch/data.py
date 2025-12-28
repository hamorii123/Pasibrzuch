import json
import os

# Dane użytkowników
users = [
    {'id': 1, 'name': 'Jan Kowalski', 'email': 'klient@example.com', 'password': 'klient123', 'role': 'client'},
    {'id': 2, 'name': 'Anna Nowak', 'email': 'kelner@example.com', 'password': 'kelner123', 'role': 'waiter'},
    {'id': 3, 'name': 'Piotr Wiśniewski', 'email': 'manager@example.com', 'password': 'manager123', 'role': 'manager'},
    {'id': 4, 'name': 'Michał Zieliński', 'email': 'klient2@example.com', 'password': 'klient123', 'role': 'client'}
]

# Restauracje w systemie P@SIBRZUCH
restaurants = [
    {
        'id': 1,
        'name': '13 Muz',
        'address': 'ul. Restauracyjna 13, Szczecin',
        'phone': '+48 123 456 789',
        'email': 'kontakt@13muz.pl',
        'opening_hours': '12:00-23:00',
        'cuisine': 'Polska, Europejska',
        'description': 'Elegancka restauracja z tradycyjną kuchnią polską',
        'image': '/static/images/13muz.jpg',
        'rating': 4.7,
        'delivery': True,
        'reservation': True
    },
    {
        'id': 2,
        'name': 'La Bella Italia',
        'address': 'ul. Włoska 5, Szczecin',
        'phone': '+48 987 654 321',
        'email': 'info@labella.pl',
        'opening_hours': '11:00-22:00',
        'cuisine': 'Włoska',
        'description': 'Autentyczna kuchnia włoska w sercu Szczecina',
        'image': '/static/images/bellaitalia.jpg',
        'rating': 4.5,
        'delivery': True,
        'reservation': True
    },
    {
        'id': 3,
        'name': 'Sushi Master',
        'address': 'ul. Japońska 8, Szczecin',
        'phone': '+48 555 123 456',
        'email': 'sushi@master.pl',
        'opening_hours': '10:00-23:00',
        'cuisine': 'Japońska, Sushi',
        'description': 'Najlepsze sushi w mieście',
        'image': '/static/images/sushimaster.jpg',
        'rating': 4.8,
        'delivery': True,
        'reservation': True
    },
    {
        'id': 4,
        'name': 'Burger House',
        'address': 'ul. Fastfoodowa 21, Szczecin',
        'phone': '+48 777 888 999',
        'email': 'burger@house.pl',
        'opening_hours': '10:00-24:00',
        'cuisine': 'Amerykańska, Burgery',
        'description': 'Autentyczne amerykańskie burgery',
        'image': '/static/images/burgerhouse.jpg',
        'rating': 4.3,
        'delivery': True,
        'reservation': False
    }
]

# Menu dla wszystkich restauracji
menu_items = [
    # 13 Muz
    {
        'id': 1,
        'restaurant_id': 1,
        'name': 'Stek Wołowy z Grilla',
        'description': 'Soczysty stek wołowy z ziemniakami i warzywami sezonowymi',
        'category': 'Dania Główne',
        'price': 45.00,
        'available': True,
        'allergens': ['gluten'],
        'stock': 12,
        'image_url': '/static/images/stek.jpg'
    },
    {
        'id': 2,
        'restaurant_id': 1,
        'name': 'Łosoś z Grilla',
        'description': 'Świeży łosoś z sosem cytrynowym i ryżem jaśminowym',
        'category': 'Dania Główne',
        'price': 38.00,
        'available': True,
        'allergens': ['ryby'],
        'stock': 8,
        'image_url': '/static/images/losos.jpg'
    },
    # La Bella Italia
    {
        'id': 3,
        'restaurant_id': 2,
        'name': 'Pizza Margherita',
        'description': 'Klasyczna pizza z sosem pomidorowym i mozzarellą',
        'category': 'Pizza',
        'price': 28.00,
        'available': True,
        'allergens': ['gluten', 'mleko'],
        'stock': 20,
        'image_url': '/static/images/pizza.jpg'
    },
    {
        'id': 4,
        'restaurant_id': 2,
        'name': 'Spaghetti Carbonara',
        'description': 'Makaron z sosem carbonara i pancettą',
        'category': 'Makarony',
        'price': 32.00,
        'available': True,
        'allergens': ['gluten', 'jaja', 'mleko'],
        'stock': 15,
        'image_url': '/static/images/carbonara.jpg'
    },
    # Sushi Master
    {
        'id': 5,
        'restaurant_id': 3,
        'name': 'Zestaw Sushi Deluxe',
        'description': '15 kawałków różnych sushi',
        'category': 'Zestawy',
        'price': 65.00,
        'available': True,
        'allergens': ['ryby', 'soja'],
        'stock': 10,
        'image_url': '/static/images/sushiset.jpg'
    },
    # Burger House
    {
        'id': 6,
        'restaurant_id': 4,
        'name': 'Burger Classic',
        'description': 'Wołowy burger z serem, sałatą i pomidorem',
        'category': 'Burgery',
        'price': 25.00,
        'available': True,
        'allergens': ['gluten', 'mleko'],
        'stock': 30,
        'image_url': '/static/images/burger.jpg'
    }
]

# Stoliki dla restauracji
tables = [
    # 13 Muz
    {'id': 1, 'restaurant_id': 1, 'number': 'Stolik 1', 'seats': 4, 'shape': 'kwadratowy', 'x': 100, 'y': 100, 'status': 'wolny', 'location': 'centrum'},
    {'id': 2, 'restaurant_id': 1, 'number': 'Stolik 2', 'seats': 6, 'shape': 'okrągły', 'x': 250, 'y': 100, 'status': 'zajęty', 'location': 'przy oknie'},
    {'id': 3, 'restaurant_id': 1, 'number': 'Stolik 3', 'seats': 2, 'shape': 'kwadratowy', 'x': 400, 'y': 100, 'status': 'sprzątanie', 'location': 'centrum'},
    {'id': 4, 'restaurant_id': 1, 'number': 'Stolik 4', 'seats': 4, 'shape': 'kwadratowy', 'x': 100, 'y': 250, 'status': 'wolny', 'location': 'centrum'},
    # La Bella Italia
    {'id': 5, 'restaurant_id': 2, 'number': 'Stolik A1', 'seats': 4, 'shape': 'okrągły', 'x': 100, 'y': 100, 'status': 'wolny', 'location': 'taras'},
    {'id': 6, 'restaurant_id': 2, 'number': 'Stolik A2', 'seats': 8, 'shape': 'długi', 'x': 300, 'y': 100, 'status': 'zarezerwowany', 'location': 'wewnątrz'},
    # Sushi Master
    {'id': 7, 'restaurant_id': 3, 'number': 'Stolik S1', 'seats': 2, 'shape': 'kwadratowy', 'x': 100, 'y': 100, 'status': 'wolny', 'location': 'przy barze'},
    {'id': 8, 'restaurant_id': 3, 'number': 'Stolik S2', 'seats': 6, 'shape': 'okrągły', 'x': 250, 'y': 100, 'status': 'zajęty', 'location': 'centrum'},
    # Burger House
    {'id': 9, 'restaurant_id': 4, 'number': 'Stolik B1', 'seats': 4, 'shape': 'kwadratowy', 'x': 100, 'y': 100, 'status': 'wolny', 'location': 'przy oknie'},
    {'id': 10, 'restaurant_id': 4, 'number': 'Stolik B2', 'seats': 4, 'shape': 'kwadratowy', 'x': 250, 'y': 100, 'status': 'wolny', 'location': 'centrum'}
]

# Rezerwacje
reservations = [
    {
        'id': 1,
        'client_id': 1,
        'client_name': 'Jan Kowalski',
        'restaurant_id': 1,
        'restaurant_name': '13 Muz',
        'table_id': 2,
        'table_number': 'Stolik 2',
        'date': '2024-03-15',
        'time': '18:00',
        'people': 4,
        'menu_items': [1, 2],
        'notes': 'Urodziny',
        'status': 'potwierdzona',
        'created_at': '2024-03-10 14:30:00'
    },
    {
        'id': 2,
        'client_id': 4,
        'client_name': 'Michał Zieliński',
        'restaurant_id': 2,
        'restaurant_name': 'La Bella Italia',
        'table_id': 6,
        'table_number': 'Stolik A2',
        'date': '2024-03-16',
        'time': '20:30',
        'people': 6,
        'menu_items': [3, 4],
        'notes': 'Spotkanie biznesowe',
        'status': 'potwierdzona',
        'created_at': '2024-03-11 10:15:00'
    }
]

# Zamówienia
orders = [
    {
        'id': 1,
        'client_id': 1,
        'client_name': 'Jan Kowalski',
        'restaurant_id': 4,
        'restaurant_name': 'Burger House',
        'items': [
            {'id': 6, 'name': 'Burger Classic', 'price': 25.00, 'quantity': 2},
            {'id': 6, 'name': 'Burger Classic', 'price': 25.00, 'quantity': 1}
        ],
        'total_amount': 75.00,
        'delivery_address': 'ul. Example 123, Szczecin',
        'delivery_time': '2024-03-15 19:00',
        'notes': 'Proszę o dodatkowy sos',
        'status': 'dostarczone',
        'created_at': '2024-03-14 16:45:00'
    }
]

# Funkcje do zapisywania danych
def save_menu_data():
    # W prawdziwej aplikacji zapis do bazy danych
    pass

def save_table_data():
    # W prawdziwej aplikacji zapis do bazy danych
    pass

def save_reservation_data():
    # W prawdziwej aplikacji zapis do bazy danych
    pass

def save_order_data():
    # W prawdziwej aplikacji zapis do bazy danych
    pass