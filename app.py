import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database setup
def init_db():
    with sqlite3.connect('app.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT UNIQUE NOT NULL,
                            email TEXT UNIQUE NOT NULL,
                            password TEXT NOT NULL
                        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS items (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            price REAL NOT NULL
                        )''')
        conn.commit()

        # Seed items data
        cursor.execute('SELECT COUNT(*) FROM items')
        if cursor.fetchone()[0] == 0:
            items = [("Apple", 0.5), ("Banana", 0.3), ("Orange", 0.8)]
            cursor.executemany('INSERT INTO items (name, price) VALUES (?, ?)', items)
            conn.commit()

# Initialize the database
init_db()

# Helper functions
def get_user_by_username_or_email(identifier):
    with sqlite3.connect('app.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? OR email = ?', (identifier, identifier))
        return cursor.fetchone()

def add_user(username, email, password):
    with sqlite3.connect('app.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                       (username, email, password))
        conn.commit()

@app.route('/')
def index():
    if 'user_id' not in session:
        flash('You must be logged in to access the index page.', 'danger')
        return redirect(url_for('login'))

    username = session['username']
    return render_template('index.html', username=username)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if not username or not email or not password:
            flash('All fields are required.', 'danger')
            return redirect(url_for('register'))

        if get_user_by_username_or_email(username) or get_user_by_username_or_email(email):
            flash('User with this username or email already exists.', 'warning')
            return redirect(url_for('register'))

        add_user(username, email, password)
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_or_email = request.form['username_or_email']
        password = request.form['password']

        user = get_user_by_username_or_email(username_or_email)

        if user and user[3] == password:  # user[3] is the password column
            session['user_id'] = user[0]  # user[0] is the id column
            session['username'] = user[1]  # user[1] is the username column
            flash('Logged in successfully.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

@app.route('/items')
def items():
    with sqlite3.connect('app.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM items')
        items = cursor.fetchall()

    # Convert tuples to dictionaries
    items = [{'id': item[0], 'name': item[1], 'price': item[2]} for item in items]
    
    return render_template('items.html', items=items)


@app.route('/add_to_cart/<int:item_id>', methods=['POST'])
def add_to_cart(item_id):
    if 'user_id' not in session:
        flash('You must be logged in to add items to the cart.', 'danger')
        return redirect(url_for('login'))

    if 'cart' not in session:
        session['cart'] = []

    with sqlite3.connect('app.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM items WHERE id = ?', (item_id,))
        item = cursor.fetchone()

    if item:
        session['cart'].append({'id': item[0], 'name': item[1], 'price': item[2]})
        flash(f'{item[1]} added to cart.', 'success')
    else:
        flash('Item not found.', 'danger')

    return redirect(url_for('cart'))


@app.route('/cart')
def cart():
    if 'user_id' not in session:
        flash('You must be logged in to view the cart.', 'danger')
        return redirect(url_for('login'))

    cart = session.get('cart', [])
    total_price = sum(item['price'] for item in cart)
    return render_template('cart.html', cart=cart, total_price=total_price)

@app.route('/remove_from_cart/<int:item_id>', methods=['POST'])
def remove_from_cart(item_id):
    if 'cart' in session:
        session['cart'] = [item for item in session['cart'] if item['id'] != item_id]
        flash('Item removed from cart.', 'info')
    return redirect(url_for('cart'))

@app.route('/qr_cart/<int:item_id>', methods=['GET'])
def qr_cart(item_id):

    if 'user_id' not in session:
        flash('You must be logged in to view the cart.', 'danger')
        return redirect(url_for('login'))


    # Get data from query parameters
    # id = int(request.args.get('id', ''))

    with sqlite3.connect('app.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM items WHERE id = ?', (item_id,))
        item = cursor.fetchone()
        # Transform tuples into dictionaries for easier access in templates
        items = {'id': item[0], 'name': item[1], 'price': item[2]}
        
    # Render the form page with pre-filled data
    return render_template('qr_cart.html', items=items)

@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403

if __name__ == '__main__':
    app.run(debug=True)




# @app.route('/qr_cart', methods=['GET'])
# def scanned_qr():
#     # Get data from query parameters
#     id = request.args.get('id', '')
#     item = request.args.get('item', '')
#     symbol = request.args.get('symbol', '')
#     shares = request.args.get('shares', '')
#     price = request.args.get('price', '')
    
    
#     # Render the form page with pre-filled data
#     return render_template('qr_cart.html', symbol=symbol, shares=shares, price=price, id=id, item=item)

# @app.route('/add_to_cart', methods=['POST'])
# def add_to_cart():
#     # Process form data

#     id = request.form.get('id')
#     item = request.form.get('item')
#     symbol = request.form.get('symbol')
#     shares = request.form.get('shares')
#     price = request.form.get('price')
    


#     # Validate inputs
#     if not symbol or not shares or not price:
#         return "Invalid input!", 400

#     # Add to cart
#     cart.append({
#         'symbol': symbol,
#         'shares': int(shares),
#         'price': float(price)
#     })

#     # Redirect to cart or send success response
#     return f"Added {symbol} ({shares} shares at ${price}) to the cart!"

# if __name__ == '__main__':
#     app.run(debug=True)
