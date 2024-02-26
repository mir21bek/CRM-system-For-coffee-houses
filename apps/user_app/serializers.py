from rest_framework import serializers
from .models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, help_text="Введите адрес эл. почты")

    class Meta:
        model = CustomUser
        fields = (
            "full_name",
            "email",
        )

    def create(self, validated_data):
        validated_data["role"] = "client"
        return CustomUser.objects.create(**validated_data)


class CheckOtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("otp",)


class BaseLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, help_text="Введите адрес эл. почты")

    def validate_role(self, value):
        if value not in CustomUser.ROLE:
            raise serializers.ValidationError("Недопустимая роль")
        return value


class ClientLoginSerializer(BaseLoginSerializer):
    def create(self, validated_data):
        validated_data["role"] = "client"
        return CustomUser.objects.create(**validated_data)


class AdminLoginSerializer(BaseLoginSerializer):
    def create(self, validated_data):
        validated_data["role"] = "admin"
        return CustomUser.objects.create(**validated_data)


class BaristaLoginSerializer(BaseLoginSerializer):
    def create(self, validated_data):
        validated_data["role"] = "barista"
        return CustomUser.objects.create(**validated_data)


class WaiterLoginSerializer(BaseLoginSerializer):
    def create(self, validated_data):
        validated_data["role"] = "barista"
        return CustomUser.objects.create(**validated_data)
