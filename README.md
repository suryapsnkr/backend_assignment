# Backend Assignment - Complete

This project contains the following:

✅ Google OAuth 2.0 Login  
✅ Google Drive Integration (Upload, List, Download)  
✅ Real-time WebSockets Chat (Between two users)

## Setup Instructions

1️⃣ Install dependencies:
```bash
pip install -r requirements.txt
```

2️⃣ Run Migrations:
```bash
python manage.py migrate
```

3️⃣ Start Redis (for WebSockets):
```bash
docker run -p 6379:6379 redis
```

4️⃣ Run server:
```bash
python manage.py runserver
```

## Test Using Postman
Import the provided `backend_assignment.postman_collection.json` into Postman to test all endpoints.
