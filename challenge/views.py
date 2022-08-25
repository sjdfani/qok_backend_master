from rest_framework.views import APIView
from challenge.models import Challenge
from .serializers import ChallengeReqSerializer, ChallengeSerializer, RetrieveChallengeReqSerializer, ChallengeCategorySerializer, ChallengeAnswerSerializer, ChallengeResultSerializer, ChallengeGiveUpSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.generics import ListAPIView
from django.db.models import Q
from account.models import Account
from .models import ChallengeResult, StateChallenge


class CreateOrFindMatch(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ChallengeReqSerializer(
            data=request.data, context={'request': request}
        )
        obj, challenge_request_found = serializer.save()
        if challenge_request_found:
            return Response(
                ChallengeSerializer(obj, context={'request': request}).data
            )
        else:
            return Response(
                RetrieveChallengeReqSerializer(
                    obj, context={'request': request}).data
            )


class CreateChallengeCategory(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChallengeCategorySerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class CreateChallengeAnswer(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChallengeAnswerSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class OpenChallengeList(ListAPIView):
    serializer_class = ChallengeSerializer
    Permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        account = Account.objects.filter(user=user).first()
        lookup = Q(account_1=account) | Q(account_2=account)
        return Challenge.objects.filter(lookup, state=StateChallenge.IN_CHALLENGE, is_archived=False)


class EndChallengeList(ListAPIView):
    serializer_class = ChallengeSerializer
    Permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        account = Account.objects.filter(user=user).first()
        lookup = Q(account_1=account) | Q(account_2=account)
        return Challenge.objects.filter(lookup, state=StateChallenge.END_CHALLENGE, is_archived=False)


class ChallengeResultView(ListAPIView):
    serializer_class = ChallengeResultSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        challenge_id = self.request.data.get('challenge_id')
        lookup = Q(challenge=challenge_id) & Q(account__user=self.request.user)
        return ChallengeResult.objects.filter(lookup)


class ChallengeGiveUp(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChallengeGiveUpSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_200_OK)
