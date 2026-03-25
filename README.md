# Asset Management API

A robust FastAPI-based **Asset Management API** tailored to handle high concurrency during the assignment/claiming of limited digital assets (Coupons/Vouchers).

The system allows authenticated users to discover available assets, claim them, and view their historical claims. In addition, the system is designed to gracefully handle concurrency and race conditions when hundreds of users simultaneously try to claim the same limited asset.

---

## 🚀 Key Features

*   **User Authentication**: JWT-based secure authentication flow. Users must be authenticated to interact with sensitive endpoints.
*   **Concurrency & Data Integrity**: Engineered to safely handle race conditions and prevent over-claiming or data corruption during high-traffic bursts, utilizing database-layer locking strategies (e.g., pessimistic locking).
*   **Relational Asset Tracking**: Efficiently stores and processes user-asset relationships. Includes complex relational queries to display real-time global asset states alongside personalized historical activities.

---

## 🛠 Tech Stack

*   **Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Python)
*   **ORM:** SQLAlchemy (for database operations)
*   **Authentication:** JWT (JSON Web Tokens), `passlib`, `bcrypt`
*   **Database:** PostgreSQL (or SQLite for dev environments)

---

## 🏗 Project Structure

```text
├── database/          # Global Database configuration & dependency injection
├── models/            # SQLAlchemy Database Models (User, Coupon, Claim)
├── routes/            # FastAPI Routers for different resource domains
│   ├── auth.py        # Registration, Login, and Profile lookups
│   ├── coupons.py     # Creation, Listing, Claiming, and Statistics
│   └── test.py        # General testing endpoints
├── schemas/           # Pydantic models for request/response validation
├── services/          # Core Business Logic handling (AuthService, CouponService)
├── utils/             # Helper utilities, authentication dependency handlers (e.g. get_current_user)
├── main.py            # Global Application Entrypoint
└── requirements.txt   # (Depending on environment, alternatively pyproject.toml / pipfile)
```

---

## 📖 API Endpoints Summary

### Authentication (`/auth`)
*   **`POST /auth/register`**: Registers a new user.
*   **`POST /auth/login`**: Authenticates the user and returns a secure JWT.
*   **`GET /auth/me`**: Returns the current authorized user profile.

### Assets & Coupons (`/coupons`)
*   **`POST /coupons/create`**: Create a new coupon and set its allocation pool.
*   **`GET /coupons/`**: Retrieve a comprehensive list of all coupons.
*   **`GET /coupons/available`**: Fetch the list of coupons that have not been fully claimed yet.
*   **`POST /coupons/claim/{coupon_id}`**: Attempt to claim an asset. Fully handles concurrency checks to prevent overselling.
*   **`GET /coupons/my-claims`**: Returns a list representing the user's previously claimed assets (Efficient join mapping Claims -> User -> Coupons).
*   **`GET /coupons/coupon-stats`**: Gets advanced global statistics of all recorded assets.

---

## 💻 Local Setup & Installation

**1. Clone the repository:**
```bash
git clone <repository_url>
cd Luarc_project
```

**2. Setup Virtual Environment:**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
```

**3. Install Dependencies:**
```bash
pip install -r requirements.txt
```

**4. Run the API Server:**
```bash
uvicorn main:app --reload
```
The server should start automatically on [http://127.0.0.1:8000](http://127.0.0.1:8000). You can explore the interactive documentation directly at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).
