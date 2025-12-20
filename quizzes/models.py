from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


User = settings.AUTH_USER_MODEL


class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='quizzes'
    )
    created_at = models.DateTimeField(auto_now_add=True)

# New field for time-limited quizzes
    duration_minutes = models.PositiveIntegerField(
        default=0,
        help_text="Duration of quiz in minutes (0 = unlimited)"
    )

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name='questions'
    )
    text = models.TextField()

    def __str__(self):
        return self.text[:50]


class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers'
    )
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class StudentAnswer(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.ForeignKey(Answer, on_delete=models.CASCADE)


class QuizAttempt(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    started_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)  # null if quiz not finished

    class Meta:
        unique_together = ('student', 'quiz')

    def __str__(self):
        return f"{self.student.username} - {self.quiz.title}"
