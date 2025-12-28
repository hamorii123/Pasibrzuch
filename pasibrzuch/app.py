from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from functools import wraps
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = 'pasibrzuch_mobile_2024_secret'

# Dane testowe
users = [
    {'id': 1, 'name': 'Jan Kowalski', 'email': 'klient@example.com', 'password': 'klient123', 'role': 'client'},
    {'id': 2, 'name': 'Anna Nowak', 'email': 'kelner@example.com', 'password': 'kelner123', 'role': 'waiter',
     'restaurant_id': 1},  # Przypisana do 13 Muz
    {'id': 3, 'name': 'Piotr Wiśniewski', 'email': 'manager@example.com', 'password': 'manager123', 'role': 'manager'},
    {'id': 4, 'name': 'Michał Kowalczyk', 'email': 'kelner2@example.com', 'password': 'kelner123', 'role': 'waiter',
     'restaurant_id': 2},  # Przypisana do La Bella Italia
]
# Dodaj bardziej szczegółowe dane dla restauracji
restaurants = [
    {
        'id': 1,
        'name': '13 Muz',
        'address': 'ul. Restauracyjna 13, Szczecin',
        'rating': 4.7,
        'cuisine': 'Polska',
        'delivery': True,
        'reservation': True,
        'opening_hours': '12:00-22:00',
        'delivery_time': '30-45 min',
        'floor_plan': {
            'width': 800,
            'height': 600,
            'background_color': '#f8f9fa',
            'tables': [
                {'id': 1, 'x': 100, 'y': 100, 'rotation': 0, 'shape': 'rectangle', 'width': 80, 'height': 120},
                {'id': 2, 'x': 250, 'y': 150, 'rotation': 45, 'shape': 'circle', 'radius': 60},
                {'id': 3, 'x': 450, 'y': 200, 'rotation': 0, 'shape': 'rectangle', 'width': 100, 'height': 80},
                {'id': 4, 'x': 650, 'y': 300, 'rotation': 90, 'shape': 'circle', 'radius': 70},
                {'id': 5, 'x': 300, 'y': 400, 'rotation': 0, 'shape': 'rectangle', 'width': 120, 'height': 80},
                {'id': 6, 'x': 500, 'y': 450, 'rotation': 30, 'shape': 'circle', 'radius': 50},
                {'id': 7, 'x': 100, 'y': 500, 'rotation': 0, 'shape': 'rectangle', 'width': 150, 'height': 100},
                {'id': 8, 'x': 700, 'y': 100, 'rotation': 0, 'shape': 'circle', 'radius': 40},
            ]
        }
    },
    {
        'id': 2,
        'name': 'La Bella Italia',
        'address': 'ul. Włoska 5, Szczecin',
        'rating': 4.5,
        'cuisine': 'Włoska',
        'delivery': True,
        'reservation': True,
        'opening_hours': '11:00-23:00',
        'delivery_time': '25-40 min',
        'floor_plan': {
            'width': 900,
            'height': 700,
            'background_color': '#fff5e6',
            'tables': [
                {'id': 9, 'x': 150, 'y': 150, 'rotation': 0, 'shape': 'rectangle', 'width': 90, 'height': 140},
                {'id': 10, 'x': 350, 'y': 200, 'rotation': 0, 'shape': 'circle', 'radius': 65},
                {'id': 11, 'x': 550, 'y': 250, 'rotation': 0, 'shape': 'rectangle', 'width': 110, 'height': 90},
                {'id': 12, 'x': 750, 'y': 350, 'rotation': 0, 'shape': 'circle', 'radius': 75},
            ]
        }
    }
]

# Rozbudowane dane dla stolików
def get_tables_for_restaurant(restaurant_id):
    """Pobierz stoliki dla konkretnej restauracji"""
    if restaurant_id == 1:
        return [
            {'id': 1, 'number': '1', 'seats': 2, 'status': 'free', 'location': 'Przy oknie',
             'shape': 'rectangle', 'width': 80, 'height': 120, 'x': 100, 'y': 100, 'rotation': 0,
             'reservation': None},
            {'id': 2, 'number': '2', 'seats': 4, 'status': 'occupied', 'location': 'Centrum sali',
             'shape': 'circle', 'radius': 60, 'x': 250, 'y': 150, 'rotation': 45,
             'reservation': {'time': '14:30', 'name': 'Jan Kowalski', 'people': 4, 'duration': 90}},
            {'id': 3, 'number': '3', 'seats': 2, 'status': 'free', 'location': 'Przy wejściu',
             'shape': 'rectangle', 'width': 100, 'height': 80, 'x': 450, 'y': 200, 'rotation': 0,
             'reservation': None},
            {'id': 4, 'number': '4', 'seats': 6, 'status': 'reserved', 'location': 'Centrum sali',
             'shape': 'circle', 'radius': 70, 'x': 650, 'y': 300, 'rotation': 90,
             'reservation': {'time': '18:00', 'name': 'Anna Kowalska', 'people': 4, 'duration': 120}},
            {'id': 5, 'number': '5', 'seats': 2, 'status': 'cleaning', 'location': 'Przy barze',
             'shape': 'rectangle', 'width': 120, 'height': 80, 'x': 300, 'y': 400, 'rotation': 0,
             'reservation': None},
            {'id': 6, 'number': '6', 'seats': 4, 'status': 'occupied', 'location': 'Przy oknie',
             'shape': 'circle', 'radius': 50, 'x': 500, 'y': 450, 'rotation': 30,
             'reservation': {'time': '13:00', 'name': 'Piotr Wiśniewski', 'people': 3, 'duration': 60}},
            {'id': 7, 'number': '7', 'seats': 8, 'status': 'free', 'location': 'VIP',
             'shape': 'rectangle', 'width': 150, 'height': 100, 'x': 100, 'y': 500, 'rotation': 0,
             'reservation': None},
            {'id': 8, 'number': '8', 'seats': 4, 'status': 'reserved', 'location': 'Przy kominku',
             'shape': 'circle', 'radius': 40, 'x': 700, 'y': 100, 'rotation': 0,
             'reservation': {'time': '20:30', 'name': 'Michał Nowak', 'people': 2, 'duration': 90}},
        ]
    if restaurant_id == 2:
        return [
            {'id': 9, 'number': '1', 'seats': 4, 'status': 'free', 'location': 'Taraz',
             'shape': 'rectangle', 'width': 90, 'height': 140, 'x': 150, 'y': 150, 'rotation': 0,
             'reservation': None},
            {'id': 10, 'number': '2', 'seats': 6, 'status': 'occupied', 'location': 'Centrum',
             'shape': 'circle', 'radius': 65, 'x': 350, 'y': 200, 'rotation': 0,
             'reservation': {'time': '15:00', 'name': 'Katarzyna Zielińska', 'people': 5, 'duration': 90}},
            {'id': 11, 'number': '3', 'seats': 2, 'status': 'free', 'location': 'Przy kuchni',
             'shape': 'rectangle', 'width': 110, 'height': 90, 'x': 550, 'y': 250, 'rotation': 0,
             'reservation': None},
            {'id': 12, 'number': '4', 'seats': 8, 'status': 'reserved', 'location': 'VIP',
             'shape': 'circle', 'radius': 75, 'x': 750, 'y': 350, 'rotation': 0,
             'reservation': {'time': '19:30', 'name': 'Robert Lewandowski', 'people': 7, 'duration': 120}},
        ]
# Dane testowe dla stolików
tables = [
    {'id': 1, 'number': '1', 'seats': 2, 'available': True},
    {'id': 2, 'number': '2', 'seats': 4, 'available': True},
    {'id': 3, 'number': '3', 'seats': 2, 'available': False},
    {'id': 4, 'number': '4', 'seats': 6, 'available': True},
    {'id': 5, 'number': '5', 'seats': 2, 'available': True},
    {'id': 6, 'number': '6', 'seats': 4, 'available': True},
]

# Dane testowe dla koszyka
sample_cart = [
    {'id': 1, 'name': 'Stek Wołowy z Grilla', 'price': 45.00, 'quantity': 1},
    {'id': 2, 'name': 'Zupa Pomidorowa', 'price': 12.00, 'quantity': 2}
]


# Helper functions
def get_assigned_restaurant(user_id):
    """Pobierz restaurację przypisaną do kelnera"""
    user = next((u for u in users if u['id'] == user_id), None)
    if user and user.get('role') == 'waiter':
        return next((r for r in restaurants if r['id'] == user.get('restaurant_id')), None)
    return None


# Decorator do sprawdzania zalogowania
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Proszę się zalogować', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function


@app.route('/')
def index():
    """Strona główna - przekierowuje do logowania"""
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Strona logowania"""
    # Jeśli użytkownik jest już zalogowany, przekieruj do odpowiedniego dashboard
    if 'user_id' in session:
        user = next((u for u in users if u['id'] == session['user_id']), None)
        if user:
            if user['role'] == 'client':
                return redirect(url_for('client_dashboard'))
            elif user['role'] == 'waiter':
                return redirect(url_for('waiter_dashboard'))
            elif user['role'] == 'manager':
                return redirect(url_for('manager_dashboard'))
        return redirect(url_for('login'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Szukaj użytkownika
        user = next((u for u in users if u['email'] == email and u['password'] == password), None)

        if user:
            # Zaloguj użytkownika
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['role'] = user['role']
            session.permanent = True

            flash(f'Zalogowano pomyślnie! Witaj {user["name"]}', 'success')

            # Przekieruj do odpowiedniego panelu
            if user['role'] == 'client':
                return redirect(url_for('client_dashboard'))
            elif user['role'] == 'waiter':
                return redirect(url_for('waiter_dashboard'))
            elif user['role'] == 'manager':
                return redirect(url_for('manager_dashboard'))
        else:
            flash('Nieprawidłowy email lub hasło', 'danger')

    return render_template('login.html')


@app.route('/logout')
def logout():
    """Wylogowanie"""
    session.clear()
    flash('Wylogowano pomyślnie', 'info')
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Rejestracja (opcjonalnie)"""
    if request.method == 'POST':
        # Tutaj logika rejestracji
        flash('Rejestracja w budowie', 'info')
        return redirect(url_for('login'))

    return render_template('register.html')


# ========== PANEL KLIENTA ==========
@app.route('/client/dashboard')
@login_required
def client_dashboard():
    """Dashboard klienta"""
    if session.get('role') != 'client':
        flash('Brak dostępu', 'danger')
        return redirect(url_for('login'))

    return render_template('client/dashboard_mobile.html',
                           user_name=session['user_name'],
                           restaurants=restaurants,
                           reservations=[],
                           orders=[])


@app.route('/client/restaurants')
@login_required
def client_restaurants():
    """Lista restauracji"""
    if session.get('role') != 'client':
        flash('Brak dostępu', 'danger')
        return redirect(url_for('login'))

    return render_template('client/restaurants_mobile.html', restaurants=restaurants)


@app.route('/client/menu/<int:restaurant_id>')
@login_required
def client_menu(restaurant_id):
    """Menu restauracji"""
    if session.get('role') != 'client':
        flash('Brak dostępu', 'danger')
        return redirect(url_for('login'))

    restaurant = next((r for r in restaurants if r['id'] == restaurant_id), None)
    if not restaurant:
        flash('Restauracja nie znaleziona', 'danger')
        return redirect(url_for('client_restaurants'))

    menu_items = [
        {'id': 1, 'name': 'Stek Wołowy z Grilla', 'price': 45.00, 'category': 'Dania Główne',
         'description': 'Stek z polędwicy wołowej podany z ziemniakami i sosem pieprzowym', 'available': True},
        {'id': 2, 'name': 'Łosoś z Grilla', 'price': 38.00, 'category': 'Dania Główne',
         'description': 'Filet z łososia z warzywami sezonowymi', 'available': True},
        {'id': 3, 'name': 'Zupa Pomidorowa', 'price': 12.00, 'category': 'Zupy',
         'description': 'Klasyczna zupa pomidorowa z makaronem', 'available': True},
        {'id': 4, 'name': 'Sałatka Cezar', 'price': 25.00, 'category': 'Sałatki',
         'description': 'Sałatka z kurczakiem, grzankami i sosem cezar', 'available': True},
        {'id': 5, 'name': 'Spaghetti Carbonara', 'price': 32.00, 'category': 'Dania Główne',
         'description': 'Makaron z sosem śmietanowym, boczkiem i żółtkiem', 'available': True},
        {'id': 6, 'name': 'Tiramisu', 'price': 18.00, 'category': 'Desery',
         'description': 'Klasyczny włoski deser kawowy', 'available': True}
    ]

    categories = list(set([item['category'] for item in menu_items]))

    return render_template('client/menu_mobile.html',
                           restaurant=restaurant,
                           menu_items=menu_items,
                           categories=categories)


@app.route('/client/search')
@login_required
def client_search():
    """Strona wyszukiwania"""
    if session.get('role') != 'client':
        flash('Brak dostępu', 'danger')
        return redirect(url_for('login'))

    query = request.args.get('q', '')

    # Filtruj restauracje
    filtered_restaurants = []
    if query:
        query_lower = query.lower()
        filtered_restaurants = [
            r for r in restaurants
            if query_lower in r['name'].lower() or query_lower in r['cuisine'].lower()
        ]
    else:
        filtered_restaurants = restaurants

    return render_template('client/search_mobile.html',
                           query=query,
                           restaurants=filtered_restaurants)


@app.route('/client/cart')
@login_required
def client_cart():
    """Koszyk"""
    if session.get('role') != 'client':
        flash('Brak dostępu', 'danger')
        return redirect(url_for('login'))

    # W rzeczywistej aplikacji pobieralibyśmy koszyk z bazy danych
    # Teraz używamy danych testowych
    cart_items = sample_cart
    total = sum(item['price'] * item['quantity'] for item in cart_items)

    return render_template('client/cart_mobile.html',
                           cart_items=cart_items,
                           total=total)


@app.route('/client/profile')
@login_required
def client_profile():
    """Profil użytkownika"""
    if session.get('role') != 'client':
        flash('Brak dostępu', 'danger')
        return redirect(url_for('login'))

    # Znajdź użytkownika
    user = next((u for u in users if u['id'] == session['user_id']), None)

    # Dane testowe
    reservations = [
        {'id': 1, 'restaurant_name': '13 Muz', 'date': '2024-01-15', 'time': '18:00', 'people': 2,
         'status': 'Potwierdzona'},
        {'id': 2, 'restaurant_name': 'La Bella Italia', 'date': '2024-01-20', 'time': '19:30', 'people': 4,
         'status': 'Oczekująca'}
    ]

    orders = [
        {'id': 1, 'restaurant_name': '13 Muz', 'date': '2024-01-10', 'total': 89.00, 'status': 'Dostarczone'},
        {'id': 2, 'restaurant_name': 'La Bella Italia', 'date': '2024-01-12', 'total': 124.50, 'status': 'W drodze'}
    ]

    return render_template('client/profile_mobile.html',
                           user=user,
                           reservations=reservations,
                           orders=orders)


@app.route('/client/reservation/<int:restaurant_id>')
@login_required
def client_reservation(restaurant_id):
    """Rezerwacja stolika"""
    if session.get('role') != 'client':
        flash('Brak dostępu', 'danger')
        return redirect(url_for('login'))

    restaurant = next((r for r in restaurants if r['id'] == restaurant_id), None)
    if not restaurant:
        flash('Restauracja nie znaleziona', 'danger')
        return redirect(url_for('client_restaurants'))

    return render_template('client/reservation_mobile.html',
                           restaurant=restaurant,
                           tables=tables)


@app.route('/client/reservation/<int:restaurant_id>/submit', methods=['POST'])
@login_required
def submit_reservation(restaurant_id):
    """Zapisz rezerwację"""
    if session.get('role') != 'client':
        return jsonify({'success': False, 'message': 'Brak dostępu'})

    try:
        data = request.get_json()

        # W rzeczywistej aplikacji zapisalibyśmy do bazy danych
        reservation_id = 1001  # Przykładowe ID

        return jsonify({
            'success': True,
            'message': f'Rezerwacja została potwierdzona. Numer rezerwacji: #{reservation_id}',
            'reservation_id': reservation_id
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route('/client/order/<int:restaurant_id>')
@login_required
def client_order(restaurant_id):
    """Zamówienie online"""
    if session.get('role') != 'client':
        flash('Brak dostępu', 'danger')
        return redirect(url_for('login'))

    restaurant = next((r for r in restaurants if r['id'] == restaurant_id), None)
    if not restaurant:
        flash('Restauracja nie znaleziona', 'danger')
        return redirect(url_for('client_restaurants'))

    return render_template('client/order_mobile.html',
                           restaurant=restaurant)


@app.route('/client/order/<int:restaurant_id>/submit', methods=['POST'])
@login_required
def submit_order(restaurant_id):
    """Zapisz zamówienie"""
    if session.get('role') != 'client':
        return jsonify({'success': False, 'message': 'Brak dostępu'})

    try:
        data = request.get_json()

        # W rzeczywistej aplikacji zapisalibyśmy do bazy danych
        order_id = 2001  # Przykładowe ID

        return jsonify({
            'success': True,
            'message': f'Zamówienie zostało przyjęte! Numer zamówienia: #{order_id}. Szacowany czas dostawy: 30-45 minut.',
            'order_id': order_id
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route('/client/cart/add', methods=['POST'])
@login_required
def add_to_cart():
    """Dodaj produkt do koszyka"""
    if session.get('role') != 'client':
        return jsonify({'success': False, 'message': 'Brak dostępu'})

    try:
        data = request.get_json()
        # Tutaj logika dodawania do koszyka
        return jsonify({'success': True, 'message': 'Produkt dodany do koszyka'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


# ========== PANEL KELNERA ==========
@app.route('/waiter/dashboard')
@login_required
def waiter_dashboard():
    """Dashboard kelnera - główny widok tabletowy"""
    if session.get('role') != 'waiter':
        flash('Brak dostępu', 'danger')
        return redirect(url_for('login'))

    # Pobierz przypisaną restaurację
    assigned_restaurant = get_assigned_restaurant(session['user_id'])

    if not assigned_restaurant:
        flash('Nie masz przypisanej restauracji', 'warning')
        return redirect(url_for('login'))

    # Przekieruj od razu do widoku restauracji
    return redirect(url_for('waiter_restaurant_view', restaurant_id=assigned_restaurant['id']))


@app.route('/waiter/restaurant')
@login_required
def waiter_my_restaurant():
    """Automatyczne przekierowanie do przypisanej restauracji"""
    if session.get('role') != 'waiter':
        flash('Brak dostępu', 'danger')
        return redirect(url_for('login'))

    assigned_restaurant = get_assigned_restaurant(session['user_id'])

    if not assigned_restaurant:
        flash('Nie masz przypisanej restauracji', 'warning')
        return redirect(url_for('login'))

    return redirect(url_for('waiter_restaurant_view', restaurant_id=assigned_restaurant['id']))


@app.route('/waiter/restaurant/<int:restaurant_id>')
@login_required
def waiter_restaurant_view(restaurant_id):
    """Widok planu sali dla konkretnej restauracji"""
    if session.get('role') != 'waiter':
        flash('Brak dostępu', 'danger')
        return redirect(url_for('login'))

    # Sprawdź czy kelner ma dostęp do tej restauracji
    assigned_restaurant = get_assigned_restaurant(session['user_id'])

    if not assigned_restaurant:
        flash('Nie masz przypisanej restauracji', 'warning')
        return redirect(url_for('login'))

    if assigned_restaurant['id'] != restaurant_id:
        flash('Nie masz dostępu do tej restauracji', 'danger')
        return redirect(url_for('waiter_my_restaurant'))

    restaurant = next((r for r in restaurants if r['id'] == restaurant_id), None)
    if not restaurant:
        flash('Restauracja nie znaleziona', 'danger')
        return redirect(url_for('waiter_my_restaurant'))

    # Dane testowe dla planu sali
    tables_data = [
        {'id': 1, 'number': '1', 'seats': 2, 'status': 'free', 'location': 'Przy oknie', 'reservation': None},
        {'id': 2, 'number': '2', 'seats': 4, 'status': 'occupied', 'location': 'Centrum sali',
         'reservation': {'time': '14:30', 'name': 'Jan Kowalski', 'people': 4, 'duration': 90}},
        {'id': 3, 'number': '3', 'seats': 2, 'status': 'free', 'location': 'Przy wejściu', 'reservation': None},
        {'id': 4, 'number': '4', 'seats': 6, 'status': 'reserved', 'location': 'Centrum sali',
         'reservation': {'time': '18:00', 'name': 'Anna Kowalska', 'people': 4, 'duration': 120}},
        {'id': 5, 'number': '5', 'seats': 2, 'status': 'cleaning', 'location': 'Przy barze', 'reservation': None},
        {'id': 6, 'number': '6', 'seats': 4, 'status': 'occupied', 'location': 'Przy oknie',
         'reservation': {'time': '13:00', 'name': 'Piotr Wiśniewski', 'people': 3, 'duration': 60}},
        {'id': 7, 'number': '7', 'seats': 8, 'status': 'free', 'location': 'VIP', 'reservation': None},
        {'id': 8, 'number': '8', 'seats': 4, 'status': 'reserved', 'location': 'Przy kominku',
         'reservation': {'time': '20:30', 'name': 'Michał Nowak', 'people': 2, 'duration': 90}},
    ]

    # Statystyki
    stats = {
        'free': len([t for t in tables_data if t['status'] == 'free']),
        'occupied': len([t for t in tables_data if t['status'] == 'occupied']),
        'reserved': len([t for t in tables_data if t['status'] == 'reserved']),
        'cleaning': len([t for t in tables_data if t['status'] == 'cleaning'])
    }

    # Nadchodzące rezerwacje
    upcoming_reservations = [
        {'table': '4', 'time': '18:00', 'name': 'Anna Kowalska', 'people': 4,
         'notes': '24 kwiaty, 14 czerwiec, 16 róża'},
        {'table': '7', 'time': '20:30', 'name': 'Michał Nowak', 'people': 2, 'notes': 'Zakończone 2015'},
        {'table': '2', 'time': '21:00', 'name': 'Piotr Wiśniewski', 'people': 8, 'notes': 'Przygotowanie wystąpienia'},
    ]

    return render_template('waiter/restaurant_view.html',
                           restaurant=restaurant,
                           tables=tables_data,
                           stats=stats,
                           upcoming_reservations=upcoming_reservations,
                           current_date=datetime.now().strftime('%A, %d %B %Y'),
                           current_time=datetime.now().strftime('%H:%M'),
                           assigned_restaurant=assigned_restaurant)


@app.route('/waiter/table/<int:table_id>/update', methods=['POST'])
@login_required
def update_table_status(table_id):
    """Zmiana statusu stolika"""
    if session.get('role') != 'waiter':
        return jsonify({'success': False, 'message': 'Brak dostępu'})

    try:
        data = request.get_json()
        status = data.get('status')

        # Tutaj w rzeczywistej aplikacji zapis do bazy danych
        return jsonify({
            'success': True,
            'message': f'Status stolika #{table_id} zmieniony na {status}',
            'status': status
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route('/waiter/notification', methods=['POST'])
@login_required
def send_notification():
    """Wysłanie powiadomienia"""
    if session.get('role') != 'waiter':
        return jsonify({'success': False, 'message': 'Brak dostępu'})

    try:
        data = request.get_json()
        message = data.get('message')
        table_id = data.get('table_id')

        # Tutaj w rzeczywistej aplikacji wysyłanie powiadomień
        return jsonify({
            'success': True,
            'message': 'Powiadomienie wysłane',
            'notification_id': 123
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


# ========== ZARZĄDZANIE PLANEM SALI ==========
@app.route('/waiter/floor-plan/<int:restaurant_id>')
@login_required
def waiter_floor_plan(restaurant_id):
    """Edytowalny plan sali"""
    if session.get('role') != 'waiter':
        flash('Brak dostępu', 'danger')
        return redirect(url_for('login'))

    # Sprawdź czy kelner ma dostęp do tej restauracji
    assigned_restaurant = get_assigned_restaurant(session['user_id'])

    if not assigned_restaurant:
        flash('Nie masz przypisanej restauracji', 'warning')
        return redirect(url_for('login'))

    if assigned_restaurant['id'] != restaurant_id:
        flash('Nie masz dostępu do tej restauracji', 'danger')
        return redirect(url_for('waiter_my_restaurant'))

    restaurant = next((r for r in restaurants if r['id'] == restaurant_id), None)
    if not restaurant:
        flash('Restauracja nie znaleziona', 'danger')
        return redirect(url_for('waiter_my_restaurant'))

    # Użyj funkcji get_tables_for_restaurant zamiast bezpośredniego dostępu
    tables_data = get_tables_for_restaurant(restaurant_id)

    return render_template('waiter/floor_plan_editor.html',
                           restaurant=restaurant,
                           tables=tables_data,
                           assigned_restaurant=assigned_restaurant,
                           current_date=datetime.now().strftime('%A, %d %B %Y'),
                           current_time=datetime.now().strftime('%H:%M'))
# ========== PANEL MENADŻERA ==========
@app.route('/manager/dashboard')
@login_required
def manager_dashboard():
    """Dashboard menadżera"""
    if session.get('role') != 'manager':
        flash('Brak dostępu', 'danger')
        return redirect(url_for('login'))

    return f'<h1>Panel Menadżera - {session["user_name"]}</h1><a href="/logout">Wyloguj</a>'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)