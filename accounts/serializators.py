from django.contrib.auth import password_validation
from rest_framework import serializers
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
            auth_token = "db414dff9f750d29953d4c7c508b4d41"
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
