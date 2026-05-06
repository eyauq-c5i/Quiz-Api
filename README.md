# Quiz API

A Django REST Framework (DRF) backend for managing quizzes.
Supports time-limited attempts, multiple-choice questions, student submissions, and educator quiz creation.

---

## 🚀 Features

### Quiz Management

* Educators can create quizzes with multiple questions and answers
* Optional time limit using `duration_minutes`

### Question & Answer Management

* Multiple-choice questions supported
* Each answer includes an `is_correct` flag
* Students submit one answer per question

### Time-Limited Quizzes

* Tracks `started_at` and `completed_at`
* Prevents submissions after time expires

### Student Quiz Attempts

* Tracks attempts per student
* Automatically calculates and stores scores
* Optional restriction on multiple attempts

---

## ⚙️ Tech Stack

* Python
* Django
* Django REST Framework
* MySQL
* JWT Authentication

---

## 🔐 Authentication

Uses JWT (Bearer Token)

Header format:

```
Authorization: Bearer <access_token>
```

---

## 📌 API Endpoints

### 1. Register User

**POST** `/api/auth/register/`

```json
{
  "username": "kofi",
  "email": "kofi@test.com",
  "password": "thefreshboy123",
  "role": "student"
}
```

---

### 2. Login (Get Token)

**POST** `/api/auth/token/`

```json
{
  "username": "kofi",
  "password": "thefreshboy123"
}
```

---

### 3. Create Quiz (Educators Only)

**POST** `/api/quizzes/create/`

```json
{
  "title": "Math Quiz",
  "description": "Simple math questions",
  "duration_minutes": 10,
  "questions": [
    {
      "text": "2+2?",
      "answers": [
        {"text": "3", "is_correct": false},
        {"text": "4", "is_correct": true}
      ]
    }
  ]
}
```

---

### 4. List Quizzes

**GET** `/api/quizzes/`

---

### 5. Retrieve Quiz

**GET** `/api/quizzes/<quiz_id>/`

---

### 6. Submit Quiz Answers (Students Only)

**POST** `/api/quizzes/<quiz_id>/submit/`

```json
{
  "answers": [
    {
      "question": 1,
      "selected_answer": 2
    }
  ]
}
```

---

### 7. Quiz Attempt History (Students Only)

**GET** `/api/quizzes/attempts/`

---

## 🧪 Running Locally

1. Clone the repository
2. Create a virtual environment
3. Install dependencies:

```
pip install -r requirements.txt
```

4. Run migrations:

```
python manage.py migrate
```

5. Start server:

```
python manage.py runserver
```

---

## 📌 Notes

* Only educators can create quizzes
* Only students can submit answers
* Ensure token is included in protected routes
* Time-limited quizzes will reject late submissions

---

## 📄 License

This project is for learning and educational purposes.
