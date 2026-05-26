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

    #db.drop_all()
    #db.create_all()
    #print("Tabele bazy danych zostały utworzone na nowo.")

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
        # === RESTAURACJA 1: 13 Muz (Kuchnia Polska) ===
        # Przystawki
        MenuItem(restaurant_id=1, name='Tatar wołowy', price=39.0, category='Przystawki',
                 description='Klasyczny tatar z polskiej polędwicy wołowej z żółtkiem, ogórkiem kiszonym, grzybkami i cebulką'),
        MenuItem(restaurant_id=1, name='Śledź w oleju lnianym', price=24.0, category='Przystawki',
                 description='Tradycyjny śledź bałtycki z cebulką, jabłkiem i kwaśną śmietaną na wiejskim chlebie'),
        MenuItem(restaurant_id=1, name='Placki ziemniaczane z łososiem', price=32.0, category='Przystawki',
                 description='Trzy chrupiące placki ziemniaczane z wędzonym łososiem i koperkowym sour cream'),
        MenuItem(restaurant_id=1, name='Oscypek z grilla', price=26.0, category='Przystawki',
                 description='Góralski ser oscypek zawijany w boczek, podawany na gorąco z konfiturą z żurawiny'),

        # Zupy
        MenuItem(restaurant_id=1, name='Żurek staropolski', price=22.0, category='Zupy',
                 description='Tradycyjny żurek na własnym zakwasie z białą kiełbasą, jajkiem i borowikami, podawany w chlebie'),
        MenuItem(restaurant_id=1, name='Rosół z lubczykiem', price=18.0, category='Zupy',
                 description='Ekskluzywny, długo gotowany rosół z trzech mięs z domowym makaronem i marchewką'),
        MenuItem(restaurant_id=1, name='Barszcz czerwony z uszkami', price=19.0, category='Zupy',
                 description='Czysty, pikantny barszcz z domowymi uszkami z nadzieniem grzybowo-kapustnym'),
        MenuItem(restaurant_id=1, name='Krem z borowików', price=24.0, category='Zupy',
                 description='Aksamitny krem ze świeżych borowików, zabielany śmietanką, podawany z groszkiem ptysiowym'),

        # Dania główne
        MenuItem(restaurant_id=1, name='Kotlet schabowy z kością', price=44.0, category='Dania główne',
                 description='Smażony na smalcu, gigantyczny schabowy podawany z purée ziemniaczanym i zasmażaną kapustą'),
        MenuItem(restaurant_id=1, name='Kaczka pieczona z jabłkami', price=58.0, category='Dania główne',
                 description='Połówka kaczki aromatyzowanej majerankiem, serwowana z kopytkami i czerwoną kapustą na ciepło'),
        MenuItem(restaurant_id=1, name='Pierogi ruskie z okrasą', price=29.0, category='Dania główne',
                 description='Ręcznie lepione pierogi z serem i ziemniakami, okraszone chrupiącym boczkiem i złotą cebulką'),
        MenuItem(restaurant_id=1, name='Pierogi z mięsem i kapustą', price=31.0, category='Dania główne',
                 description='Domowe pierogi z farszem z wieprzowiny i podgrzybków, okraszone słoninką'),
        MenuItem(restaurant_id=1, name='Gulasz jeleni z borowikami', price=52.0, category='Dania główne',
                 description='Aromatyczny gulasz z dziczyzny w sosie własnym, podawany z plackami drożdżowymi (pampuchami)'),
        MenuItem(restaurant_id=1, name='Golonka pieczona w piwie', price=49.0, category='Dania główne',
                 description='Chrupiąca golonka wieprzowa z dodatkiem chrzanu, musztardy i zasmażanej kapusty kiszonej'),
        MenuItem(restaurant_id=1, name='Placek po zbójnicku', price=46.0, category='Dania główne',
                 description='Wielki placek ziemniaczany z pikantnym gulaszem wieprzowym, gęstą śmietaną i serem'),
        MenuItem(restaurant_id=1, name='Pieczony filet z sandacza', price=54.0, category='Dania główne',
                 description='Sandacz w sosie kurkowym, podawany z dzikim ryżem i blanszowanymi szparagami'),

        # Sałatki
        MenuItem(restaurant_id=1, name='Sałatka z pieczonym burakiem', price=34.0, category='Sałatki',
                 description='Karmelizowany burak, kozi ser, orzechy włoskie, rukola, sos miodowo-musztardowy'),

        # Menu dla dzieci
        MenuItem(restaurant_id=1, name='Mini kurczaczki', price=22.0, category='Dla dzieci',
                 description='Chrupiące kęski z piersi kurczaka z frytkami i mizerią'),

        # Desery
        MenuItem(restaurant_id=1, name='Ciepły jabłecznik', price=21.0, category='Desery',
                 description='Domowa szarlotka z polskich jabłek, podawana na ciepło z gałką lodów waniliowych'),
        MenuItem(restaurant_id=1, name='Sernik krakowski', price=23.0, category='Desery',
                 description='Puszysty, tradycyjny sernik z rodzynkami i skórką pomarańczową pod aksamitną polewą czekoladową'),
        MenuItem(restaurant_id=1, name='Leniwe na słodko', price=18.0, category='Desery',
                 description='Kluski leniwe z masłem, bułką tartą, cukrem i cynamonem'),

        # Napoje
        MenuItem(restaurant_id=1, name='Kompot owocowy', price=8.0, category='Napoje',
                 description='Tradycyjny, domowy kompot z owoców sezonowych (truskawka, wiśnia, jabłko)'),
        MenuItem(restaurant_id=1, name='Kwas chlebowy', price=12.0, category='Napoje',
                 description='Orzeźwiający, naturalnie fermentowany klasyczny kwas chlebowy'),
        MenuItem(restaurant_id=1, name='Podpiwek warmiński', price=11.0, category='Napoje',
                 description='Tradycyjny, lekko słodki napój zbożowy'),

        # === RESTAURACJA 2: La Bella Italia (Kuchnia Włoska) ===
        # Przystawki
        MenuItem(restaurant_id=2, name='Bruschetta al Pomodoro', price=22.0, category='Przystawki',
                 description='Grzanki z pieczywa domowego z pomidorkami koktajlowymi, czosnkiem, oliwą i świeżą bazylią'),
        MenuItem(restaurant_id=2, name='Carpaccio di Manzo', price=42.0, category='Przystawki',
                 description='Cienkie plastry surowej polędwicy wołowej z rukolą, kaparami, płatkami parmezanu i oliwą cytrynową'),
        MenuItem(restaurant_id=2, name='Caprese della Casa', price=28.0, category='Przystawki',
                 description='Plastry dojrzałych pomidorów i włoskiej mozzarelli di bufala, polane domowym pesto bazyliowym'),
        MenuItem(restaurant_id=2, name='Focaccia Rosmarino', price=18.0, category='Przystawki',
                 description='Wypiekane na miejscu włoskie pieczywo z oliwą z oliwek, grubą solą i świeżym rozmarynem'),

        # Pizza
        MenuItem(restaurant_id=2, name='Pizza Margherita', price=34.0, category='Pizza',
                 description='Klasyczne ciasto, włoski sos pomidorowy, mozzarella fior di latte, świeża bazylia, oliwa'),
        MenuItem(restaurant_id=2, name='Pizza Diavola', price=39.0, category='Pizza',
                 description='Sos pomidorowy, mozzarella, pikantne włoskie salami salami piccante, peperoncino'),
        MenuItem(restaurant_id=2, name='Pizza Quattro Formaggi', price=44.0, category='Pizza',
                 description='Sos biały, mozzarella, gorgonzola, parmezan, ser kozi, świeżo mielony pieprz'),
        MenuItem(restaurant_id=2, name='Pizza Prosciutto e Rucola', price=42.0, category='Pizza',
                 description='Sos pomidorowy, mozzarella, po upieczeniu: szynka dojrzewająca San Daniele, rukola, płatki parmezanu'),
        MenuItem(restaurant_id=2, name='Pizza Capricciosa', price=40.0, category='Pizza',
                 description='Sos pomidorowy, mozzarella fior di latte, szynka gotowana cotto, pieczarki, karczochy, czarne oliwki'),
        MenuItem(restaurant_id=2, name='Pizza Tonno e Cipolla', price=38.0, category='Pizza',
                 description='Sos pomidorowy, mozzarella, tuńczyk, czerwona cebula, kapary'),

        # Makarony
        MenuItem(restaurant_id=2, name='Spaghetti Carbonara', price=38.0, category='Makarony',
                 description='Oryginalny włoski przepis: żółtko, ser Pecorino Romano, chrupiące guanciale i dużo pieprzu'),
        MenuItem(restaurant_id=2, name='Tagliatelle ai Frutti di Mare', price=49.0, category='Makarony',
                 description='Świeży makaron z owocami morza (krewetki, małże, kalmary) w sosie winno-maślanym z pomidorkami'),
        MenuItem(restaurant_id=2, name='Penne Arrabbiata', price=32.0, category='Makarony',
                 description='Pikantny sos pomidorowy z czosnkiem, chili (peperoncino) i natką pietruszki'),
        MenuItem(restaurant_id=2, name='Lasagne Bolognese', price=41.0, category='Makarony',
                 description='Zapiekane płaty makaronu z domowym ragù mięsnym, sosem beszamelowym, mozzarellą i parmezanem'),
        MenuItem(restaurant_id=2, name='Gnocchi ze szpinakiem', price=36.0, category='Makarony',
                 description='Włoskie kopytka w kremowym sosie z dodatkiem liści świeżego szpinaku i sera Gorgonzola'),

        # Sałatki
        MenuItem(restaurant_id=2, name='Sałatka Cezar', price=36.0, category='Sałatki',
                 description='Rzymska sałata, grillowany kurczak, chrupiący boczek, grzanki, płatki parmezanu, kultowy sos Cezar'),

        # Menu dla dzieci
        MenuItem(restaurant_id=2, name='Bambino Spaghetti', price=20.0, category='Dla dzieci',
                 description='Słodkawy, delikatny sos pomidorowy z makaronem i tartym parmezanem'),

        # Desery
        MenuItem(restaurant_id=2, name='Tiramisu Classico', price=24.0, category='Desery',
                 description='Biszkopty nasączone mocnym espresso i likierem Amaretto, przełożone kremem z serka mascarpone'),
        MenuItem(restaurant_id=2, name='Panna Cotta z malinami', price=20.0, category='Desery',
                 description='Waniliowy deser śmietankowy z musem ze świeżych leśnych malin'),
        MenuItem(restaurant_id=2, name='Cannoli Siciliani', price=19.0, category='Desery',
                 description='Chrupiące rurki sycylijskie nadziewane słodkim kremem z sera ricotta z kawałkami czekolady'),

        # Napoje
        MenuItem(restaurant_id=2, name='Woda San Pellegrino', price=14.0, category='Napoje',
                 description='Naturalna włoska woda gazowana premium (butelka 750ml)'),
        MenuItem(restaurant_id=2, name='Lemoniada Sycylijska', price=15.0, category='Napoje',
                 description='Domowa, mocno cytrynowa lemoniada ze świeżych cytrusów z dodatkiem mięty'),
        MenuItem(restaurant_id=2, name='Espresso', price=9.0, category='Napoje',
                 description='Klasyczny, intensywny napar ze świeżo mielonych ziaren włoskiej Arabiki')
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