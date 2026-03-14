# Secure Login System with Session Management

## Project Objective

This repository contains the source code for a defense-in-depth authentication system. The architecture is designed to mitigate common web vulnerabilities, including brute-force attacks, session hijacking, and Insecure Direct Object Reference (IDOR), demonstrating practical application of advanced backend security methodologies.

## Core Security Architecture

* **Memory-Hard Cryptography:** Passwords are hashed using Argon2id, rendering offline dictionary and GPU-based brute-force attacks mathematically infeasible.

* **Stateful Session Management:** Sessions are tracked in-memory using Redis, enforcing server-side Time-To-Live (TTL) expirations and allowing immediate access revocation.

* **XSS & CSRF Mitigation:** Session identifiers are transmitted exclusively via HTTP-Only, SameSite=Lax secure cookies.

* **Active Anti-Brute-Force Defenses:** The PostgreSQL database tracks failed authentication attempts. Surpassing the threshold triggers an automatic, cryptographic 15-minute account lockout utilizing UTC timestamps.

* **IDOR Prevention:** Sequential integer IDs are replaced with cryptographically secure UUIDv4 primary keys.

## Technology Stack

* **Backend Framework:** Python / FastAPI
* **Database:** PostgreSQL (Asynchronous via `asyncpg` and SQLAlchemy)
* **Caching & Sessions:** Redis
* **Cryptography:** `passlib[argon2]`, `secrets` (CSPRNG)
* **Data Validation:** Pydantic
* **Infrastructure:** Docker & Docker Compose
* **Frontend:** Vanilla HTML/JS/CSS (Served via FastAPI StaticFiles)

## Local Setup and Initialization

### 1. Prerequisites

* Docker Desktop installed and running.
* Python 3.10+ installed.

### 2. Environment Configuration

Create a `.env` file in the root directory and configure your cryptographic keys and database routing. Replace the bracketed variables with secure values.

```env
DATABASE_URL=postgresql+asyncpg://postgres:<YOUR_SECURE_PASSWORD>@localhost:5432/secure_login_db
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=<YOUR_64_CHARACTER_SECURE_HEX_STRING>
POSTGRES_PASSWORD=<YOUR_SECURE_PASSWORD>
```

### 3. Infrastructure Provisioning

Initialize the PostgreSQL and Redis containers:

```bash
docker-compose up -d
```

### 4. Application Startup

Initialize the Python virtual environment, install dependencies, and start the ASGI server:

```bash
python -m venv venv

# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

pip install -r requirements.txt
uvicorn main:app --reload
```

## System Access

* **Interactive API Documentation:** `http://127.0.0.1:8000/docs`
* **Frontend Interface:** `http://127.0.0.1:8000/app/`

## Project Structure

```text
static/
└── index.html          # Secure frontend interface
main.py                 # FastAPI application and route definitions
models.py               # SQLAlchemy database schema and lockout logic
schemas.py              # Pydantic strict input/output validation
security.py             # Argon2id hashing and token generation
session.py              # Redis stateful session management
database.py             # Asynchronous PostgreSQL connection pooling
test_security.py        # Automated audit script
docker-compose.yml      # Containerized infrastructure
```
