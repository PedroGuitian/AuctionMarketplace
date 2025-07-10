# Auction Marketplace

A fully functional online auction marketplace built with Django. Inspired by modern platforms like OfferUp, this app allows users to create listings, place bids, comment, and manage watchlists — all with a clean, modern, and responsive design.

---

## Features

- User authentication (register, login, logout)
- Create and manage auction listings
- Upload images and set categories
- Place bids on active listings
- Automatic winner selection when closing auctions
- Watchlist to track favorite items
- Commenting system for each listing
- Sold listings history for sellers
- Clean, responsive, modern UI

---

## Tech Stack

- **Backend**: Django
- **Frontend**: HTML, CSS (custom, Bootstrap 4), JavaScript
- **Database**: SQLite (default Django database)

---

## Setup & Run Locally

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/PedroGuitian/AuctionMarketplace.git
   cd AuctionMarketplace
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

