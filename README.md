# Expense Tracker — Backend API

A Django REST API that powers the Expense Tracker mobile app. Handles user authentication, expense storage, category management, and monthly summaries.

## Features

- JWT-based authentication (register, login, token refresh)
- Full CRUD for expenses with category support
- Bulk expense creation (used when importing from SMS)
- Monthly summary with spending breakdown by category
- Tracks whether each expense was added manually or detected from SMS
- CORS enabled for mobile app access

## Tech Stack

- **Python 3.10** / **Django 5.2**
- **Django REST Framework** — API layer
- **djangorestframework-simplejwt** — JWT authentication
- **django-cors-headers** — Cross-origin requests from Flutter app
- **SQLite** — Development database (swap to PostgreSQL for production)

## Project Structure

```
expense_tracker/          ← Django project config (settings, urls)
expenses/
├── models.py             ← Expense, Category models
├── serializers.py        ← DRF serializers
├── views.py              ← API views (list, create, bulk, summary)
└── urls.py               ← API routes
users/
├── serializers.py        ← User / Register serializers
├── views.py              ← Register, Profile views
└── urls.py               ← Auth routes
```

## API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/auth/register/` | Register new user, returns tokens | No |
| POST | `/api/auth/login/` | Login, returns JWT access + refresh tokens | No |
| POST | `/api/auth/token/refresh/` | Refresh access token | No |
| GET | `/api/auth/profile/` | Get current user info | Yes |
| GET | `/api/expenses/` | List user's expenses | Yes |
| POST | `/api/expenses/` | Create a single expense | Yes |
| POST | `/api/expenses/bulk/` | Create multiple expenses at once (SMS import) | Yes |
| GET | `/api/expenses/<id>/` | Get a single expense | Yes |
| PUT | `/api/expenses/<id>/` | Update an expense | Yes |
| DELETE | `/api/expenses/<id>/` | Delete an expense | Yes |
| GET | `/api/categories/` | List all categories | Yes |
| GET | `/api/summary/` | Monthly totals by category (`?month=2026-06`) | Yes |

### Authentication

All protected endpoints require the header:
```
Authorization: Bearer <access_token>
```

### Expense Model

```json
{
  "id": 1,
  "amount": "500.00",
  "description": "Zomato",
  "date_of_expense": "2026-06-17",
  "category": 2,
  "category_name": "Food",
  "source": "sms",
  "raw_sms": "Rs. 500 debited from your account for UPI/Zomato",
  "created_at": "2026-06-17T10:30:00Z"
}
```

`source` is either `manual` (user typed it) or `sms` (auto-detected from bank message).

## Local Setup

### Prerequisites
- Python 3.10+
- pip

### Steps

```bash
# Clone the repo
git clone https://github.com/RichaKhatod/expense-tracker-backend.git
cd expense-tracker-backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # Mac/Linux
# venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create admin user (optional)
python manage.py createsuperuser

# Start server
python manage.py runserver 0.0.0.0:8000
```

The API will be available at `http://localhost:8000/api/`

Admin panel: `http://localhost:8000/admin/`

### Add Categories

Go to `http://localhost:8000/admin/` → Categories → Add a few (e.g. Food, Transport, Shopping, Bills, Entertainment).

## Production Deployment

For production (e.g. Railway, Render, DigitalOcean):

1. Set `DEBUG = False` in `settings.py`
2. Set `ALLOWED_HOSTS` to your domain
3. Use PostgreSQL instead of SQLite
4. Set `CORS_ALLOW_ALL_ORIGINS = False` and specify allowed origins
5. Store `SECRET_KEY` in an environment variable

## Related

- [Mobile App (Flutter)](https://github.com/RichaKhatod/expense-tracker-mobile) — Android app with SMS auto-detection
