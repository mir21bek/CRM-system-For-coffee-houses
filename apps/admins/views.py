from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.admins.serializers import EmployeeCreateSerializer
from apps.user_app.models import CustomUser


class BranchAPIView(APIView):
    pass


class EmployeeCreateAPIView(APIView):
    @swagger_auto_schema(
        request_body=EmployeeCreateSerializer,
        responses={201: "Code send successfully", 400: "Bad request"},
    )
    def post(self, request):
        serializer = EmployeeCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user_data = serializer.validated_data
            if request.user.is_superuser:
                CustomUser.objects.create_user(**user_data)
                return Response(
                    "Employee created successfully", status=status.HTTP_201_CREATED
                )
            elif request.user.role.admin:
                if user_data.get("admin", False) or user_data.get(
                    "is_superuser", False
                ):
                    return Response(
                        "Only superuser can create admins",
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                else:
                    CustomUser.objects.create(**user_data)
                    return Response(
                        "Employee created successfully", status=status.HTTP_201_CREATED
                    )
            else:
                return Response(
                    "You don't have permission to perform this action.",
                    status=status.HTTP_403_FORBIDDEN,
                )
