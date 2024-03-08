from rest_framework import serializers

from apps.admins.models import Branches, Menu
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


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branches
        fields = (
            "branch_name",
            "slug",
            "address",
            "phone_number",
            "link_on_2gis",
            "image1",
            "image2",
            "image3",
            "image4",
            "table_quantity",
            "schedule",
        )


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ("name_dish",)


class BranchesMenuSerializer(serializers.ModelSerializer):
    menu = MenuSerializer(many=True, read_only=True)

    class Meta:
        model = Branches
        fields = ("branch_name", "menu")
