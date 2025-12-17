from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Quiz
from .serializers import QuizCreateSerializer
from .permissions import IsEducator

class QuizCreateView(generics.CreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizCreateSerializer
    permission_classes = [IsAuthenticated, IsEducator]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
