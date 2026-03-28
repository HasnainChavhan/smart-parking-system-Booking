# 🚘 Smart Parking System

Welcome to the **Smart Parking System**! This is a modern, real-time web application built with FastAPI (Backend) and React/TailwindCSS (Frontend). 

This guide provides a complete, foolproof, step-by-step installation guide to get the project running locally from scratch.

---

## 🌟 Core Features
- **Premium Dark-Mode UI**: Built natively with Tailwind CSS and React for a lag-free experience.
- **Live Websocket Updates**: As soon as a car is parked or a slot is booked, the UI updates instantly for all connected users without refreshing.
- **Secure JWT Authentication**: Enterprise-grade login and registration flow.
- **Razorpay Integration**: Built-in payment gateway structures for real transactions.
- **Admin Dashboard**: Hidden revenue metrics and administrative mass-clear actions specifically reserved for management accounts.

---

## 🛠 Prerequisites
Before you start, ensure you have the following installed on your machine:
- **Python (3.9 or higher)**
- **Git** (optional, to clone the repo)
- A code editor like **VS Code**

---

## 🚀 Step-by-Step Installation Guide

### Step 1: Set Up the Backend Environment
Open your terminal and navigate to the project folder, then move into the `backend/` directory.

```bash
cd Smart-Parking-System-main
cd backend
```

Create a virtual environment (this isolates your python packages safely):
```bash
python -m venv venv
```

Activate the virtual environment:
- **Windows:** `venv\Scripts\activate`
- **Mac/Linux:** `source venv/bin/activate`

Install all required Python libraries:
```bash
pip install -r requirements.txt
```

### Step 2: Initialize the Database
We use a lightweight, serverless **SQLite** database (`sql_app.db`) to store users and parking slots safely. You need to "seed" (initialize) it before first boot!

Run the seeding script (while still inside the `backend/` folder):
```bash
python seed_parksmart.py
```
*This will automatically generate the 48 parking slots and your root Admin credential.*

### Step 3: Start the Backend Server
Now it's time to bring the API online! Keep your terminal open and run:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```
> **✅ Success Check:** You should see `Uvicorn running on http://0.0.0.0:8000` in your terminal. Leave this terminal window running in the background!

### Step 4: Start the Frontend Application
Open a **completely new terminal window**, and navigate to the root of the project (not the backend folder).

We will use Python's built-in web server to host the HTML files on port `5555`.
```bash
cd Smart-Parking-System-main
python -m http.server 5555 --directory frontend
```

### Step 5: Launch the App in your Browser
Open Google Chrome or Firefox and type this exact URL into the top bar:
🔗 **http://localhost:5555/login.html**

---

## 🔑 Default Administrator Login
Use the following credentials to log in. The system will recognize this specific account and automatically unlock the hidden **Revenue Viewer** and **Clear Slots** management buttons on the UI grid!

- **Email:** `admin@parksmart.test`
- **Password:** `admin123`

*(Note: You can use the "Create Account" tab to register standard non-admin drivers directly from the UI!)*

---

## 🩺 Quick Troubleshooting for Juniors
1. **Network Error on Login:** This means your Backend server (Step 3) crashed or isn't running. Check the first terminal for Python errors! 
2. **"Address already in use" Error:** This means port 8000 or 5555 is being used by another app. Restart your computer or kill the python task in Task Manager to free the ports up.
3. **Seeing the Database:** If you want to view the literal rows and columns inside `parksmart.db`, go to the VS Code extension marketplace and download **"SQLite Viewer"**.

---
*Developed for the Smart Parking Pro Initiative.*
