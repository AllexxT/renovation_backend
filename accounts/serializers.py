from django.contrib.auth import password_validation
from rest_framework import serializers, exceptions
from twilio.rest import Client

from accounts.models import User, SMSModel


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "business_name"
        ]

    def validate_password(self, password):
        password_validation.validate_password(password)
        return password


class SMSModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMSModel
        fields = [
            'number'
        ]

    def validate(self, data):
        if data.get("number") < 20:
            account_sid = "AC05755a0649f04630367561dfa6ff10f4"
            auth_token = "9608af3ee71e120bf1e1970263a73861"
            client = Client(account_sid, auth_token)

            try:
                message = client.messages.create(
                    body='Test Message',
                    from_='+15707558188',
                    to='+380682724293'
                )
                print(message)
            except Exception as e:
                print(e)
        return data


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=150, required=True)
    password = serializers.CharField(max_length=32, required=True)

    def validate(self, attrs):
        self.user = User.objects.filter(
            email=attrs.get("email")
        ).first()
        if not self.user:
            raise exceptions.AuthenticationFailed("Bad credentials!")
        if not self.user.check_password(attrs.get("password")):
            raise exceptions.ValidationError({"error": "Bad credentials"})
        return attrs

class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=256)
