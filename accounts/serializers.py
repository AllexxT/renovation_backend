from django.contrib.auth import password_validation
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers, exceptions
from twilio.rest import Client

from accounts.models import User, SMSModel


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, write_only=True)

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
            auth_token = "ae0caa03280e465c5f265840ab36e133"
            client = Client(account_sid, auth_token)

            try:
                message = client.messages.create(
                    body='Test Message',
                    from_='+15707558188',
                    to='+15628024809'
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


class PhoneSerializer(serializers.Serializer):
    phone = PhoneNumberField()


class PhoneNumberSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    phone = PhoneNumberField(source="phone_number")

    def validate(self, attrs):
        self._user = User.objects.filter(email=attrs.get("email")).first()
        if not self._user:
            raise exceptions.ValidationError("User doesn't exist")
        self._user.phone_number = attrs.get("phone_number")
        self._user.save()
        return attrs

    class Meta:
        model = User
        fields = ("phone", "email")


# raise exceptions.ValidationError(
#     detail={"detail": f"Twilio: {ex}"},
# )