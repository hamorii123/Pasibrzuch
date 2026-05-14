from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from functools import wraps
from datetime import datetime
import json
from flask_migrate import Migrate
from models import db, User, Restaurant, Table, Reservation, MenuItem

app = Flask(__name__)
app.secret_key = 'pasibrzuch_mobile_2024_secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db.init_app(app)
migrate = Migrate(app, db)

@app.context_processor
def inject_now():
    return {'now': datetime.now()}

def get_tables_for_restaurant(restaurant_id):
    return Table.query.filter_by(restaurant_id=restaurant_id).all()

# Dane testowe dla koszyka
sample_cart = [
    {'id': 1, 'name': 'Stek Wołowy z Grilla', 'price': 45.00, 'quantity': 1},
    {'id': 2, 'name': 'Zupa Pomidorowa', 'price': 12.00, 'quantity': 2}
]


# Helper functions
def get_assigned_restaurant(user_id):
    """Pobierz restaurację przypisaną do kelnera"""
    user = User.query.get(user_id)
    if user and user.role == 'waiter':
        return Restaurant.query.get(user.restaurant_id)
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
        user = User.query.get(session['user_id'])
        if user:
            if user.role == 'client':
                return redirect(url_for('client_dashboard'))
            elif user.role == 'waiter':
                return redirect(url_for('waiter_dashboard'))
            elif user.role == 'manager':
                return redirect(url_for('manager_dashboard'))
        return redirect(url_for('login'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Szukaj użytkownika
        user = User.query.filter_by(email=email, password=password).first()

        if user:
            # Zaloguj użytkownika
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['role'] = user.role
            session.permanent = True

            flash(f'Zalogowano pomyślnie! Witaj {user.name}', 'success')

            # Przekieruj do odpowiedniego panelu
            if user.role == 'client':
                return redirect(url_for('client_dashboard'))
            elif user.role == 'waiter':
                return redirect(url_for('waiter_dashboard'))
            elif user.role == 'manager':
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
    restaurants = Restaurant.query.all()

    return render_template(
        'client/dashboard_mobile.html',
        user_name=session['user_name'],
        restaurants=restaurants,
        reservations=[],
        orders=[]
    )

@app.route('/client/restaurants')
@login_required
def client_restaurants():
    """Lista restauracji"""
    if session.get('role') != 'client':
        flash('Brak dostępu', 'danger')
        return redirect(url_for('login'))

    restaurants = Restaurant.query.all()
    return render_template('client/restaurants_mobile.html', restaurants=restaurants)


@app.route('/client/menu/<int:restaurant_id>')
@login_required
def client_menu(restaurant_id):
    """Menu restauracji"""
    if session.get('role') != 'client':
        flash('Brak dostępu', 'danger')
        return redirect(url_for('login'))

    restaurant = Restaurant.query.get(restaurant_id)
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
        query=query.lower()
        filtered_restaurants = Restaurant.query.filter(
            (Restaurant.name.ilike(f'%{query}%')) |
            (Restaurant.cuisine.ilike(f'%{query}%'))
        ).all()
    else:
        filtered_restaurants = Restaurant.query.all()

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
    user = User.query.get(session['user_id'])

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

    restaurant = Restaurant.query.get(restaurant_id)
    tables = get_tables_for_restaurant(restaurant_id)

    if not restaurant:
        flash('Restauracja nie znaleziona', 'danger')
        return redirect(url_for('client_restaurants'))

    return render_template('client/reservation_mobile.html',
                           restaurant=restaurant,
                           tables=tables,
                           now=datetime.now()
                           )

@app.route('/client/reservation/<int:restaurant_id>/submit', methods=['POST'])
@login_required
def submit_reservation(restaurant_id):
    """Zapisz rezerwację"""
    if session.get('role') != 'client':
        return jsonify({'success': False, 'message': 'Brak dostępu'})

    try:
        data = request.get_json()

        # --- walidacja minimalna ---
        table_id = int(data.get('tableId'))
        people = int(data.get('people'))
        notes = data.get('notes', '')

        res_date = datetime.strptime(data.get('date'), "%Y-%m-%d").date()
        res_time = datetime.strptime(data.get('time'), "%H:%M").time()

        table = Table.query.filter_by(
            id=table_id,
            restaurant_id=restaurant_id
        ).first()

        if not table:
            return jsonify({'success': False, 'message': 'Stolik nie istnieje'}), 404

        if table.seats < people:
            return jsonify({'success': False, 'message': 'Za mały stolik'}), 400

        if table.status != 'free':
            return jsonify({'success': False, 'message': 'Stolik niedostępny'}), 400

        # --- tworzenie rezerwacji ---
        reservation = Reservation(
            user_id=session['user_id'],
            restaurant_id=restaurant_id,
            table_id=table_id,
            date=res_date,
            time=res_time,
            people=people,
            notes=notes,
            status='pending'
        )

        # --- zmiana statusu stolika ---
        table.status = 'reserved'

        db.session.add(reservation)
        db.session.commit()


        return jsonify({
            'success': True,
            'message': f'Rezerwacja została potwierdzona. Numer rezerwacji: #{reservation.id}',
            'reservation_id': reservation.id
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

    restaurant = Restaurant.query.get(restaurant_id)
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
    return redirect(url_for('waiter_restaurant_view', restaurant_id=assigned_restaurant.id))


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

    return redirect(url_for('waiter_restaurant_view', restaurant_id=assigned_restaurant.id))


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

    if assigned_restaurant.id != restaurant_id:
        flash('Nie masz dostępu do tej restauracji', 'danger')
        return redirect(url_for('waiter_my_restaurant'))

    restaurant = Restaurant.query.get(restaurant_id)
    if not restaurant:
        flash('Restauracja nie znaleziona', 'danger')
        return redirect(url_for('waiter_my_restaurant'))

    tables_data=Table.query.filter_by(
        restaurant_id=restaurant_id
    ).all()

    # Statystyki
    stats = {
        'free': len([t for t in tables_data if t.status == 'free']),
        'occupied': len([t for t in tables_data if t.status == 'occupied']),
        'reserved': len([t for t in tables_data if t.status == 'reserved']),
        'cleaning': len([t for t in tables_data if t.status == 'cleaning'])
    }

    return render_template('waiter/restaurant_view.html',
                           restaurant=restaurant,
                           tables=tables_data,
                           stats=stats,
                           upcoming_reservations=[],#upcoming_reservations,
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

    if assigned_restaurant.id != restaurant_id:
        flash('Nie masz dostępu do tej restauracji', 'danger')
        return redirect(url_for('waiter_my_restaurant'))

    restaurant = Restaurant.query.get(restaurant_id)
    if not restaurant:
        flash('Restauracja nie znaleziona', 'danger')
        return redirect(url_for('waiter_my_restaurant'))

    # Użyj funkcji get_tables_for_restaurant zamiast bezpośredniego dostępu
    #tables_data = get_tables_for_restaurant(restaurant_id)
    tables_data = [
        {
            "id": t.id,
            "number": t.number,
            "seats": t.seats,
            "status": t.status,
            "shape": t.shape,
            "width": t.width,
            "height": t.height,
            "radius": t.radius,
            "x": t.x,
            "y": t.y,
            "rotation": t.rotation,
        }
        for t in get_tables_for_restaurant(restaurant_id)
    ]

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