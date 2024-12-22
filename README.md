# QR Code Scanner with Flask and Auto-Filled Form

## Overview
This project implements a web application using Flask and JavaScript that:
1. Scans QR codes containing stock information.
2. Redirects users to a form page with pre-filled data from the scanned QR code.
3. Allows users to add the stock information to a cart by submitting the form.

### Features
- **QR Code Scanning:** Uses `Html5Qrcode` for efficient QR code scanning.
- **Auto-find Stock:** Automatically extracts stock id to find stock details.
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
   git clone https://github.com/Quick-Pay.git
   cd Quick-Pay
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

