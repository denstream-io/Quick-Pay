# QuickPay: Revolutionizing In-Store Shopping

<div style="text-align: center;">
  <img src="./static/qr_code.png" alt="image of qr code" width="300"/>
</div>

## Inspiration 
Shopping should be easy and convenient. No one likes to have their receipt scrutinized after making a purchase, a common practice at large superstores and chain markets. We aim to eliminate the hassle of multiple steps and unnecessary checks. Our goal is to make the in-store shopping experience smoother, faster, and better.

## What it does
QuickPay simplifies the shopping process by combining scanning, video conferencing, and screen sharing. No more juggling between different apps:
- **Scan the item**: Simply scan the barcode to view product details and ensure you’re buying the right item.
- **Video Conferencing/Screen Share**: Consult a friend or family member instantly to check if it’s the right product, without leaving the app. 
- **Real-time Calculations**: Keep track of your total price as you shop, preventing surprises at checkout when a product is mismarked. No need for a staff member to recheck the price and adjust it later.

With QuickPay, you can do everything in one seamless experience. Say goodbye to using FaceTime for advice, switching between apps to verify purchases, and dealing with price surprises at checkout.

## How we built it
We built QuickPay using a combination of technologies:
- **Python & Flask**: For backend development and QR code functionality.
- **JavaScript & Bootstrap**: To create an interactive and responsive front-end.
- **HTML & CSS**: For clean, functional, and user-friendly design.

## Challenges we ran into
One of the major challenges was redirecting to the stock details page after scanning the QR code. It required a robust backend to ensure smooth transitions between pages and features, while maintaining the speed and accuracy of item scanning.

## Accomplishments we're proud of
We’re proud to have developed a fully functional product with a complete prototype and mockups. The system works seamlessly, integrating login, log out, scanning, add to cart, and remove from cart features.

## What we learned
Through this project, we discovered how different languages are integrated together to solve various real-world problems and how technology can make life easier practically. QuickPay is designed to benefit both the financial and tech industries by streamlining in-store purchases, saving time, and reducing errors.

## What's next for QuickPay
We’re excited to take QuickPay to the next level by integrating video conference, screen sharing features and real-time price update - all in one app. We plan to refine the product further, expand its reach, and revolutionize the way people shop. Together, we can make shopping easier, better, and more enjoyable for everyone.

Let's build a future where shopping is as convenient as it should be.

## Overview
This project implements a web application using Flask and JavaScript that:
1. Scans QR codes containing stock id.
2. Redirects users to a page with stock details  from the scanned QR code.
3. Allows users to add the stock to a cart.

### Features
- **QR Code Scanning:** Uses `Html5Qrcode` for efficient QR code scanning.
- **Auto-find Stock:** Automatically extracts stock id to find stock details.
- **Add to Cart:** Allows users to confirm the data and add it cart.

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

## License
This project is open-source and available under the [MIT License](LICENSE).

---

## Acknowledgments
- [Html5Qrcode](https://github.com/mebjas/html5-qrcode): A robust library for QR code scanning in web applications.

