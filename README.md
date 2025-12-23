#Quiz API
A Django REST Framework (DRF) backend for managing quizzes, supporting time-limited attempts, multiple-choice questions, student answers, and educator quiz creation.


#Features
✅ Quiz Management
Educators can create quizzes with multiple questions and answers.
Each quiz can have an optional time limit (duration_minutes).

✅ Question & Answer Management
Supports multiple-choice questions.
Each answer has a boolean is_correct flag.
Students can submit answers per question.

✅ Time-Limited Quizzes
Each quiz can have a duration_minutes limit.
Tracks when the attempt starts (started_at) and finishes (completed_at).
Prevents submission if time expires.

✅ Student Quiz Attempts
Tracks quiz attempts per student.
Calculates and stores score automatically.
Optionally prevents multiple attempts per quiz.

✅ APIs
List all quizzes
Retrieve a single quiz
Create a quiz (educators only)
Submit/attempt a quiz
View quiz attempt history


✅User End-points
#Register
URL: http://127.0.0.1:8000/api/auth/register/
Method: POST
Body (JSON):

{
  "username": "kofi",
  "email": "kofi@test.com",
  "password": "thefreshboy123",
  "role": "student"
}


#Login
URL: http://127.0.0.1:8000/api/auth/token/
Method: POST
Body (JSON):

**Educator
{
  "username": "jeff",
  "password": "wawolo123"
}

**Student
{
  "username": "kofi",
  "password": "thefreshboy123"
}


#Create Quiz (Educator only)
URL: http://127.0.0.1:8000/api/quizzes/create/
Method: POST
Headers:
Authorization: Bearer <access_token>

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
    },
    {
      "text": "5-3?",
      "answers": [
        {"text": "2", "is_correct": true},
        {"text": "3", "is_correct": false}
      ]
    }
  ]
}


#List Quizzes (All users)
URL: http://127.0.0.1:8000/api/quizzes/
Method: GET
Headers:
Authorization: Bearer <access_token>


#Retrieve Quiz (All users)
URL: http://127.0.0.1:8000/api/quizzes/<quiz_id>/
Method: GET
Headers:
Authorization: Bearer <access_token>


#Submit Quiz Answers (Student only)
URL: /api/quizzes/<quiz_id>/submit/
Method: POST
Headers:
Authorization: Bearer <access_token>

{
  "answers": [
    {
      "question": 1,
      "selected_answer": 2
    },
    {
      "question": 2,
      "selected_answer": 3
    }
  ]
}


#Quiz Attempt History (Student only)
URL: /api/quizzes/attempts/
Method: GET
Headers:
Authorization: Bearer <access_token>