# 🌾 Krushi Settu - Smart Farmer Marketplace

A revolutionary digital marketplace platform designed to **connect farmers directly with buyers**, eliminating middlemen and ensuring fair prices for agricultural products.

![Python](https://img.shields.io/badge/Python-3.8%2B-green)
![Django](https://img.shields.io/badge/Django-4.2-blue)
![Database](https://img.shields.io/badge/Database-SQLite-orange)
![Status](https://img.shields.io/badge/Status-Development-yellow)

---

## 📋 Overview

**Krushi Settu** is a comprehensive digital solution aimed at transforming Indian agriculture by creating a **direct farmer-to-buyer marketplace**. It eliminates the role of middlemen, enabling:

- 🚜 **Farmers** to sell directly at fair prices
- 🛒 **Buyers** to source fresh produce at better rates
- 💰 **50-70% cost savings** for both parties
- 📱 **Simple & accessible** platform designed for all users

### Problem Statement
Indian farmers lose 40-50% of their income to middlemen, while buyers pay 2-3x the farm price for produce.

### Our Solution
A direct marketplace where farmers list products at fair prices and buyers can find fresh, local produce with complete transparency.

---

## ✨ Key Features

### 👨‍🌾 For Farmers
- **Dual Role Authentication** - Separate login for farmers and buyers
- **Product Management** - List crops with real-time pricing
- **Aadhaar-Based Verification** - Trust & security through identity verification
- **Order Management** - Track pending, accepted, and delivered orders
- **Live Chat System** - Direct communication with buyers
- **Market Prices** - Real-time Mandi prices for informed decision-making
- **Profile Management** - Farmer ratings, farmer type categorization
- **Payment Integration** - Bank & UPI details for seamless transactions

### 🛒 For Buyers
- **Smart Searching** - Find farmers & crops by location and type
- **Location-Based Matching** - Discover nearby farmers (distance calculated)
- **Live Marketplace** - Browse verified farmers and fresh produce
- **Order Placement** - One-click ordering with delivery options
- **Farmer Profiles** - View ratings and verified farmer information
- **Direct Messaging** - Negotiate prices & discuss delivery
- **Price Comparison** - See Mandi prices vs. marketplace prices

### 🌐 Platform Features
- **Multi-Language Support** - English, Hindi, and Odia interfaces
- **Real-Time Updates** - Order status tracking & notifications
- **Secure Authentication** - Phone verification with OTP
- **Responsive Design** - Works on desktop, tablet, and mobile
- **Search & Filter** - Advanced filtering by location, crop type, price
- **Ratings & Reviews** - Trust system for both farmers and buyers

---

## 🏗️ Tech Stack

### Backend
- **Framework**: Django 4.2
- **Language**: Python 3.8+
- **Database**: SQLite3 (development) / PostgreSQL (production-ready)
- **Authentication**: Django's built-in auth + OTP verification

### Frontend
- **Markup**: HTML5 with Django Templates
- **Styling**: CSS3 (responsive design)
- **Interactivity**: Vanilla JavaScript
- **Internationalization (i18n)**: Custom translation system (EN, HI, OR)

### Storage
- **Media**: File uploads (profile images, product images)
- **Static Files**: CSS, JavaScript, and image assets

---

## 📁 Project Structure

```
Krushi/
├── manage.py                      # Django management script
├── db.sqlite3                     # Development database
├── readme.md                      # This file
│
├── Krushi/                        # Main project settings
│   ├── settings.py                # Configuration
│   ├── urls.py                    # URL routing
│   ├── asgi.py                    # ASGI config
│   └── wsgi.py                    # WSGI config
│
├── app1/                          # Main application
│   ├── models.py                  # Database models
│   ├── views.py                   # View logic
│   ├── urls.py                    # App URLs
│   ├── forms.py                   # Django forms
│   ├── admin.py                   # Admin panel
│   ├── sms.py                     # SMS/OTP service
│   ├── tests.py                   # Unit tests
│   ├── apps.py                    # App config
│   └── migrations/                # Database migrations
│
├── static/                        # Static files
│   ├── css/                       # Stylesheets
│   │   ├── styles.css             # Main styles
│   │   └── farmer_portal.css      # Farmer dashboard styles
│   ├── js/                        # JavaScript files
│   │   ├── script.js              # Main functionality
│   │   ├── language.js            # i18n system
│   │   └── farmer_portal.js       # Portal interactions
│   └── image/                     # Images & assets
│
├── media/                         # User uploads
│   └── profiles/                  # User profile images
│
└── templates/                     # HTML templates
    ├── index.html                 # Homepage (landing page)
    ├── auth_form.html             # Login/Registration
    ├── farmer_dashboard.html       # Farmer portal
    ├── buyer_dashboard.html        # Buyer portal
    ├── farmer_portal_base.html    # Farmer base template
    ├── buyer_portal_base.html     # Buyer base template
    ├── add_crop.html              # Product listing form
    ├── crops.html                 # Crops management
    ├── orders.html                # Order management
    ├── chat.html                  # Messaging interface
    ├── prices.html                # Market prices
    ├── profile.html               # User profile
    ├── buyer_marketplace.html     # Marketplace browse
    ├── buyer_farmers.html         # Find farmers
    ├── buyer_buy.html             # Purchase interface
    ├── terms.html                 # Terms & conditions
    └── buyer_messages.html        # Buyer messaging
```

---

## 🗄️ Database Models

### 1. **UserProfile**
Stores detailed user information with role-based access
```
- user (One-to-One with User)
- role (farmer/buyer)
- full_name, phone_number, email
- location (latitude, longitude, name)
- farmer_type (Small Scale, Organic, Dairy, Grain, etc.)
- verification_status (verified/pending)
- preferred_language (EN, HI, OR)
- rating, bank_upi_details
- profile_image
```

### 2. **Product**
Agricultural products listed by farmers
```
- farmer (Foreign Key → UserProfile)
- crop_name, price, quantity_available
- unit (kg, quintal, piece, etc.)
- product_image
- status (available/sold_out)
- created_at, updated_at
```

### 3. **Order**
Purchase orders between buyers and farmers
```
- farmer, product (Foreign Keys)
- buyer_name, quantity, total_amount
- status (pending/accepted/delivered/rejected)
- delivery_mode (self/transport)
- created_at
```

### 4. **ChatMessage**
Direct messaging between farmers and buyers
```
- farmer (Foreign Key → UserProfile)
- buyer_name, message, is_unread
- created_at
```

### 5. **BuyerDemand**
Buyer requests for specific crops
```
- farmer (Foreign Key → UserProfile)
- crop_name, quantity_needed, distance_km
- created_at
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Git

### Step 1: Clone the Repository
```bash
cd path/to/project
git clone <repository-url>
cd Krushi
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

Create `requirements.txt` if not present:
```
Django==4.2.28
Pillow==10.0.0
python-decouple==3.8
requests==2.31.0
```

### Step 4: Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Create Superuser (Admin)
```bash
python manage.py createsuperuser
# Follow the prompts to create admin account
```

### Step 6: Collect Static Files
```bash
python manage.py collectstatic --noinput
```

---

## 🏃 Running the Project

### Development Server
```bash
python manage.py runserver
```
Access the application at: `http://127.0.0.1:8000`

### Access Admin Panel
```
http://127.0.0.1:8000/admin
Login with superuser credentials
```

### Application URLs

| Page | URL | Purpose |
|------|-----|---------|
| Homepage | `/` | Landing page with marketplace overview |
| Farmer Login | `/farmer/login/` | Farmer authentication |
| Buyer Login | `/buyer/login/` | Buyer authentication |
| Farmer Dashboard | `/farmer/dashboard/` | Main farmer portal |
| Farmer Crops | `/farmer/crops/` | Manage listed products |
| Farmer Sell | `/farmer/sell/` | Add new crop listing |
| Farmer Orders | `/farmer/orders/` | Track incoming orders |
| Farmer Prices | `/farmer/prices/` | View market prices |
| Farmer Profile | `/farmer/profile/` | Edit profile & settings |
| Buyer Marketplace | `/buyer/marketplace/` | Browse all products |
| Buyer Farmers | `/buyer/farmers/` | Find verified farmers |
| Buyer Orders | `/buyer/buy/` | My purchases |
| Buyer Prices | `/buyer/prices/` | Market price comparison |
| Messages | `/farmer/messages/` & `/buyer/messages/` | Direct chat |
| Terms & Conditions | `/terms/` | Legal information |
| Logout | `/logout/` | End session |

---

## 🌐 Multilingual Support

The platform supports **3 languages**:

1. **English** (en) - Default
2. **हिंदी (Hindi)** (hi) - North India
3. **ଓଡ଼ିଆ (Odia)** (or) - Eastern India

### Language System
- Located in: `static/js/language.js`
- Uses HTML `data-i18n` attributes for automatic translation
- Language preference saved in browser localStorage
- Supports text content, HTML content, and placeholders

### Adding New Languages
Edit `static/js/language.js` and add new language object:
```javascript
or: {
    nav_about: 'Your Translation',
    // ... more translations
}
```

---

## 🔐 Security Features

- ✅ **Aadhaar Verification** - Identity verification
- ✅ **OTP Authentication** - Phone number verification via SMS
- ✅ **CSRF Protection** - Django's built-in CSRF middleware
- ✅ **Password Hashing** - Django's password hash system
- ✅ **Session Management** - Secure session handling
- ✅ **User Authorization** - Role-based access control (Farmer/Buyer)

---

## 📞 Key Functionalities

### For Farmers 🚜
1. **Register & Verify** - Sign up with Aadhaar, verify phone via OTP
2. **List Products** - Add crops with price, quantity, description
3. **Manage Orders** - View & update order status
4. **Chat with Buyers** - Direct messaging for negotiations
5. **Track Income** - Dashboard showing sales & earnings
6. **View Market Prices** - Real Mandi prices for reference

### For Buyers 🛒
1. **Register & Search** - Browse farmers by location
2. **Place Orders** - Select products & confirm purchase
3. **Track Delivery** - Real-time order tracking
4. **Negotiate Prices** - Direct chat with sellers
5. **Verify Sellers** - Check farmer ratings & profiles
6. **Payment Options** - UPI, Bank Transfer support

---

## 🛠️ Development Tips

### Adding New Features
1. Create models in `app1/models.py`
2. Create forms in `app1/forms.py` if needed
3. Add views in `app1/views.py`
4. Create templates in `templates/`
5. Add URLs in `app1/urls.py`
6. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

### Adding Translations
1. Find the element to translate
2. Add `data-i18n="key_name"` attribute
3. Add translation in `static/js/language.js` in all three languages
4. Save and refresh browser

### Common Issues
- **Import Errors**: Ensure virtual environment is activated
- **Database Errors**: Run `python manage.py migrate`
- **Static Files Not Loading**: Run `python manage.py collectstatic`
- **Images Not Showing**: Check `MEDIA_URL` and `MEDIA_ROOT` in settings

---

## 📊 Admin Panel

Access Django admin at `/admin/`:
- Manage UserProfiles
- View & edit Products
- Track Orders
- Moderate ChatMessages
- View BuyerDemands

---

## 🚀 Deployment Considerations

For production deployment:

1. **Update Settings**
   ```python
   DEBUG = False
   ALLOWED_HOSTS = ['your-domain.com']
   SECRET_KEY = 'generate-secure-key'
   ```

2. **Use PostgreSQL** - More robust than SQLite
3. **Enable HTTPS** - Set `SECURE_SSL_REDIRECT = True`
4. **Configure Email** - For OTP & notifications
5. **Use Environment Variables** - Store sensitive data
6. **Setup Caching** - Redis for better performance
7. **Configure CDN** - Serve static files efficiently

---

## 🤝 Contributing

We welcome contributions! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👨‍💼 Project Owner

**Krushi Settu Development Team**
- Empowering Indian farmers through technology
- Connecting rural to urban markets

---

## 📧 Contact & Support

For issues, suggestions, or collaboration inquiries:
- **Email**: support@krushisettu.com
- **Issues**: GitHub Issues
- **Documentation**: Check project wiki

---

## 🌟 Acknowledgments

- Django community for a robust framework
- All contributors & farmers who inspire this project
- Special thanks to farmers & buyers for feedback

---

## 📈 Roadmap

- [ ] Payment Gateway Integration (Razorpay/Stripe)
- [ ] Mobile App (React Native/Flutter)
- [ ] GPS Tracking for Deliveries
- [ ] Advanced Analytics Dashboard
- [ ] Video Consultation Features
- [ ] IoT Integration for Crop Monitoring
- [ ] Machine Learning for Price Prediction
- [ ] Blockchain for Traceability

---

**Made with ❤️ for Farmers**

---

*Last Updated: March 2026*
*Version: 1.0.0 (Beta)*
