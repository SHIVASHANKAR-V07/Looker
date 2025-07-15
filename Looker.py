from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'this_791'

def init_users_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def init_orders_db():
    with sqlite3.connect("orders.db") as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT,
                phone TEXT,
                address TEXT,
                items TEXT,
                total_price INTEGER,
                created_at TEXT
            )
        ''')
    conn.commit()        
    conn.close()

init_users_db()
init_orders_db()

@app.route('/')
def home_page():
    return render_template('Looker_Home.htm')

def get_user(email):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = c.fetchone()
    conn.close()
    return user

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = get_user(email)
        if user and user[2] == password:
            session['user'] = email
            flash('Logged in successfully!', 'success')
            return redirect(url_for('home_page'))
        else:
            flash('Invalid credentials!', 'error')
            return redirect(url_for('signin'))
    return render_template('Looker_Signin.htm')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, password))
            conn.commit()
            flash('Account created! Please log in.', 'success')
            return redirect(url_for('signin'))
        except sqlite3.IntegrityError:
            flash('Email already exists.', 'error')
            return redirect(url_for('signup'))
        finally:
            conn.close()
    return render_template('Looker_Signup.htm')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out successfully!', 'info')
    return redirect(url_for('home_page'))

@app.route('/add_to_cart/<product_id>', methods=['POST'])
def add_to_cart(product_id):
    quantity = int(request.form.get('quantity', 1))
    quantity = min(quantity, 10)
    
    products = {
        "1": {"name": "Blue Shirt", "price": 399},
        "2": {"name": "Grey Hoodie", "price": 499},
        "3": {"name": "Formal Pant", "price": 699},
        "4": {"name": "Track Pant", "price": 359}
    }
    
    product = products.get(product_id)
    if not product:
        return "Product not found", 404

    cart = session.get('cart', {})
    if product_id in cart:
        cart[product_id]['quantity'] = min(cart[product_id]['quantity'] + quantity, 10)
    else:
        cart[product_id] = {
            'name': product['name'],
            'price': product['price'],
            'quantity': quantity
        }

    session['cart'] = cart
    #flash(f"Added {quantity} x {product['name']} to cart.")
    return redirect(url_for('home_page'))

@app.route('/remove_from_cart/<product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    if product_id in cart:
        del cart[product_id]
        session['cart'] = cart
        #flash("Item removed from cart.")
    return redirect(url_for('buy_now'))

@app.route('/buy_now')
def buy_now():
    if 'user' not in session:
        flash("Please signin to place an order.")
        return redirect(url_for('signin'))

    cart = session.get('cart', {})
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    return render_template('Cart.htm', cart=cart, total=total)

@app.route('/place_order', methods=['POST'])
def place_order():
    if 'user' not in session:
        return redirect(url_for('signin'))

    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    address = f"{request.form['door']}, {request.form['street']}, {request.form['city']}, {request.form['district']}, {request.form['state']}"
    cart = session.get('cart', {})
    items_str = "; ".join([f"{v['quantity']} x {v['name']}" for v in cart.values()])
    total_price = sum(v['price'] * v['quantity'] for v in cart.values())

    with sqlite3.connect("orders.db") as conn:
        c = conn.cursor()
        c.execute("INSERT INTO orders (name, email, phone, address, items, total_price, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (name, email, phone, address, items_str, total_price, datetime.now()))
        conn.commit()

    session.pop('cart', None)
    return render_template("Orders.htm")

@app.route('/shirt_1')
def blue_shirt():
    return render_template('Blue_shirt.htm')

@app.route('/shirt_2')
def grey_hoodie():
    return render_template('Grey_hoodie.htm')

@app.route('/pant_1')
def formal_pant():
    return render_template('Formal_pant.htm')

@app.route('/pant_2')
def track_pant():
    return render_template("Track_pant.htm")

if __name__ == '__main__':
    app.run(debug=True)
