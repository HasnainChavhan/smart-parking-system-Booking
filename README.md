<div align="center">

# 🅿️ ParkSmart Pro

### AI-Powered Smart Parking Management System

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3-06B6D4?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com)

**Real-time slot booking · Role-based admin dashboard · Live occupancy tracking · UPI mock payments**

---

</div>

## 📖 Table of Contents

- [✨ Features](#-features)
- [🏗️ Project Structure](#️-project-structure)
- [⚙️ Prerequisites](#️-prerequisites)
- [🚀 Installation & Run Guide](#-installation--run-guide)
  - [Step 1 — Clone / Open the Project](#step-1--clone--open-the-project)
  - [Step 2 — Set Up the Backend](#step-2--set-up-the-backend)
  - [Step 3 — Seed the Database](#step-3--seed-the-database)
  - [Step 4 — Start the Backend Server](#step-4--start-the-backend-server)
  - [Step 5 — Start the Frontend Server](#step-5--start-the-frontend-server)
  - [Step 6 — Open in Browser](#step-6--open-in-browser)
- [🔐 Login Credentials](#-login-credentials)
- [🧪 Testing Features](#-testing-features)
- [🛠️ Troubleshooting](#️-troubleshooting)
- [📡 API Reference](#-api-reference)

---

## ✨ Features

| Feature | Description |
|--------|-------------|
| 🗺️ **Live Slot Grid** | 48 slots across 3 zones (A/B/C) with real-time green/red status |
| 👑 **Admin Control Center** | Full table view: Name, Email, Car Plate, Slot, Time Remaining, Amount |
| 🕐 **Time Remaining Badge** | Color-coded countdown — green (>30m), amber (<30m), red (expired) |
| 💳 **Mock UPI Payments** | QR-based instant booking without real Razorpay integration |
| 📊 **Live Revenue Tracker** | Admin dashboard shows live ₹ earnings |
| 🔄 **Auto Refresh** | Slot grid refreshes every 3s; admin bookings every 30s |
| 🔐 **Role-Based Access** | Clean separation between User flow and Admin flow |
| 📡 **WebSocket Support** | Real-time slot updates via WebSocket |

---

## 🏗️ Project Structure

```
Smart-Parking-System-main/
│
├── backend/                        # FastAPI backend
│   ├── app/
│   │   ├── api/endpoints/
│   │   │   ├── auth.py             # Register, Login, /me
│   │   │   ├── bookings.py         # Book, Verify, My Bookings, Admin All Active
│   │   │   ├── lots.py             # Parking lot + slot data
│   │   │   └── health.py           # Health check
│   │   ├── db/
│   │   │   ├── models.py           # SQLAlchemy ORM models
│   │   │   └── session.py          # DB session
│   │   ├── schemas/
│   │   │   └── schemas.py          # Pydantic schemas incl. BookingWithUser
│   │   └── core/
│   │       ├── security.py         # JWT auth, password hashing
│   │       └── config.py           # Settings
│   ├── main.py                     # FastAPI app entry point
│   ├── seed_parksmart.py           # DB seeder (admin + 48 slots)
│   └── parksmart.db                # SQLite database (auto-created)
│
└── frontend/                       # Pure HTML/CSS/React frontend
    ├── login.html                  # User login & registration
    ├── admin_login.html            # Dedicated admin login portal
    └── dashboard.html              # Main dashboard (user + admin views)
```

---

## ⚙️ Prerequisites

Before starting, make sure you have:

### 1. Python 3.10+
Download from [python.org/downloads](https://www.python.org/downloads/)

> ⚠️ **CRITICAL:** During installation, check **"Add Python to PATH"**

Verify installation:
```bash
python --version
```

### 2. Git (optional, for cloning)
Download from [git-scm.com](https://git-scm.com/downloads)

---

## 🚀 Installation & Run Guide

> 💡 You will need **2 terminal windows** open simultaneously — one for backend, one for frontend.

---

### Step 1 — Clone / Open the Project

If you have Git:
```bash
git clone https://github.com/HasnainChavhan/smart-parking-system-Booking.git
cd smart-parking-system-Booking
```

Or simply open the project folder in your terminal:
```powershell
cd "c:\Users\91932\Downloads\Smart-Parking-System-main\Smart-Parking-System-main"
```

---

### Step 2 — Set Up the Backend

Open **Terminal Window #1** and run:

```powershell
# Navigate to the backend folder
cd backend

# Create a virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate
```

> ✅ You should see `(venv)` appear at the start of your prompt.

Now install all dependencies:

```powershell
pip install fastapi uvicorn sqlalchemy pydantic pydantic-settings python-jose[cryptography] passlib bcrypt slowapi loguru razorpay email-validator httpx websockets
```

> ☕ This takes ~1-2 minutes. Grab a coffee.

---

### Step 3 — Seed the Database

Still in **Terminal Window #1**, run:

```powershell
python seed_parksmart.py
```

**Expected output:**
```
Recreating database...
Adding Admin user...
Adding ParkSmart Main Lot...
Seeding exactly 48 slots (3 Zones of 16)...
Database seeded successfully with 48 slots!
```

> ✅ This creates `parksmart.db` with the admin account and all 48 parking slots.

---

### Step 4 — Start the Backend Server

Still in **Terminal Window #1**, run:

```powershell
uvicorn main:app --reload --host localhost --port 8000
```

**Expected output:**
```
INFO:     Uvicorn running on http://localhost:8000 (Press CTRL+C to quit)
INFO:     Started reloader process using StatReload
```

> 🔴 **Leave this terminal open! Do NOT close it.**

---

### Step 5 — Start the Frontend Server

Open a **brand new Terminal Window #2** and run:

```powershell
cd "c:\Users\91932\Downloads\Smart-Parking-System-main\Smart-Parking-System-main\frontend"

python -m http.server 5500
```

**Expected output:**
```
Serving HTTP on :: port 5500 (http://[::]:5500/) ...
```

> 🔴 **Leave this terminal open too! Do NOT press Ctrl+C.**

---

### Step 6 — Open in Browser

Open **Chrome / Edge / Brave** and go to:

| Portal | URL |
|--------|-----|
| 👤 **User Login** | http://localhost:5500/login.html |
| 👑 **Admin Login** | http://localhost:5500/admin_login.html |
| 📖 **API Docs (Swagger)** | http://localhost:8000/docs |

---

## 🔐 Login Credentials

| Role | Email | Password |
|------|-------|----------|
| 👑 **Admin** | `admin@parksmart.test` | `admin123` |
| 👤 **User** | Register on login page | Your choice |

> The admin account is automatically created when you run `seed_parksmart.py`.

---

## 🧪 Testing Features

### As a Regular User:
1. Go to `login.html` → Register a new account
2. Click any **🟢 Green slot** on the grid to book it
3. Enter your **Car Number**, **Date**, **Start Time**, **End Time**
4. Click **Pay & Confirm** — booking is instant (mock payment)
5. Click **My Bookings** in the top-right to view your active reservations
6. Click **Cancel Registration** to free up a slot

### As Admin:
1. Go to `admin_login.html` → Login with `admin@parksmart.test` / `admin123`
2. You'll see the **live slot grid** (green = free, red = reserved)
3. Scroll down to the **Admin Control Center** table showing:
   - Slot # | Car Number | User Name | Email Address | Time Remaining | Amount Paid
4. **Time Remaining** badge is color-coded:
   - 🟢 Green = more than 30 minutes left
   - 🟡 Amber = less than 30 minutes left
   - 🔴 Red = expired
5. Click **Revoke** to cancel any booking instantly
6. Click **Clear Slots (Admin)** to reset all parking slots
7. Top-right card shows live **₹ Revenue**

---

## 🛠️ Troubleshooting

| Problem | Solution |
|---------|----------|
| `venv\Scripts\activate` gives an error | Run `Set-ExecutionPolicy RemoteSigned` in PowerShell as Admin, then retry |
| `python` not recognized | Reinstall Python and make sure to check **"Add to PATH"** |
| Port 8000 already in use | Change port: `uvicorn main:app --reload --port 8001` (update `BACKEND_URL` in `dashboard.html`) |
| Port 5500 already in use | Use `python -m http.server 5501` instead |
| "This site can't be reached" on port 5500 | Your frontend server stopped — re-run `python -m http.server 5500` |
| Database errors / wrong data | Delete `backend/parksmart.db`, then re-run `python seed_parksmart.py` |
| Login says "Incorrect credentials" | Make sure you seeded the DB first with `python seed_parksmart.py` |
| Slots not updating live | Check backend is running on port 8000 and WebSocket is connected (green dot in header) |

---

## 📡 API Reference

Base URL: `http://localhost:8000/api/v1`

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/auth/register` | ❌ | Register new user |
| `POST` | `/auth/login` | ❌ | Login, get JWT token |
| `GET` | `/auth/me` | ✅ | Get current user info |
| `GET` | `/lots/` | ❌ | Get all parking lots + slots |
| `GET` | `/lots/1/revenue` | ❌ | Get today's revenue |
| `POST` | `/bookings/verify` | ✅ | Confirm a booking (mock payment) |
| `GET` | `/bookings/my_bookings` | ✅ | Get my active bookings |
| `DELETE` | `/bookings/{id}/cancel` | ✅ | Cancel a booking |
| `GET` | `/bookings/all_active` | ✅ Admin | Get ALL active bookings with user details |
| `GET` | `/health` | ❌ | API health check |

> 📖 Full interactive docs: **http://localhost:8000/docs**

---

<div align="center">

Built with ❤️ by **Hasnain Chavhan**

⭐ Star this repo if it helped you!

</div>
