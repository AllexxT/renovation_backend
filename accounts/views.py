from django.contrib.auth import get_user_model
from rest_framework import status, views
from rest_framework.response import Response

from accounts.serializators import UserSerializer, SMSModelSerializer
from accounts.services import UserRegistrationService


class RegisterView(views.APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = UserRegistrationService(serializer.data).execute()
        return Response(response, status=status.HTTP_201_CREATED)


class LoginView(views.APIView):
    pass


class TokenRefreshView(views.APIView):
    pass


class LogoutView(views.APIView):
    pass


class SMSView(views.APIView):
    def post(self, request):
        serializer = SMSModelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
