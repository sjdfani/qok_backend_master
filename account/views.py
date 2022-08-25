from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.views import APIView
from .models import Account, CoinLog
from .serializers import AccountSerializer, CoinLogSerializer, UpdateAccountSerializer, UpdateIconAccountSerializer, TotalGamesSerializer, SummaryCategorySerializer
from rest_framework.views import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from challenge.models import ChallengeAnswer
from django.db.models import Count, Q, F


class AccountViewSet(ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [IsAuthenticated, ]
        else:
            self.permission_classes = [IsAdminUser, ]
        return super(AccountViewSet, self).get_permissions()


class CoinLogViewSet(ModelViewSet):
    queryset = CoinLog.objects.all()
    serializer_class = CoinLogSerializer
    permission_classes = [IsAuthenticated]


class UpdateAccount(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UpdateAccountSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateIconAccount(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UpdateIconAccountSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'done'}, status=status.HTTP_200_OK)


class TotalGames(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = TotalGamesSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            result = serializer.save()
            return Response(result, status=status.HTTP_200_OK)


class SummaryCategoryView(ListAPIView):
    serializer_class = SummaryCategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ChallengeAnswer.objects.filter(
            account__user=user).values(
            'challenge_category__category__name').annotate(correct_answers=Count('question', filter=Q(question__correct_answer=F('answer'))), total_answers=Count('question'))
