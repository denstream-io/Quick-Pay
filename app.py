from flask import Flask, request, jsonify, render_template
import re

app = Flask(__name__)

cart = []

@app.route('/')
def index():
    """
    Renders the main page with a form to display scanned data.
    """
    return render_template('index.html')

@app.route('/scanned_qr', methods=['GET'])
def scanned_qr():
    # Get data from query parameters
    symbol = request.args.get('symbol', '')
    shares = request.args.get('shares', '')
    price = request.args.get('price', '')
    
    # Render the form page with pre-filled data
    return render_template('scanned_qr.html', symbol=symbol, shares=shares, price=price)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    # Process form data
    symbol = request.form.get('symbol')
    shares = request.form.get('shares')
    price = request.form.get('price')

    # Validate inputs
    if not symbol or not shares or not price:
        return "Invalid input!", 400

    # Add to cart
    cart.append({
        'symbol': symbol,
        'shares': int(shares),
        'price': float(price)
    })

    # Redirect to cart or send success response
    return f"Added {symbol} ({shares} shares at ${price}) to the cart!"



if __name__ == '__main__':
    app.run(debug=True)
