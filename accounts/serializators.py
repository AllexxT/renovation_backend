from django.contrib.auth import password_validation
from rest_framework import serializers

from accounts.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
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

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
