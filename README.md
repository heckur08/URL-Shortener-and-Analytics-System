# 🔗 URL Shortener & Analytics System

A **FastAPI-based backend project** that shortens long URLs, redirects users via custom short codes, tracks clicks (timestamp, IP), and uses **Redis for caching**. Inspired by systems like Bitly, this project emphasizes performance, analytics, and system design.

---

## 🚀 Features

* 🔹 Shorten any long URL into a 6-character code
* 🔹 Redirect using the short URL
* 🔹 Log each click (IP + timestamp)
* 🔹 View click statistics via REST API
* 🔹 Redis caching for faster redirection
* 🔹 Simple frontend UI (HTML + JS)
* 🔹 Scalable database design with MySQL
* 🔹 Rate-limiting & concurrency testing support (bonus)

---

## 🧠 Tech Stack

* **Backend:** FastAPI
* **Database:** MySQL (SQLAlchemy ORM)
* **Cache:** Redis (via `redis-py`)
* **Frontend:** Vanilla JS + HTML
* **Testing:** `pytest` (optional)
* **Load Testing:** ApacheBench or Locust (optional)

---

## 📁 Folder Structure

```
url_shortener/
├── main.py              # FastAPI app
├── models.py            # SQLAlchemy models
├── database.py          # DB engine setup
├── static/
│   ├── index.html       # Frontend page
│   └── script.js        # JS logic for frontend
├── tests/
│   └── test_main.py     # (Optional) Unit tests
├── requirements.txt     # Python deps
└── README.md
```

---

## 🔧 Setup Instructions

### 1. 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install fastapi uvicorn sqlalchemy pymysql redis
```

---

### 2. 🛠️ Database Setup

#### MySQL Table Schema:

```sql
CREATE DATABASE url_shortener;

USE url_shortener;

CREATE TABLE urls (
    id INT PRIMARY KEY AUTO_INCREMENT,
    long_url TEXT NOT NULL,
    short_code VARCHAR(10) UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE clicks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    short_code VARCHAR(10),
    timestamp DATETIME,
    ip_address VARCHAR(45)
);
```

Update your `database.py` connection string:

```python
DATABASE_URL = "mysql+pymysql://<user>:<password>@localhost/url_shortener"
```

---

### 3. 🚀 Run the App

```bash
uvicorn main:app --reload
```

App will be available at:
`http://localhost:8000`

---

### 4. 🖥️ Frontend Usage

Open in browser:
`http://localhost:8000`

* Paste a long URL → Get a short one
* Use the short link to redirect
* Check stats by entering the short code

---

## 📊 API Endpoints

### 🔹 POST `/shorten`

```json
Request:
{ "long_url": "https://example.com" }

Response:
{ "short_url": "http://localhost:8000/abc123" }
```

---

### 🔹 GET `/{short_code}`

Redirects to the original long URL and logs click metadata.

---

### 🔹 GET `/stats/{short_code}`

Returns analytics:

```json
{
  "short_code": "abc123",
  "long_url": "https://example.com",
  "total_clicks": 2,
  "click_logs": [
    { "timestamp": "2025-06-06T12:34:56", "ip": "127.0.0.1" }
  ]
}
```

---

## ⚙️ Redis Caching (Optional but Recommended)

* Speeds up redirection
* Caches long URL for `short_code` for 1 hour
* Modify TTL as needed:

```python
r.set(short_code, long_url, ex=3600)
```

---

## 🧪 Testing

#### Concurrency:

```bash
ab -n 1000 -c 50 http://localhost:8000/abc123
```

#### Unit Tests (Optional):

```bash
pytest tests/
```

---

## 📝 Future Improvements

* Add user login / authentication
* UI for managing all shortened links
* Custom short code support
* Rate limiting per IP using Redis

---

## 📌 Author

**Anurag Singh**
[GitHub Profile](https://github.com/heckur08)
B.Tech, IIT Patna | Backend & Systems Enthusiast
