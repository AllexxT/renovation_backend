from django.contrib.auth import get_user_model
from rest_framework import status, views
from rest_framework.response import Response

from accounts.serializators import UserRegisterSerializer


class RegisterView(views.APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)


class LoginView(views.APIView):
    pass


class TokenRefreshView(views.APIView):
    pass


class LogoutView(views.APIView):
    pass
