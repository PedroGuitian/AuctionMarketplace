# Commerce

This is Project 2 of Harvard's CS50 Web Programming with Python and JavaScript (CS50W). It is a basic eBay-style e-commerce platform built using Django and Python.

## Features

- **User Registration & Login**: Users can create accounts, log in, and log out
- **Auction Listings**: Authenticated users can create new auction listings with a title, description, starting bid, optional image URL, and category
- **Bidding System**: Users can place bids; the highest bid is tracked
- **Watchlist**: Users can add or remove listings from their watchlist and view it at any time
- **Comments**: Users can comment on active listings
- **Auction Closing**: The user who created a listing can close the auction, at which point the highest bidder wins
- **Category View**: Users can browse listings by category
- **Sold Listings**: Closed listings with a winner are displayed separately

## Technologies Used

- Python 3
- Django
- SQLite
- HTML
- CSS

## Getting Started

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/commerce.git
   cd commerce
2. **Apply database migrations**
   ```bash
   python manage.py migrate
3. **Create a superuser (optional for admin access)**
    ```bash
    python manage.py createsuperuser
4. **Run the development server**
   ```bash
   python manage.py runserver
5. **Visit the application**
   Open your browser and go to: http://127.0.0.1:8000/

