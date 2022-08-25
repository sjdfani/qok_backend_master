from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from QOK.settings import Redis_object
from user.models import CustomUser
from .serializer import RegisterSerializer, LoginSerializer, RestorePasswordVerifySerializer, RestorePasswordSerializer
from .utils import get_tokens_for_user
from account.models import Account, Level


class Register(APIView):

    def post(self, request):
        serializer = RegisterSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_200_OK)


class Verify(APIView):

    def get(self, request):
        url = request.GET.get('u')
        original_url_list = urlsafe_base64_decode(
            force_str(url)).decode('utf-8').split('/')
        redis_data = Redis_object.get(original_url_list[0])
        if redis_data is not None:
            redis_data_list = redis_data.split('/')
            if original_url_list[1] == redis_data_list[1]:
                user = CustomUser.objects.create(
                    email=original_url_list[0], password=redis_data_list[0])
                account = Account.objects.create(user=user, coin=0)
                Level.objects.create(
                    account=account, stage=1, minimum=0, maximum=10)
                return Response({'message': 'done'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'error'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'link was expired.'}, status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):

    def post(self, request):
        login_serializer = LoginSerializer(data=request.data)
        if login_serializer.is_valid(raise_exception=True):
            email = login_serializer.validated_data['email']
            password = login_serializer.validated_data['password']
            user_exists = CustomUser.objects.filter(email=email).exists()
            if user_exists:
                user = CustomUser.objects.filter(email=email).first()
                if user.check_password(password):
                    tokens = get_tokens_for_user(user)
                    return Response(tokens, status=status.HTTP_200_OK)
                else:
                    return Response({'password': 'password is incorrect.'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'email': 'email is not exist.'}, status=status.HTTP_404_NOT_FOUND)


class RestorePassword(APIView):

    def post(self, request):
        serializer = RestorePasswordSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'done'}, status=status.HTTP_200_OK)


class RestorePasswordVerify(APIView):

    def post(self, request):
        serializer = RestorePasswordVerifySerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
