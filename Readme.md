# Storefront E-Commerce Platform

A full-featured e-commerce platform built with Django and Django REST Framework, featuring a comprehensive product management system, shopping cart functionality, order processing, and user authentication.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [API Documentation](#api-documentation)
- [Database Models](#database-models)
- [Testing](#testing)
- [Performance Optimization](#performance-optimization)
- [Deployment](#deployment)
- [Before Going to Production](#before-going-to-production)
- [Serving Static Files](#serving-static-files)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

Storefront is a modern e-commerce backend platform that provides RESTful APIs for managing products, collections, shopping carts, orders, and customer accounts. Built with scalability and performance in mind, it includes features like caching, background task processing, and comprehensive testing.

## ✨ Features

### Core Features

- **Product Management**: Complete CRUD operations for products with image upload support
- **Collection Management**: Organize products into collections with featured products
- **Shopping Cart**: Persistent cart functionality with UUID-based identification
- **Order Processing**: Full order lifecycle management with multiple payment statuses
- **Customer Accounts**: User registration, authentication, and profile management
- **Review System**: Product reviews and ratings
- **Image Management**: Multiple images per product with validation

### Advanced Features

- **JWT Authentication**: Secure token-based authentication using SimpleJWT
- **Permission System**: Role-based access control with custom permissions
- **Filtering & Search**: Advanced product filtering, searching, and ordering
- **Pagination**: Optimized pagination for large datasets
- **Caching**: Redis-based caching for improved performance
- **Background Tasks**: Celery integration for asynchronous task processing
- **Email Notifications**: SMTP email support for notifications
- **Admin Interface**: Customized Django admin panel
- **API Documentation**: RESTful API with comprehensive endpoints
- **CORS Support**: Cross-Origin Resource Sharing enabled
- **File Validation**: Image size and type validation
- **Query Optimization**: Optimized database queries with select_related and prefetch_related

## 🛠 Technology Stack

### Backend

- **Django 5.x**: Web framework
- **Django REST Framework**: API development
- **PostgreSQL**: Production database (MySQL supported)
- **Redis**: Caching and message broker
- **Celery**: Asynchronous task processing
- **Flower**: Celery monitoring

### Authentication & Security

- **Djoser**: User registration and authentication
- **SimpleJWT**: JWT token authentication
- **Django CORS Headers**: Cross-origin resource sharing

### Performance & Monitoring

- **Django Debug Toolbar**: Development debugging
- **Django Silk**: SQL profiling and analysis (dev)
- **Locust**: Load testing
- **WhiteNoise**: Static file serving

### Testing

- **Pytest**: Testing framework
- **pytest-django**: Django-specific testing utilities
- **pytest-watch**: Auto-running tests
- **Model Bakery**: Test data generation

### DevOps

- **Gunicorn**: WSGI HTTP server
- **Render**: Cloud hosting platform
- **Docker**: Containerization support

## 📁 Project Structure

```
storefront3/
├── core/                      # Core app (authentication, users)
│   ├── models.py             # Custom User model
│   ├── serializers.py        # User serializers
│   ├── views.py              # Core views
│   ├── signals/              # Signal handlers
│   └── static/               # Core static files
│
├── store/                     # Main store app
│   ├── models.py             # Product, Order, Cart models
│   ├── serializers.py        # API serializers
│   ├── views.py              # ViewSets and API views
│   ├── filters.py            # Custom filters
│   ├── permissions.py        # Custom permissions
│   ├── pagination.py         # Pagination classes
│   ├── validators.py         # Custom validators
│   ├── signals/              # Store signal handlers
│   └── tests/                # Test suite
│       ├── conftest.py       # Pytest fixtures
│       └── test_collections.py
│
├── tags/                      # Tagging system
├── likes/                     # Like functionality
├── playground/                # Testing playground
│   ├── tasks.py              # Celery tasks
│   └── views.py
│
├── storefront/                # Project settings
│   ├── settings/
│   │   ├── common.py         # Common settings
│   │   ├── dev.py            # Development settings
│   │   └── prod.py           # Production settings
│   ├── celery.py             # Celery configuration
│   ├── urls.py               # URL routing
│   └── wsgi.py               # WSGI configuration
│
├── static/                    # Static files (collected)
├── media/                     # User-uploaded files
├── logs/                      # Application logs
├── locustfiles/              # Load testing scripts
│
├── manage.py                  # Django management script
├── requirements.txt           # Python dependencies
├── Pipfile                    # Pipenv configuration
├── pytest.ini                 # Pytest configuration
├── build.sh                   # Build script for deployment
└── render.yaml                # Render.com configuration
```

## 🚀 Installation

### Prerequisites

- Python 3.10 or higher
- PostgreSQL (for production) or MySQL
- Redis server
- pip or pipenv

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd storefront3
```

### Step 2: Create Virtual Environment

```bash
# Using pipenv (recommended)
pipenv install

# Or using venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 3: Install Redis

```bash
# Ubuntu/Debian
sudo apt-get install redis-server

# macOS
brew install redis

# Start Redis
redis-server
```

### Step 4: Environment Variables

Create a `.env` file in the project root:

```bash
# Django Settings
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_SETTINGS_MODULE=storefront.settings.dev
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgres://user:password@localhost:5432/storefront
# Or for MySQL
# DATABASE_URL=mysql://user:password@localhost:3306/storefront

# Redis
REDIS_URL=redis://localhost:6379

# Email
EMAIL_HOST=localhost
EMAIL_PORT=2525
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL=admin@gmail.com

# Celery
CELERY_BROKER_URL=redis://localhost:6379/1
```

### Step 5: Database Setup

```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load seed data (optional)
# mysql -u root -p storefront < seed.sql
```

### Step 6: Collect Static Files

```bash
python manage.py collectstatic --no-input
```

### Step 7: Run Development Server

```bash
# Start Django server
python manage.py runserver

# In separate terminals:
# Start Celery worker
celery -A storefront worker --loglevel=info

# Start Celery beat (scheduled tasks)
celery -A storefront beat --loglevel=info

# Start Flower (Celery monitoring)
celery -A storefront flower
```

## ⚙️ Configuration

### Settings Structure

The project uses a split settings configuration:

- `common.py`: Shared settings
- `dev.py`: Development-specific settings
- `prod.py`: Production-specific settings

### Key Configuration Options

#### REST Framework

```python
REST_FRAMEWORK = {
    'COERCE_DECIMAL_TO_STRING': False,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}
```

#### JWT Settings

```python
SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('JWT',),
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1)
}
```

#### Caching

```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/2',
        'TIMEOUT': 10 * 60,
    }
}
```

#### Celery

```python
CELERY_BROKER_URL = 'redis://localhost:6379/1'
CELERY_BEAT_SCHEDULE = {
    'notify_customers': {
        'task': 'playground.tasks.notify_customers',
        'schedule': 5,
    }
}
```

## 📚 API Documentation

### Base URL

```
http://localhost:8000/
```

### Authentication Endpoints

```
POST   /auth/users/                    # Register new user
POST   /auth/jwt/create/               # Obtain JWT token
POST   /auth/jwt/refresh/              # Refresh JWT token
POST   /auth/jwt/verify/               # Verify JWT token
GET    /auth/users/me/                 # Get current user
```

### Product Endpoints

```
GET    /store/products/                # List all products
POST   /store/products/                # Create product (admin)
GET    /store/products/{id}/           # Get product details
PUT    /store/products/{id}/           # Update product (admin)
PATCH  /store/products/{id}/           # Partial update (admin)
DELETE /store/products/{id}/           # Delete product (admin)
GET    /store/products/{id}/images/    # List product images
POST   /store/products/{id}/images/    # Upload product image
```

### Collection Endpoints

```
GET    /store/collections/             # List all collections
POST   /store/collections/             # Create collection (admin)
GET    /store/collections/{id}/        # Get collection details
PUT    /store/collections/{id}/        # Update collection (admin)
DELETE /store/collections/{id}/        # Delete collection (admin)
```

### Cart Endpoints

```
GET    /store/carts/{uuid}/            # Get cart
POST   /store/carts/                   # Create cart
DELETE /store/carts/{uuid}/            # Delete cart
GET    /store/carts/{uuid}/items/      # List cart items
POST   /store/carts/{uuid}/items/      # Add item to cart
PATCH  /store/carts/{uuid}/items/{id}/ # Update cart item
DELETE /store/carts/{uuid}/items/{id}/ # Remove cart item
```

### Order Endpoints

```
GET    /store/orders/                  # List orders
POST   /store/orders/                  # Create order
GET    /store/orders/{id}/             # Get order details
PATCH  /store/orders/{id}/             # Update order (admin)
DELETE /store/orders/{id}/             # Delete order (admin)
```

### Customer Endpoints

```
GET    /store/customers/               # List customers (admin)
GET    /store/customers/me/            # Get current customer
PUT    /store/customers/me/            # Update current customer
GET    /store/customers/{id}/history/  # Get customer history
```

### Review Endpoints

```
GET    /store/products/{id}/reviews/   # List product reviews
POST   /store/products/{id}/reviews/   # Create review
GET    /store/products/{id}/reviews/{id}/ # Get review
PUT    /store/products/{id}/reviews/{id}/ # Update review
DELETE /store/products/{id}/reviews/{id}/ # Delete review
```

### Query Parameters

- `?search=query` - Search products by title or description
- `?collection_id=1` - Filter by collection
- `?ordering=unit_price` - Order by field
- `?ordering=-unit_price` - Reverse order
- `?page=2` - Pagination
- `?page_size=10` - Items per page

## 🗄️ Database Models

### Core Models

- **User**: Custom user model with email authentication
- **Customer**: Extended user profile with membership levels

### Store Models

- **Product**: Product information with title, price, inventory
- **ProductImage**: Multiple images per product
- **Collection**: Product categorization
- **Cart**: Shopping cart with UUID
- **CartItem**: Items in cart with quantity
- **Order**: Customer orders with payment status
- **OrderItem**: Products in an order
- **Review**: Product reviews with ratings
- **Promotion**: Discount promotions

### Relationships

- Products belong to Collections (Many-to-One)
- Products have multiple Images (One-to-Many)
- Cart contains CartItems (One-to-Many)
- Orders contain OrderItems (One-to-Many)
- Customers have Orders (One-to-Many)
- Products have Reviews (One-to-Many)

## 🧪 Testing

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=store

# Run specific test file
pytest store/tests/test_collections.py

# Auto-run tests on changes
ptw
```

### Test Configuration

Tests are configured in `pytest.ini`:

```ini
[pytest]
DJANGO_SETTINGS_MODULE = storefront.settings.dev
addopts = --reuse-db
```

### Load Testing

```bash
# Run Locust load tests
locust -f locustfiles/browse_products.py
```

## ⚡ Performance Optimization

### Query Optimization

The project implements several optimization techniques:

1. **Select Related**: Reduce queries for foreign keys

```python
Product.objects.select_related('collection')
```

2. **Prefetch Related**: Optimize reverse foreign keys and many-to-many

```python
Cart.objects.prefetch_related('items__product__images')
```

3. **Only/Defer**: Fetch only required fields

```python
Product.objects.only('id', 'title', 'unit_price')
```

4. **Exists() vs Count()**: Use exists() for boolean checks

```python
if Product.objects.filter(collection_id=pk).exists():
```

5. **Annotate**: Calculate aggregates at database level

```python
Collection.objects.annotate(products_count=Count('products'))
```

### Caching Strategy

- Redis caching for frequently accessed data
- 10-minute default timeout
- Cache invalidation on model changes

### Static File Optimization

- WhiteNoise for efficient static file serving
- Gzip compression enabled
- Browser caching headers

## 🚀 Deployment

### Render.com Deployment

The project is configured for Render.com with the following setup:

#### render.yaml Configuration

```yaml
services:
  - type: web
    name: sijanbuy
    runtime: python
    plan: free
    buildCommand: './build.sh'
    startCommand: 'gunicorn storefront.wsgi:application'
    envVars:
      - key: DJANGO_SETTINGS_MODULE
        value: storefront.settings.prod
      - key: DJANGO_SECRET_KEY
        generateValue: true
      - key: ALLOWED_HOSTS
        value: '*'

databases:
  - name: sijanbuy-db
    plan: free
    databaseName: storefront
    user: storefront
```

#### Build Script (build.sh)

```bash
#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
```

### Deployment Steps

1. Push code to GitHub
2. Connect Render.com to repository
3. Configure environment variables
4. Deploy automatically on push

### Environment Variables for Production

```
DJANGO_SECRET_KEY=<generated-secret>
DJANGO_SETTINGS_MODULE=storefront.settings.prod
ALLOWED_HOSTS=*.onrender.com,yourdomain.com
DATABASE_URL=<postgres-connection-string>
REDIS_URL=<redis-connection-string>
DEBUG=False
```

## 📝 Before Going to Production

### Static Files Collection

Collect static files by running:

```bash
python manage.py collectstatic
```

This will gather all static files into the directory specified by `STATIC_ROOT` in your settings.py.

### Checklist

- ✅ Collect static files
- ✅ Set `DEBUG=False`
- ✅ Configure `ALLOWED_HOSTS`
- ✅ Set strong `SECRET_KEY`
- ✅ Configure production database
- ✅ Set up Redis for caching
- ✅ Configure email backend
- ✅ Set up HTTPS
- ✅ Configure CORS origins
- ✅ Run migrations
- ✅ Create superuser
- ✅ Test static file serving
- ✅ Verify email functionality
- ✅ Check error logging
- ✅ Set up monitoring

### Static File Configuration

Update your `settings.py` to include the `STATIC_ROOT` setting:

```python
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
```

Verify that your static files are accessible in the production environment by visiting a URL like:

```
https://yourdomain.com/static/yourfile.css
```

## 🔧 Serving Static Files

### Development

During development, Django automatically serves static files when `DEBUG` is set to `True`.

### Production with WhiteNoise

Django does not serve static files in production by default. We use **WhiteNoise** for this purpose.

#### Install WhiteNoise

```bash
pipenv install whitenoise
# or
pip install whitenoise
```

#### Configure Middleware

Add WhiteNoise to your `settings.py` middleware (right after `SecurityMiddleware`):

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this line
    'django.contrib.sessions.middleware.SessionMiddleware',
    # ... other middleware classes ...
]
```

#### Benefits

- Serves static files efficiently in production
- Gzip compression
- Far-future cache headers
- Works with any WSGI server

### Logging Static Files

After production deployment, if some static files are not loading properly, check the logs for any errors related to static file serving.

Configure logging in your `settings.py`:

```python
# Create logs directory if it doesn't exist
LOGS_DIR = BASE_DIR / 'logs'
LOGS_DIR.mkdir(exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': LOGS_DIR / 'static_files.log',
            'formatter': 'verbose',
        }
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': os.environ.get('DJANGO_LOG_LEVEL', 'INFO'),
        },
    },
    'formatters': {
        'verbose': {
            'format': '{asctime} ({levelname}) -- {name} --- {message}',
            'style': '{',
        }
    }
}
```

This will help identify issues with file paths, permissions, or configuration problems.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Write tests for new features

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Django and Django REST Framework teams
- All contributors and maintainers
- Open source community

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Built with ❤️ using Django and Django REST Framework**
