from django.urls import path
from .views import (
    QuizCreateView,
    QuizListView,
    QuizDetailView,
    SubmitQuizView,
    QuizAttemptHistoryView,
)

urlpatterns = [
    # List all quizzes (student + educator)
    path('quizzes/', QuizListView.as_view(), name='quiz-list'),

    # Retrieve a single quiz
    path('quizzes/<int:pk>/', QuizDetailView.as_view(), name='quiz-detail'),

    # Educator: Create a new quiz
    path('quizzes/create/', QuizCreateView.as_view(), name='quiz-create'),

    # Student: Submit or attempt a quiz (time-limited)
    path('quizzes/<int:quiz_id>/submit/', SubmitQuizView.as_view(), name='submit-quiz'),

    # Student: View quiz attempt history
    path('attempts/', QuizAttemptHistoryView.as_view(), name='quiz-attempt-history'),
]
