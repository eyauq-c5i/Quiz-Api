from django.utils import timezone
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import OpenApiParameter

from .models import Quiz, QuizAttempt, StudentAnswer
from .serializers import (
    QuizCreateSerializer,
    QuizSerializer,
    StudentAnswerSerializer,
    QuizAttemptSerializer,
)
from .permissions import IsEducator


# Educator: Create quiz
@extend_schema(
    summary="Create a quiz",
    description="Educators can create quizzes with questions, answers, and optional time limits.",
    request=QuizCreateSerializer,
    responses={201: QuizSerializer},
    tags=["Quizzes"]
)
class QuizCreateView(generics.CreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizCreateSerializer
    permission_classes = [IsAuthenticated, IsEducator]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


# Student + Educator: List quizzes
@extend_schema(
    summary="List quizzes",
    description="Retrieve all available quizzes.",
    responses={200: QuizSerializer(many=True)},
    tags=["Quizzes"]
)
class QuizListView(generics.ListAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]


# Student + Educator: Retrieve single quiz
@extend_schema(
    summary="Retrieve a quiz",
    description="Get quiz details including questions and answers.",
    responses={200: QuizSerializer},
    tags=["Quizzes"],
    parameters=[
        OpenApiParameter(
            name="pk",
            description="ID of the quiz",
            required=True,
            type=int
        )
    ]
)
class QuizDetailView(generics.RetrieveAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]


# Student: Attempt and submit quiz (time-limited)
@extend_schema(
    summary="Submit quiz answers",
    description=(
        "Submit answers for a quiz attempt. "
        "Late submissions are rejected for timed quizzes."
    ),
    request=StudentAnswerSerializer(many=True),
    responses={
        200: {
            "type": "object",
            "properties": {
                "message": {"type": "string"},
                "score": {"type": "integer"},
                "started_at": {"type": "string"},
                "completed_at": {"type": "string"},
            }
        },
        403: {"description": "Time expired"},
        403: {"description": "Quiz not found"},
    },
    tags=["Attempts"],
    parameters=[
        OpenApiParameter(
            name="quiz_id",
            description="ID of the quiz",
            required=True,
            type=int
        )
    ]
)
class SubmitQuizView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, quiz_id):
        try:
            quiz = Quiz.objects.get(id=quiz_id)
        except Quiz.DoesNotExist:
            return Response(
                {"detail": "Quiz not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Get or create attempt
        attempt, created = QuizAttempt.objects.get_or_create(
            student=request.user,
            quiz=quiz,
            defaults={'started_at': timezone.now()}
        )

        # Enforce time limit
        if quiz.duration_minutes > 0:
            end_time = attempt.started_at + timezone.timedelta(
                minutes=quiz.duration_minutes
            )
            if timezone.now() > end_time:
                attempt.completed_at = end_time
                attempt.save()
                return Response(
                    {"detail": "Time is up! You cannot submit answers."},
                    status=status.HTTP_403_FORBIDDEN
                )

        # Process answers
        answers_data = request.data.get('answers', [])
        serializer = StudentAnswerSerializer(data=answers_data, many=True)
        serializer.is_valid(raise_exception=True)

        for ans_data in serializer.validated_data:
            StudentAnswer.objects.update_or_create(
                student=request.user,
                question=ans_data['question'],
                defaults={'selected_answer': ans_data['selected_answer']}
            )

        # Calculate score
        score = 0
        for ans in StudentAnswer.objects.filter(
            student=request.user,
            question__quiz=quiz
        ):
            if ans.selected_answer.is_correct:
                score += 1

        # Save attempt
        attempt.score = score
        attempt.completed_at = timezone.now()
        attempt.save()

        return Response({
            "message": "Quiz submitted successfully",
            "score": score,
            "started_at": attempt.started_at,
            "completed_at": attempt.completed_at
        })


# Student: View attempt history
@extend_schema(
    summary="Quiz attempt history",
    description="Retrieve the authenticated user's quiz attempt history.",
    responses={200: QuizAttemptSerializer(many=True)},
    tags=["Attempts"]
)
class QuizAttemptHistoryView(generics.ListAPIView):
    serializer_class = QuizAttemptSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return QuizAttempt.objects.filter(student=self.request.user)
