from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Quiz, QuizAttempt
from .serializers import (
    QuizCreateSerializer,
    QuizSerializer,
    StudentAnswerSerializer,
    QuizAttemptSerializer,
)
from .permissions import IsEducator


# Educator: Create quiz
class QuizCreateView(generics.CreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizCreateSerializer
    permission_classes = [IsAuthenticated, IsEducator]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


# Student + Educator: List quizzes
class QuizListView(generics.ListAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]


# Student + Educator: Retrieve single quiz
class QuizDetailView(generics.RetrieveAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]


class SubmitQuizView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, quiz_id):
        answers = request.data.get('answers', [])
        score = 0

        for ans in answers:
            serializer = StudentAnswerSerializer(data=ans)
            serializer.is_valid(raise_exception=True)

            student_answer = serializer.save(student=request.user)

            if student_answer.selected_answer.is_correct:
                score += 1

        return Response({
            "message": "Quiz submitted successfully",
            "score": score
        })


class SubmitQuizView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, quiz_id):
        quiz = Quiz.objects.get(id=quiz_id)

        # Prevent retakes
        if QuizAttempt.objects.filter(student=request.user, quiz=quiz).exists():
            return Response(
                {"detail": "You have already taken this quiz."},
                status=400
            )

        answers = request.data.get('answers', [])
        score = 0

        for ans in answers:
            serializer = StudentAnswerSerializer(data=ans)
            serializer.is_valid(raise_exception=True)
            student_answer = serializer.save(student=request.user)

            if student_answer.selected_answer.is_correct:
                score += 1

        QuizAttempt.objects.create(
            student=request.user,
            quiz=quiz,
            score=score
        )

        return Response({
            "message": "Quiz submitted successfully",
            "score": score
        })


class QuizAttemptHistoryView(generics.ListAPIView):
    serializer_class = QuizAttemptSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return QuizAttempt.objects.filter(student=self.request.user)