from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = 'knr_stylo_hub_secret_key_2026'

# Database setup
DATABASE = os.path.join(os.path.dirname(__file__), 'users.db')

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users 
                   (username TEXT PRIMARY KEY, password TEXT)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS orders 
                   (id INTEGER PRIMARY KEY, username TEXT, items TEXT, total REAL, date TIMESTAMP)''')
    conn.commit()
    conn.close()

# ✅ IMPORTANT: Initialize DB for Render
init_db()

# Products
PRODUCTS = {
    "1": {"name": "Shirt", "price": 500, "emoji": "👕", "image": "shirt.jpg"},
    "2": {"name": "Shoes", "price": 1200, "emoji": "👞", "image": "ryan.jpg"},
    "3": {"name": "Watch", "price": 800, "emoji": "⌚", "image": "Watch.jpg"},
    "4": {"name": "Bag", "price": 700, "emoji": "👜", "image": "Bag.avif"}
}

# Login check
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db()
        cur = conn.cursor()
        
        try:
            cur.execute('INSERT INTO users VALUES (?, ?)', (username, password))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            conn.close()
            return render_template('register.html', error='Username already exists')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db()
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
        user = cur.fetchone()
        conn.close()
        
        if user:
            session['username'] = username
            session['cart'] = []
            return redirect(url_for('shop'))
        else:
            return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@app.route('/shop')
@login_required
def shop():
    return render_template('index.html', products=PRODUCTS)

@app.route('/add-to-cart', methods=['POST'])
@login_required
def add_to_cart():
    product_id = request.form.get('product_id')
    
    if 'cart' not in session:
        session['cart'] = []
    
    cart_item = next((item for item in session['cart'] if item['id'] == product_id), None)
    
    if cart_item:
        cart_item['quantity'] += 1
    else:
        product = PRODUCTS.get(product_id)
        if product:
            session['cart'].append({
                'id': product_id,
                'name': product['name'],
                'price': product['price'],
                'image': product['image'],
                'quantity': 1
            })
    
    session.modified = True
    return redirect(url_for('view_cart'))

@app.route('/cart')
@login_required
def view_cart():
    if 'cart' not in session:
        session['cart'] = []
    
    total = sum(item['price'] * item['quantity'] for item in session['cart'])
    return render_template('cart.html', cart=session['cart'], total=total)

@app.route('/remove-from-cart', methods=['POST'])
@login_required
def remove_from_cart():
    product_id = request.form.get('product_id')
    
    if 'cart' in session:
        session['cart'] = [item for item in session['cart'] if item['id'] != product_id]
        session.modified = True
    
    return redirect(url_for('view_cart'))

@app.route('/checkout', methods=['POST'])
@login_required
def checkout():
    if 'cart' not in session or len(session['cart']) == 0:
        return redirect(url_for('view_cart'))
    
    cart = session['cart']
    total = sum(item['price'] * item['quantity'] for item in cart)
    
    items_str = ', '.join([f"{item['name']} x{item['quantity']}" for item in cart])
    username = session['username']
    
    conn = get_db()
    cur = conn.cursor()
    cur.execute('INSERT INTO orders (username, items, total, date) VALUES (?, ?, ?, datetime("now"))',
                (username, items_str, total))
    conn.commit()
    conn.close()
    
    session['cart'] = []
    session.modified = True
    
    return render_template('bill.html', cart=cart, total=total)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Local run only
if __name__ == '__main__':
    app.run(debug=True)