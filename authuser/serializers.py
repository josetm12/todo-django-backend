# authuser/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )

    class Meta:
        model = User
        fields = ("id", "email", "password", "first_name", "last_name")
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name")
