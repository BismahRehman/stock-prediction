# Stock Prediction API

A production-ready **Stock Prediction SaaS API** built with FastAPI, featuring ML-powered price forecasting using scikit-learn, user authentication (JWT + Google OAuth), subscription management via Stripe, and admin controls.

---

## 🚀 Features

- **User Authentication**: Email/password registration with JWT tokens (15-min expiry) + Google OAuth 2.0
- **ML Stock Predictions**: Train models on historical stock data from Yahoo Finance (1 year daily)
- **Multiple ML Algorithms**:
  - Random Forest Regressor (all users)
  - Linear Regression (all users)
  - Neural Network MLP (premium users only)
- **Token-Based Quota System**: 100 tokens/month, 10 tokens per prediction, auto-resets every 30 days
- **Subscription Tiers**: Free and Premium plans via Stripe checkout
- **Prediction History**: Track past predictions with R² accuracy scores
- **Admin Controls**: Ban/unban users, reset tokens, manage subscriptions
- **Async Architecture**: Non-blocking I/O with async SQLAlchemy and asyncpg

---

## 📋 Tech Stack

| Category | Technology |
|----------|-----------|
| **Backend** | FastAPI 0.135+, Uvicorn |
| **Database** | PostgreSQL 15, asyncpg, SQLAlchemy 2.0 (async) |
| **Migrations** | Alembic |
| **ML** | scikit-learn, yfinance |
| **Auth** | JWT (python-jose), bcrypt (passlib), Google OAuth 2.0 |
| **Payments** | Stripe SDK |
| **Package Manager** | uv (Astral) |
| **Testing** | pytest, pytest-asyncio, pytest-mock |
| **Containerization** | Docker, Docker Compose |
| **Python** | 3.13 |

---

## 📁 Project Structure

```
stock_predition/
├── app/
│   ├── main.py                 # FastAPI app entry point, admin seeder
│   ├── config.py               # Pydantic Settings (.env-backed)
│   ├── database.py             # Async SQLAlchemy engine & session
│   ├── dependency.py           # Auth guard, token quota, admin check
│   ├── model/                  # SQLAlchemy ORM models
│   │   ├── user.py             # User table
│   │   ├── history.py          # PredictionHistory table
│   │   └── Blacklist_Table.py  # BlacklistedToken table
│   ├── schema/                 # Pydantic request/response schemas
│   │   ├── user.py             # Auth schemas
│   │   ├── prediction.py       # Prediction request/response
│   │   └── history.py          # History response
│   ├── routes/                 # API routers
│   │   ├── user.py             # /auth/* endpoints
│   │   ├── google_auth.py      # /auth/google/* endpoints
│   │   ├── prediction.py       # /prediction/train
│   │   ├── history.py          # /prediction/history
│   │   ├── stripe.py           # Stripe payment endpoints
│   │   └── admin.py            # /admin/* endpoints
│   ├── service/                # Business logic
│   │   ├── auth.py             # Password hashing, JWT creation
│   │   ├── google_auth.py      # Google OAuth handler
│   │   ├── prediction.py       # ML training pipeline
│   │   └── stripe.py           # Stripe checkout & webhook
│   ├── repository/             # Database access layer
│   └── ml_model/
│       └── model_selector.py   # ML model factory
├── alembic/                    # Database migrations
│   ├── env.py
│   └── versions/               # Migration scripts
├── tests/                      # Test suite
│   ├── conftest.py             # TestClient setup
│   ├── routes/                 # API endpoint tests
│   ├── service/                # Service layer tests
│   ├── repository/             # Repository tests
│   ├── schema/                 # Schema tests
│   └── model/                  # Model tests
├── compose.yaml                # Docker Compose
├── Dockerfile                  # Container definition
├── pyproject.toml              # Dependencies
├── alembic.ini                 # Alembic config
└── pytest.ini                  # pytest config
```

---

## 🗄️ Database Models

### User
- `id` (Integer, PK), `email` (String, unique, indexed)
- `hashed_password` (String, nullable for OAuth users)
- `role` (Enum: "user" | "admin", default: "user")
- `subscription` (Enum: "free" | "premium", default: "free")
- `token` (Integer, default: 100), `banned` (Boolean, default: False)
- `google_id` (String, unique, nullable), `auth_provider` (String, nullable)
- `last_reset_date` (DateTime, default: utcnow)

### PredictionHistory
- `id` (Integer, PK), `user_id` (Integer, FK → users.id)
- `model_name` (String), `accuracy` (JSON), `created_at` (DateTime)

### BlacklistedToken
- `token` (String, PK), `created_at` (DateTime)

---

## 🔌 API Endpoints

### Authentication (`/auth`)
| Method | Path | Description | Auth |
|--------|------|-------------|------|
| POST | `/auth/register` | Register with email/password | None |
| POST | `/auth/login` | Login, returns JWT | None |
| GET | `/auth/logout` | Logout (blacklists token) | Bearer |
| GET | `/auth/google/login` | Get Google OAuth URL | None |
| GET | `/auth/google/callback` | OAuth callback, returns JWT | None |

### Predictions (`/prediction`)
| Method | Path | Description | Auth |
|--------|------|-------------|------|
| POST | `/prediction/train` | Train ML model on stocks | Bearer + tokens |
| GET | `/prediction/history` | Get user's prediction history | Bearer |

### Payments (Stripe)
| Method | Path | Description | Auth |
|--------|------|-------------|------|
| GET | `/create-subscription-checkout` | Create checkout session | Bearer |
| POST | `/webhook` | Stripe webhook handler | Stripe signature |
| GET | `/success` | Payment success page | None |
| GET | `/cancel` | Payment cancel page | None |

### Admin (`/admin`)
| Method | Path | Description | Auth |
|--------|------|-------------|------|
| POST | `/admin/ban-user/{user_id}` | Ban a user | Admin only |
| POST | `/admin/unban-user/{user_id}` | Unban a user | Admin only |
| POST | `/admin/update-tokens/{user_id}` | Reset tokens to 100 | Admin only |
| POST | `/admin/cancel-subscription/{user_id}` | Downgrade to free | Admin only |
| POST | `/admin/renew-subscription/{user_id}` | Upgrade to premium | Admin only |

---

## 🤖 ML Pipeline

1. **Data Fetch**: Downloads 1 year of daily stock data via `yfinance` (async via `asyncio.to_thread`)
2. **Feature Engineering**: EMA (Exponential Moving Average), MAR (Moving Average Ratio)
3. **Feature Selection**: OHLC, EMA, MAR (user-configurable)
4. **Train-Test Split**: Time-series safe (`shuffle=False`)
5. **Model Training**: RandomForest, LinearRegression, or MLPRegressor(50,50) for premium
6. **Evaluation**: R² score per stock ticker
7. **Token Deduction**: 10 tokens consumed per request

---

## 🔐 Authentication & Authorization

### JWT Token System
- **Access Token**: 15-minute expiry, signed with `SECRET_KEY` using HS256
- **Token Blacklisting**: Logout stores JWT in database; checked on every request
- **Bearer Token Auth**: All protected endpoints require `Authorization: Bearer <token>`

### Google OAuth 2.0
- Authorization code flow with Google
- Exchanges code for access token, fetches user info
- Creates/links user account, issues internal JWT (60-min expiry)

### Token Quota
- New users start with **100 tokens**
- Each prediction costs **10 tokens**
- Auto-resets every **30 days** (checked on prediction request)

### Admin Guard
- `/admin/*` endpoints require `role = "admin"`
- First admin created automatically on startup from `.env` settings

---

## 🛠️ Setup & Installation

### Prerequisites
- Python 3.13
- PostgreSQL 15
- Docker & Docker Compose (optional, for containerized deployment)

### Local Development

1. **Clone and navigate to project**
   ```bash
   cd stock_predition
   ```

2. **Create `.env` file** (required - no defaults in code)
   ```env
   DATABASE_URI=postgresql+asyncpg://postgres:1234@localhost:5432/stock_prediction
   SECRET_KEY=<your-secret-key>
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=15
   CLIENT_ID=<google-client-id>
   CLIENT_SECRET=<google-client-secret>
   REDIRECT_URI=http://localhost:8000/auth/google/callback
   TOKEN_URL=https://oauth2.googleapis.com/token
   USERINFO_URL=https://www.googleapis.com/oauth2/v2/userinfo
   STRIPE_SECRET_KEY=<stripe-secret-key>
   STRIPE_WEBHOOK_SECRET=<stripe-webhook-secret>
   DOMAIN_URL=http://localhost:8000
   PRICE_ID=<stripe-price-id>
   ADMIN_EMAIL=admin@example.com
   ADMIN_PASSWORD=<admin-password>
   ```

3. **Install dependencies**
   ```bash
   uv sync
   ```

4. **Create database** (if not exists)
   ```bash
   # Connect to PostgreSQL and run:
   CREATE DATABASE stock_prediction;
   ```

5. **Run migrations**
   ```bash
   uv run alembic upgrade head
   ```

6. **Start development server**
   ```bash
   uv run uvicorn app.main:app --reload
   ```

7. **Access the API**
   - Server: http://localhost:8000
   - API Docs (Swagger): http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Docker Deployment

1. **Build and run**
   ```bash
   docker compose up --build
   ```

   This starts:
   - **app**: FastAPI on port 8000
   - **db**: PostgreSQL 15 on port 5432 with persistent volume

2. **Run migrations** (first time only)
   ```bash
   docker compose exec app uv run alembic upgrade head
   ```

3. **Access**: http://localhost:8000

---

## 🧪 Testing

Run full test suite:
```bash
uv run pytest
```

Run with verbose output:
```bash
uv run pytest -v
```

Run specific test file:
```bash
uv run pytest tests/routes/test_user.py -v
```

**Test Structure**:
- `tests/routes/` - API endpoint tests (mocked services)
- `tests/service/` - Service layer unit tests
- `tests/repository/` - Repository layer tests
- Tests use `TestClient` with monkeypatching (no test DB)

---

## 📚 API Documentation

Interactive API documentation auto-generated by FastAPI:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🚦 Token System

| Action | Token Cost |
|--------|-----------|
| Train ML model (`/prediction/train`) | 10 tokens |
| Monthly reset | Auto-resets to 100 |

Admins can manually reset tokens via `/admin/update-tokens/{user_id}`.

---

## 🎯 Subscription Tiers

| Feature | Free | Premium |
|---------|------|---------|
| Random Forest | ✅ | ✅ |
| Linear Regression | ✅ | ✅ |
| Neural Network (MLP) | ❌ | ✅ |
| Token Quota | 100/month | 100/month |

Upgrade via `/create-subscription-checkout` → Stripe checkout.

---

## 🔧 Development

### Add a new migration
```bash
uv run alembic revision --autogenerate -m "description"
uv run alembic upgrade head
```

### Rollback migration
```bash
uv run alembic downgrade -1
```

### Check migration status
```bash
uv run alembic current
uv run alembic history
```

---

## 🐳 Docker Configuration

### Dockerfile
- Base: `python:3.13.7-slim`
- Installs `uv` package manager
- Copies `pyproject.toml` + `uv.lock` first (Docker cache optimization)
- Runs `uv sync --frozen` for reproducible dependencies
- Entry point: `uv run uvicorn app.main:app --host 0.0.0.0 --port 8000`

### Docker Compose
- **app**: Builds from Dockerfile, port 8000, depends on db
- **db**: PostgreSQL 15, port 5432, persistent volume `db_data`
- Environment variables set in `compose.yaml`

---

## ⚠️ Troubleshooting

### Missing `.env` file
**Error**: App fails to start with missing settings
**Solution**: Create `.env` file with all required variables (see Setup section). The app has no defaults for Settings fields.

### Database connection errors
**Error**: `connection refused` or `database does not exist`
**Solution**: 
1. Ensure PostgreSQL is running
2. Create database: `CREATE DATABASE stock_prediction;`
3. Verify `DATABASE_URI` in `.env` matches your setup

### Alembic migration fail
**Error**: `Target database is not up to date`
**Solution**: Run `uv run alembic upgrade head`

### Stripe configuration
**Error**: `Stripe keys not set in .env`
**Solution**: Set `STRIPE_SECRET_KEY` in `.env`. The app validates this on startup.

### Neural Network access denied (403)
**Error**: "Neural Network is only available for premium users"
**Solution**: User must have `subscription = "premium"` and send `premium_user: true` in prediction request.

### Token quota exceeded (403)
**Error**: Forbidden when tokens < 10
**Solution**: Wait for 30-day auto-reset, or admin can reset via `/admin/update-tokens/{user_id}`

---

## 📄 License

This project is provided for educational and development purposes.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
