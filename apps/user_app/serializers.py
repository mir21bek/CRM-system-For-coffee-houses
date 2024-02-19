from rest_framework import serializers
from .models import CustomUser


class CustomRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, help_text="Введите адрес эл. почты")

    class Meta:
        model = CustomUser
        fields = ("email",)

    def create(self, validated_data):
        validated_data["role"] = "client"
        return CustomUser.objects.create(**validated_data)
