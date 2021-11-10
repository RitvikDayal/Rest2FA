from django.contrib.auth import authenticate

from rest_framework import serializers

from accounts.models import User
from accounts.utils import get_tokens_for_user


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration
    """

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "password", "email")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data["password"])
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for 1FA login authentication.
    """

    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    user_name = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                "User with given email and password does not exists."
            )
        try:
            tokens = get_tokens_for_user(user)

        except User.DoesNotExist:
            raise serializers.ValidationError(
                "User with given email and password does not exists"
            )
        return {
            "user_name": user.get_full_name,
            "email": user.email,
            "tokens": tokens,
        }
