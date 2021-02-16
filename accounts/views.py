from django.contrib.auth import get_user_model
from rest_framework import status, views, exceptions
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.serializers import UserSerializer, SMSModelSerializer, LogoutSerializer, LoginSerializer, \
    PhoneNumberSerializer
from accounts.services import UserRegistrationService, UserLoginService


class RegisterView(views.APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = UserRegistrationService(serializer.data).execute()
        return Response(response, status=status.HTTP_201_CREATED)


class LoginView(views.APIView):

    def post(self, request):
        serializer = LoginSerializer(data={**request.data})
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        user_token_data = UserLoginService(user).execute()
        return Response(user_token_data, status=HTTP_200_OK)


class LogoutView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = RefreshToken(serializer.data["refresh_token"])
        try:
            token.blacklist()
        except TokenError as exc:
            raise ValidationError(exc)
        return Response(status=status.HTTP_205_RESET_CONTENT)



class SMSView(views.APIView):
    def post(self, request):
        serializer = SMSModelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PhoneNumberView(views.APIView):
    def patch(self, request):
        serializer = PhoneNumberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SomeInfoView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response({"detail": "Some info for registered users"})
