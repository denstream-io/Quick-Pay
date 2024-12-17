# QR Code Scanner with Flask and Auto-Filled Form

## Overview
This project implements a web application using Flask and JavaScript that:
1. Scans QR codes containing stock information.
2. Redirects users to a form page with pre-filled data from the scanned QR code.
3. Allows users to add the stock information to a cart by submitting the form.

### Features
- **QR Code Scanning:** Uses `Html5Qrcode` for efficient QR code scanning.
- **Auto-filled Form:** Automatically extracts stock symbol, number of shares, and stock price from the QR code and pre-fills the form.
- **Add to Cart:** Allows users to confirm the data and add it to an in-memory cart.

---

## Requirements

### Backend
- Python 3.7+
- Flask

### Frontend
- HTML5 and JavaScript
- `Html5Qrcode` library

---

## Installation and Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo-name.git
   cd your-repo-name
   ```

2. Set up a virtual environment (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install flask
   ```

4. Run the Flask application:
   ```bash
   python app.py
   ```

5. Open the app in your browser:
   ```
   http://127.0.0.1:5000/
   ```

---

## File Structure

```plaintext
.
├── app.py                # Flask backend application
├── templates/
│   ├── index.html        # QR code scanning page
│   ├── scanned_qr.html    # Auto-filled form page
├── static/               # Static files like CSS or JS
└── README.md             # Project documentation
```

---

## Workflow

### 1. QR Code Scanning
- **File:** `index.html`
- The user scans a QR code using the `Html5Qrcode` library.
- Example QR code format: `/stock/AAPL/10/145.23`
- The scanned data is parsed into:
  - `symbol`: Stock symbol (e.g., `AAPL`)
  - `shares`: Number of shares (e.g., `10`)
  - `price`: Stock price (e.g., `145.23`)

### 2. Redirect to Form Page
- After a successful scan, the app redirects to `/scanned_qr` with the scanned values passed as query parameters.

### 3. Pre-filled Form
- **File:** `scanned_qr.html`
- Displays the stock details (symbol, shares, price) in a read-only form.
- The user can confirm the details and click "Add to Cart."

### 4. Add to Cart
- **Route:** `/add_to_cart`
- The form data is submitted via a POST request.
- The backend processes the data and adds it to an in-memory cart.

---

## Example QR Code Data
- Example QR code string:
  ```
  /stock/AAPL/10/145.23
  ```
  - **symbol:** `AAPL`
  - **shares:** `10`
  - **price:** `145.23`

---

## Routes

### `/` (GET)
- Displays the QR code scanning page.

### `/scanned_qr` (GET)
- Redirects to the form page with pre-filled data from the QR code.
- Query Parameters:
  - `symbol`: Stock symbol
  - `shares`: Number of shares
  - `price`: Stock price

### `/add_to_cart` (POST)
- Processes the form submission and adds the data to an in-memory cart.

---

## Future Improvements
- Integrate a database to store cart data persistently.
- Enhance error handling for invalid QR codes.
- Add a dedicated cart page to display the added items.
- Implement user authentication for personalized cart management.

---

## License
This project is open-source and available under the [MIT License](LICENSE).

---

## Acknowledgments
- [Html5Qrcode](https://github.com/mebjas/html5-qrcode): A robust library for QR code scanning in web applications.

