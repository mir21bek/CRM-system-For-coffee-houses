from rest_framework import serializers
from apps.user_app.models import CustomUser


class EmployeeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "role",
            "email",
            "full_name",
            "date_of_birth",
            "phone_number",
            "password",
            "login",
        )

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = CustomUser.objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user
