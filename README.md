# Foodie: E-commerce Platform for Food Items

Foodie is an online marketplace for food lovers, built using Django and PostgreSQL, following the MVT (Model-View-Template) architecture. It provides a seamless experience for users to browse, search, and purchase food items while offering an intuitive admin panel for managing products, orders, and discounts.

## Features
- **User Authentication**: Email OTP-based login and registration.
- **Admin Management**: Admin panel to manage food items, categories, users, and orders.
- **Food Listings**: Display food items with categories, filtering, and search functionality.
- **Cart and Checkout**: Add food items to cart, apply coupons, and proceed to checkout.
- **Wallet-based Payments**: Users can make purchases using their wallet balance.
- **Razorpay Integration**: Secure online payment gateway for transactions.
- **Order Tracking**: View order history and track order status.
- **Deployment**: Hosted on AWS EC2 with Nginx as a reverse proxy.

## Installation and Setup

### 1. Clone the Repository
```sh
git clone https://github.com/Elbin12/Foodie-website.git
```

### 2. Set Up a Virtual Environment
```sh
python3 -m venv env
source venv/bin/activate
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory and add:

```env
CALLBACK_URL=http://localhost:8000
```

### 5. Apply Database Migrations
```sh
python manage.py migrate
python manage.py createsuperuser  # Create an admin user
```

### 6. Run the Development Server
```sh
python manage.py runserver
```
Access the app at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

## Deployment on AWS EC2

### 1. Install Dependencies on the EC2 Instance
```sh
sudo apt update && sudo apt install -y python3-pip python3-venv nginx
```

### 2. Clone the Repository & Set Up Virtual Environment
```sh
git clone https://github.com/Elbin12/Foodie-website.git
python3 -m venv env
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure Gunicorn
```sh
gunicorn --bind 0.0.0.0:8000 Foodie.wsgi:application
```

### 4. Set Up Nginx Reverse Proxy
Configure `/etc/nginx/sites-available/foodie` with:

```nginx
server {
    listen 80;
    server_name your_domain_or_IP;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

Enable the site and restart Nginx:
```sh
sudo ln -s /etc/nginx/sites-available/foodie /etc/nginx/sites-enabled
sudo systemctl restart nginx
```

## Future Enhancements
- Implement a recommendation engine for personalized food suggestions.
- Introduce user reviews and ratings for food items.
- Add social login support (Google, Facebook, etc.).
- Enhance UI/UX with modern design improvements.

## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests.