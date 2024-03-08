from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

from apps.admins.models import Branches, Menu
from apps.admins.serializers import (
    EmployeeCreateSerializer,
    BranchSerializer,
    BranchesMenuSerializer,
)
from apps.user_app.models import CustomUser
from apps.user_app import permissions


class BranchCreateAPIView(APIView):
    permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(
        request_body=BranchSerializer,
        responses={
            201: "Branch created successfully",
            400: "Bad request or Schedule is missing",
            403: "You are not authorized to perform this action",
            404: "Menu not found",
        },
    )
    def post(self, request):
        serializer = BranchSerializer(data=request.data)
        if serializer.is_valid():
            branch = serializer.save()
            common_menus = Menu.objects.all()
            branch.menu.set(common_menus)
            schedule = request.data.get("schedule")
            if schedule:
                branch.schedule.set(schedule)
                return Response(
                    "Branch created successfully", status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    "Schedule is missing", status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeCreateAPIView(APIView):
    @swagger_auto_schema(
        request_body=EmployeeCreateSerializer,
        responses={
            201: "Admin created successfully",
            400: "Only superuser can create admins",
            201: "Employee created successfully",
            403: "You don't have permission to perform this action.",
        },
    )
    def post(self, request):
        serializer = EmployeeCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user_data = serializer.validated_data
            if request.user.is_super_admin or request.user.is_superuser:
                CustomUser.objects.create_user(**user_data)
                return Response(
                    "Admin created successfully", status=status.HTTP_201_CREATED
                )
            elif not request.user.is_super_admin or not request.user.is_superuser:
                return Response(
                    "Only superuser or super admin can create admins",
                    status=status.HTTP_400_BAD_REQUEST,
                )
            elif request.user.role.admin or request.user.is_super_admin:
                CustomUser.objects.create(**user_data)
                return Response(
                    "Employee created successfully", status=status.HTTP_201_CREATED
                )
        else:
            return Response(
                "You don't have permission to perform this action.",
                status=status.HTTP_403_FORBIDDEN,
            )


class MenuAPIView(generics.ListAPIView):
    queryset = Branches.objects.all()
    serializer_class = BranchesMenuSerializer
