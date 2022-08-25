from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveDestroyAPIView,ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Question, ReportQuestion, StateChoices
from .serializer import CreateQuestionSerializer, ReportQuestionSerializer, QuestionSerializer


class CreateQuestion(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreateQuestionSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class RetrieveDeleteQuestion(RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = QuestionSerializer

    def get_queryset(self):
        return Question.objects.filter(user=self.request.user)


class ReportQuestionView(ListCreateAPIView):
    queryset = ReportQuestion.objects.all()
    serializer_class = ReportQuestionSerializer
    permission_classes = [IsAuthenticated]


class QuestionByCategory(ListAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        category = self.request.GET.get('category')
        return Question.objects.filter(category__name=category, state=StateChoices.ACCEPT)


class QuestionWithAcceptState(ListAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Question.objects.filter(user=user, state=StateChoices.ACCEPT)


class QuestionWithPendingState(ListAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Question.objects.filter(user=user, state=StateChoices.PENDING)


class QuestionWithFailedState(ListAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Question.objects.filter(user=user, state=StateChoices.FAILED)
