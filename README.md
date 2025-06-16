# 🏋️‍♀️ Fitness Class Booking System

A backend service to manage fitness classes, user registrations, and class bookings. Built with **Flask**, **SQLAlchemy**, and **SQLite**, this API supports user registration/login with token authentication, class creation, and booking features.

---

## 🚀 Features

- Register and login users (email or mobile).
- JWT-based authentication.
- Create and view fitness classes (Zumba, Yoga, HIIT).
- Book classes per user.
- View bookings per user.
- Cancel booking per user.

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/theprateekgoyal2/DreamFyre.git
cd DreamFyre
````

### 2. Set up a Virtual Environment 

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Running the App
```bash
python backend/main.py
```

### 5. Set Up the Database
```bash
python backend/seed.py
```

## 📬 Using Postman

Instead of using curl, you can test the API easily with Postman.

### 📦 Import Postman Collection

1. Open Postman.
2. Click `Import` > `Upload Files`.
3. Select the file: `DreamFyre.postman_collection.json` from this repo.
4. Once imported, you’ll see a collection named **DreamFyre API** with all the available endpoints.

### ⚙️ Set Up Environment (Optional)

1. Create a Postman environment (e.g. `DreamFyre Local`).
2. Add a variable named `base_url` with value: http://127.0.0.1:5000
3. Add a variable named `token` to store your auth token after login.
4. Use `{{base_url}}` and `{{token}}` in your requests.

### ▶️ Example Flow

1. **Register/Login** a user using the `Register` or `Login` request.
2. **Copy the token** from the login response and set it as the `token` environment variable.
3. Use the remaining requests like:
- `Create Class`
- `Get Fitness Classes`
- `Book Class`
- `Get User Bookings`

---
### 📁 Postman Collection Location

The collection is located at: 
> /DreamFyre.postman_collection.json

> If you're cloning this repo, just import the file directly into Postman and you're good to go!
