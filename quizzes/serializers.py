from rest_framework import serializers
from .models import Quiz, Question, Answer, StudentAnswer, QuizAttempt


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'text', 'is_correct')


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ('id', 'text', 'answers')


class QuizCreateSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ('id', 'title', 'description', 'duration_minutes', 'questions')

    def create(self, validated_data):
        questions_data = validated_data.pop('questions')
        quiz = Quiz.objects.create(**validated_data)

        for question_data in questions_data:
            answers_data = question_data.pop('answers')
            question = Question.objects.create(
                quiz=quiz,
                **question_data
            )

            for answer_data in answers_data:
                Answer.objects.create(
                    question=question,
                    **answer_data
                )

        return quiz


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'duration_minutes', 'questions']


class StudentAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAnswer
        fields = ['question', 'selected_answer']

    def validate(self, data):
        question = data['question']
        selected_answer = data['selected_answer']
        if selected_answer.question != question:
            raise serializers.ValidationError("Selected answer does not belong to the question.")
        return data


class QuizAttemptSerializer(serializers.ModelSerializer):
    quiz_title = serializers.CharField(source='quiz.title', read_only=True)

    class Meta:
        model = QuizAttempt
        fields = ['id', 'quiz', 'quiz_title', 'score', 'started_at', 'completed_at']
