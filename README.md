# 🛒 NovaStore - Simple E-Commerce Store

[![CodeAlpha Internship](https://img.shields.io/badge/CodeAlpha-Web%20Development%20Internship-blue.svg)](https://www.codealpha.tech)
[![Task](https://img.shields.io/badge/Task-Task%201%3A%20Simple%20E--Commerce%20Store-indigo.svg)](https://www.codealpha.tech)
[![Python](https://img.shields.io/badge/Python-3.13-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.1.6-darkgreen.svg?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Database](https://img.shields.io/badge/Database-SQLite3-003B57.svg?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Frontend](https://img.shields.io/badge/Frontend-HTML5%20%7C%20CSS3%20%7C%20Vanilla%20JS-orange.svg)](#frontend-features)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](#license)

> Developed as part of the **CodeAlpha Web Development Internship** ([www.codealpha.tech](https://www.codealpha.tech)).  
> **Task 1: Simple E-Commerce Store** — A modern, responsive, and full-featured e-commerce platform built with Django (Python), SQLite, and vanilla frontend technologies.

---

## 🌟 Live Demo & Quick Links

- 🌐 **Internship Portal**: [https://www.codealpha.tech](https://www.codealpha.tech)
- 💻 **GitHub Repository**: [https://github.com/Harika3560123/CodeAlpha_Ecommerce_Store](https://github.com/Harika3560123/CodeAlpha_Ecommerce_Store)
- 🚀 **Pre-seeded Admin Dashboard**: `http://127.0.0.1:8000/admin/`

---

## 🎯 Task Requirements & Implemented Features

| Requirement | Implemented Feature Description | Status |
| :--- | :--- | :---: |
| **Product Listings** | Interactive catalog with live search, category filtering, sort by price/rating/date, discount tags, and pagination | ✅ Completed |
| **Product Details Page** | Full details view with image preview, price comparisons, stock tracking, specs, quantity limits & related items | ✅ Completed |
| **Shopping Cart** | Dynamic AJAX add-to-cart, +/- quantity controls without page reload, subtotal, tax calculation & free shipping tracker | ✅ Completed |
| **Order Processing** | Multi-step checkout, shipping address capture, payment options (COD, Card, UPI), and automated order receipts | ✅ Completed |
| **User Registration / Login** | Session-based authentication, user profile management, orders history, and 1-click evaluator login buttons | ✅ Completed |
| **Relational Database** | SQLite database schema with Category, Product, Cart, CartItem, Order, OrderItem, and UserProfile models | ✅ Completed |
| **Deployment Ready** | Production configuration with WhiteNoise static assets, Gunicorn, `render.yaml`, `Procfile`, and `vercel.json` | ✅ Completed |

---

## 🔑 Pre-Configured Demo Credentials

For swift testing and evaluator review, the database comes pre-seeded with ready-to-use accounts:

| Role | Username | Password | Access Level |
| :--- | :--- | :--- | :--- |
| **Store Administrator** | `admin` | `admin123` | Full Django Admin & store catalog control |
| **Demo Customer** | `customer` | `customer123` | Cart, customer profile & past order history |

*(Tip: Both the Login and Checkout pages include a **1-Click Auto-Fill** button to test without manual typing!)*

---

## 📸 Key Pages & Visual Flow

1. **Storefront & Catalog (`/`)**:
   - Hero spotlight banner with internship announcement.
   - Category filtering (Electronics, Fashion, Home & Lifestyle, Accessories).
   - Product cards with discount badges (`-20% OFF`), star ratings, price, and instant AJAX "Add to Cart".

2. **Product Details (`/product/<slug>/`)**:
   - High-resolution product showcase.
   - Pricing comparison with original price strikethrough.
   - Bulleted specifications, stock countdown, quantity selector (+/-).
   - Instant "Add to Cart" and "Buy Now" checkout shortcut.
   - Related products in the same category.

3. **Shopping Cart (`/cart/`)**:
   - Dynamic quantity adjustment with real-time AJAX total recalculation.
   - Free shipping progress bar (Free for orders over $50).
   - Promo code simulator (e.g. `CODEALPHA10`).
   - Order summary box: Subtotal, 5% Estimated Tax, Shipping, Grand Total.

4. **Checkout & Order Processing (`/checkout/` -> `/order/process/`)**:
   - 3-step checkout stepper (Cart ➜ Checkout ➜ Confirmation).
   - 1-click "Auto-Fill Demo Details" button.
   - Shipping address and customer phone verification.
   - Payment method selection: Cash on Delivery (COD), Credit/Debit Card, UPI.
   - Automatic stock inventory deduction upon placement.

5. **Order Confirmation & Tracking (`/order/success/<order_number>/` & `/orders/`)**:
   - Celebratory order confirmation screen.
   - Unique order ID generation (`#ORD-XXXXXXXX`).
   - Print-ready invoice receipt with print button (`window.print()`).
   - Visual order fulfillment tracker timeline: Placed ➔ Confirmed ➔ Shipped ➔ Delivered.

6. **Authentication & Profile (`/register/`, `/login/`, `/profile/`)**:
   - Form validation with flash toast feedback.
   - Customer shipping address synchronization.
   - Past order history dashboard.

7. **Admin Dashboard (`/admin/`)**:
   - Complete inventory and sales control over Categories, Products, Carts, Orders, and Users.

---

## 🏗️ Technology Stack

- **Backend**: Python 3.13, Django 5.1
- **Database**: SQLite3 (zero external driver dependencies, lightweight & ACID compliant)
- **Frontend**: HTML5, CSS3, Modern Bootstrap 5.3, Bootstrap Icons, Vanilla JavaScript (Fetch API / AJAX)
- **Static Assets Serving**: WhiteNoise 6.12 (compressed production asset pipeline)
- **WSGI Production Server**: Gunicorn 23.0
- **Deployment Blueprints**: Render (`render.yaml`), Heroku/Railway (`Procfile`), Vercel (`vercel.json`)

---

## 📁 Project Directory Structure

```text
c:\codealpha\project1\
├── ecommerce_project/          # Django Project Root Configuration
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py             # Settings, WhiteNoise, Context Processors & Auth
│   ├── urls.py                 # Root URL routing
│   └── wsgi.py                 # WSGI application entrypoint
├── store/                      # Core E-Commerce Application
│   ├── migrations/             # Database migrations
│   ├── admin.py                # Django Admin models configuration
│   ├── apps.py
│   ├── context_processors.py   # Global cart counter & category navigation
│   ├── forms.py                # Registration, Login, Profile & Checkout forms
│   ├── models.py               # Category, Product, Cart, CartItem, Order, OrderItem
│   ├── tests.py                # Automated test suite (6 passing test cases)
│   ├── urls.py                 # Store endpoints routing
│   └── views.py                # Business logic & AJAX endpoints
├── templates/                  # Frontend HTML Templates
│   ├── base.html               # Main layout, navbar, footer & toast system
│   └── store/
│       ├── home.html           # Storefront catalog & hero section
│       ├── product_detail.html # Product details page
│       ├── cart.html           # Dynamic shopping cart
│       ├── checkout.html       # Order checkout & payment selection
│       ├── order_success.html  # Order confirmation & receipt
│       ├── order_history.html  # Customer orders dashboard
│       ├── order_detail.html   # Detailed order tracker
│       ├── login.html          # Login page with 1-click evaluator login
│       ├── register.html       # Signup page with 1-click autofill
│       ├── profile.html        # Account & shipping settings
│       ├── about.html          # CodeAlpha task overview
│       └── contact.html        # Support & FAQs
├── static/                     # Static Assets
│   ├── css/
│   │   └── custom.css          # Modern custom design system stylesheet
│   └── js/
│       └── main.js             # AJAX cart, toast engine, demo fillers
├── db.sqlite3                  # Pre-seeded database with 16 products & demo users
├── seed_data.py                # Automated database population script
├── requirements.txt            # Python dependencies
├── runtime.txt                 # Python runtime version
├── Procfile                    # Web process command for cloud PaaS
├── render.yaml                 # 1-Click Render deployment blueprint
├── vercel.json                 # Vercel deployment configuration
├── .gitignore                  # Git ignore rules
└── README.md                   # Comprehensive documentation
```

---

## 🚀 Local Installation & Setup Guide

Follow these simple steps to run NovaStore on your local machine:

### 1. Clone the Repository
```bash
git clone https://github.com/Harika3560123/CodeAlpha_Ecommerce_Store.git
cd CodeAlpha_Ecommerce_Store
```

### 2. Create and Activate a Virtual Environment
**On Windows:**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**On macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Migrations & Populate Seed Data
```bash
python manage.py migrate
python seed_data.py
```
*(This creates categories, 16 realistic products, demo user accounts, and a sample order!)*

### 5. Start the Development Server
```bash
python manage.py runserver
```

Open your browser and navigate to:
```
http://127.0.0.1:8000/
```

- Storefront: `http://127.0.0.1:8000/`
- Admin Dashboard: `http://127.0.0.1:8000/admin/` (Login: `admin` / `admin123`)

---

## 🧪 Running Automated Tests

Run the built-in test suite to verify all endpoints, models, cart logic, and checkout workflows:

```bash
python manage.py test
```

Expected output:
```text
Ran 6 tests in 5.742s

OK
```

---

## ☁️ Step-by-Step Deployment Guide

You can deploy this project for **free** on cloud platforms like **Render**, **Railway**, or **PythonAnywhere**.

### Option A: 1-Click Deployment on Render.com (Recommended)

1. Fork or push this repository to your GitHub account: `https://github.com/Harika3560123/CodeAlpha_Ecommerce_Store`.
2. Sign in to [Render.com](https://render.com) with GitHub.
3. Click **New +** ➜ **Web Service**.
4. Select your `CodeAlpha_Ecommerce_Store` repository.
5. Fill in the service details:
   - **Environment**: `Python 3`
   - **Region**: Any (e.g. Oregon, Frankfurt, Singapore)
   - **Build Command**:
     ```bash
     pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate && python seed_data.py
     ```
   - **Start Command**:
     ```bash
     gunicorn ecommerce_project.wsgi:application
     ```
6. Add Environment Variables:
   - `DEBUG`: `False`
   - `SECRET_KEY`: `your-random-production-secret-key-here`
   - `ALLOWED_HOSTS`: `*`
7. Click **Create Web Service**. Your app will build, seed, and go live with a free URL like:
   `https://codealpha-ecommerce-store.onrender.com`

---

### Option B: PythonAnywhere Deployment

1. Register a free beginner account at [PythonAnywhere.com](https://www.pythonanywhere.com/).
2. Open a Bash console and clone the repository:
   ```bash
   git clone https://github.com/Harika3560123/CodeAlpha_Ecommerce_Store.git
   ```
3. Set up a virtualenv and install dependencies:
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 myenv
   pip install -r requirements.txt
   python manage.py migrate
   python seed_data.py
   python manage.py collectstatic
   ```
4. In the PythonAnywhere **Web** tab, configure the WSGI configuration file pointing to `ecommerce_project.wsgi:application`.
5. Reload your web app!

---

## 📹 Internship Video Submission Tips

For the CodeAlpha Internship presentation:
1. **Showcase the Storefront**: Demonstrate category filtering, live keyword search, and sorting.
2. **Product Details**: Click on a product to show high-res imagery, discounted pricing, and bulleted specs.
3. **Shopping Cart**: Add products using the AJAX button, change quantity in the cart table, and show the Free Shipping progress bar.
4. **Checkout & Order Process**: Use the 1-click demo filler button on checkout, select payment method, and submit.
5. **Invoice & Order Tracking**: Show the generated `#ORD-XXXXXXXX` invoice, print receipt button, and fulfillment tracker.
6. **Admin Panel**: Log in to `/admin/` and demonstrate how products and orders can be managed in real-time.

---

## 👩‍💻 Author & Credits

- **Developer**: Harika Budamakayala
- **GitHub**: [@Harika3560123](https://github.com/Harika3560123)
- **Organization**: [CodeAlpha](https://www.codealpha.tech)
- **Program**: CodeAlpha Web Development Internship
- **Task**: Task 1 - Simple E-Commerce Store

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
