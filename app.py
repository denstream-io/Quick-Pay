import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'hsjeyrndbshjsksjdhegjsgsgsnsbsge'  # Secret key for session management and secure cookies.

# Database setup
def init_db():
    """
    Initializes the SQLite database. 
    Creates `users` and `items` tables if they do not exist.
    Seeds the `items` table with default data if it's empty.
    """
    with sqlite3.connect('app.db') as conn:
        cursor = conn.cursor()
        # Create `users` table to store user information.
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT UNIQUE NOT NULL,
                            email TEXT UNIQUE NOT NULL,
                            password TEXT NOT NULL
                        )''')
        # Create `items` table to store product data.
        cursor.execute('''CREATE TABLE IF NOT EXISTS items (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            price REAL NOT NULL
                        )''')
        conn.commit()

        # Seed the `items` table with default data if it is empty.
        cursor.execute('SELECT COUNT(*) FROM items')
        if cursor.fetchone()[0] == 0:
            items = [("Apple", 0.5), ("Banana", 0.3), ("Orange", 0.8)]
            cursor.executemany('INSERT INTO items (name, price) VALUES (?, ?)', items)
            conn.commit()

# Initialize the database at the start of the application.
init_db()

# Helper functions
def get_user_by_username_or_email(identifier):
    """
    Fetches a user from the `users` table by username or email.
    :param identifier: Username or email to search for.
    :return: User record or None if no match is found.
    """
    with sqlite3.connect('app.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? OR email = ?', (identifier, identifier))
        return cursor.fetchone()

def add_user(username, email, password):
    """
    Adds a new user to the `users` table.
    :param username: The user's username.
    :param email: The user's email.
    :param password: The user's password.
    """
    with sqlite3.connect('app.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                       (username, email, password))
        conn.commit()

@app.route('/')
def index():
    """
    Renders the homepage. Redirects to login if the user is not logged in.
    """
    if 'user_id' not in session:
        flash('You must be logged in to access the index page.', 'danger')
        return redirect(url_for('login'))

    username = session['username']  # Get the logged-in user's username from the session.
    return render_template('index.html', username=username)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handles user registration. 
    Displays the registration form and processes new user sign-ups.
    """
    if request.method == 'POST':
        # Collect form data
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Ensure all fields are filled
        if not username or not email or not password:
            flash('All fields are required.', 'danger')
            return redirect(url_for('register'))

        # Check if username or email already exists
        if get_user_by_username_or_email(username) or get_user_by_username_or_email(email):
            flash('User with this username or email already exists.', 'warning')
            return redirect(url_for('register'))

        # Add the user to the database
        add_user(username, email, password)
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')  # Render the registration form.

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handles user login. 
    Verifies credentials and starts a session for the user.
    """
    if request.method == 'POST':
        # Collect form data
        username_or_email = request.form['username_or_email']
        password = request.form['password']

        # Fetch user by username or email
        user = get_user_by_username_or_email(username_or_email)

        # Check credentials
        if user and user[3] == password:  # user[3] is the password column
            session['user_id'] = user[0]  # user[0] is the id column
            session['username'] = user[1]  # user[1] is the username column
            flash('Logged in successfully.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')  # Render the login form.

@app.route('/logout')
def logout():
    """
    Logs the user out by clearing the session data.
    """
    session.pop('user_id', None)
    session.pop('username', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

@app.route('/items')
def items():
    """
    Displays a list of all items available in the `items` table.
    """
    with sqlite3.connect('app.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM items')
        items = cursor.fetchall()

    # Convert tuples to dictionaries for easier handling in templates.
    items = [{'id': item[0], 'name': item[1], 'price': item[2]} for item in items]

    return render_template('items.html', items=items)

@app.route('/add_to_cart/<int:item_id>', methods=['POST'])
def add_to_cart(item_id):
    """
    Adds an item to the user's cart, stored in the session.
    Redirects to the login page if the user is not logged in.
    """
    if 'user_id' not in session:
        flash('You must be logged in to add items to the cart.', 'danger')
        return redirect(url_for('login'))

    if 'cart' not in session:
        session['cart'] = []  # Initialize an empty cart in the session.

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
    """
    Displays the items in the user's cart and calculates the total price.
    Redirects to the login page if the user is not logged in.
    """
    if 'user_id' not in session:
        flash('You must be logged in to view the cart.', 'danger')
        return redirect(url_for('login'))

    cart = session.get('cart', [])
    total_price = sum(item['price'] for item in cart)  # Calculate total price of items in the cart.
    return render_template('cart.html', cart=cart, total_price=total_price)

@app.route('/remove_from_cart/<int:item_id>', methods=['POST'])
def remove_from_cart(item_id):
    """
    Removes an item from the user's cart by its ID.
    """
    if 'cart' in session:
        # Filter out the item to be removed.
        session['cart'] = [item for item in session['cart'] if item['id'] != item_id]
        flash('Item removed from cart.', 'info')
    return redirect(url_for('cart'))

@app.route('/qr_cart/<int:item_id>', methods=['GET'])
def qr_cart(item_id):
    """
    Displays a QR code page or item details for the specified item.
    Redirects to the login page if the user is not logged in.
    """
    if 'user_id' not in session:
        flash('You must be logged in to view the cart.', 'danger')
        return redirect(url_for('login'))

    with sqlite3.connect('app.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM items WHERE id = ?', (item_id,))
        item = cursor.fetchone()

        # Transform tuple into dictionary for easier access in templates.
        items = {'id': item[0], 'name': item[1], 'price': item[2]}

    # Render the form page with pre-filled data.
    return render_template('qr_cart.html', items=items)


if __name__ == '__main__':
    # Start the Flask application in debug mode for development.
    app.run(debug=True)