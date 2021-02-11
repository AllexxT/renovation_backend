from django.contrib.auth import get_user_model

from accounts.serializators import UserSerializer
from base.services import Service
UserModel = get_user_model()


class UserRegistrationService(Service):

    def __init__(self, user_data):
        self._user_data = user_data
        self.data = {}
        self._user = None

    def execute(self):
        self._create_user()
        self._generate_token()
        return self.data

    def _create_user(self):
        user = UserModel(**self._user_data)
        user.set_password(self._user_data.get("password"))
        user.save()
        self._user = user
        self.data['user'] = UserSerializer(self._user).data

    def _generate_token(self):
        from rest_framework_simplejwt.serializers import (
            TokenObtainPairSerializer,
        )
        refresh = TokenObtainPairSerializer.get_token(self._user)
        self.data["access_token"] = str(refresh.access_token)
        self.data["refresh_token"] = str(refresh)

class UserLoginService(Service):
    pass

class UserTokenService(Service):
    pass