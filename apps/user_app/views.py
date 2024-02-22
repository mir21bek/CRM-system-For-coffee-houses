from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from .serializers import RegisterSerializer, CheckOtpSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from utils.services.send_email import check_and_activate
import logging
from apps.user_app.models import CustomUser
from apps.user_app.tasks import send_otp_code
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone

logger = logging.getLogger("main")


class ClientRegisterAPIView(APIView):
    @swagger_auto_schema(
        request_body=RegisterSerializer,
        responses={201: "Code send successfully", 400: "Bad request"},
    )
    def post(self, request):
        logger.error("client register class")
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            send_otp_code.delay(user.id)
            return Response(
                {"massage": "Code send successfully", "user email": user.email},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckOtpAPIView(APIView):
    @swagger_auto_schema(
        request_body=CheckOtpSerializer,
        responses={
            201: "User verify successfully",
            400: "Code is incorrect please check again",
        },
    )
    def post(self, request):
        logger.info("Check otp view")
        serializer = CheckOtpSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            otp = serializer.validated_data["otp"]
            user = CustomUser.objects.filter(otp=otp, is_verify=False).first()
            if user:
                if (
                    user.otp_expiration
                    and (timezone.now() - user.otp_expiration).total_seconds <= 180
                ):
                    return check_and_activate(user, otp)
                else:
                    return Response(
                        {"error": "Code has expired. Please request a new one."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                return Response(
                    {"error": f"User with OTP {otp} not found"},
                    status=status.HTTP_400_BAD_REQUEST,
                )


class ResentOtpAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Resent otp code if code incorrect or code expiration.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["user_id"],
            properties={"user_id": openapi.Schema(type=openapi.TYPE_STRING)},
        ),
        responses={
            status.HTTP_200_OK: "Code resent successfully.",
            status.HTTP_404_NOT_FOUND: "User not found.",
        },
    )
    def post(self, request):
        logger.info("Resent otp view")
        user_id = request.data.get("user_id")
        try:
            user = CustomUser.objects.get(id=user_id)
            send_otp_code.delay(user.id)
            return Response(
                {"message": "Code resent successfully"}, status=status.HTTP_200_OK
            )
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )


class ClientLoginAPIView(APIView):
    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={201: "Successfully", 400: "Bad request"},
    )
    def post(self, request):
        logger.info("Client login view")
        email = request.data.get("email")
        try:
            user = CustomUser.objects.get(email=email)
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "message": f"Glad to see you {user.full_name}, here is your token",
                    "tokens": {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                },
                status=status.HTTP_200_OK,
            )
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "email is not found"}, status=status.HTTP_400_BAD_REQUEST
            )


class LogoutAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Logout the user by invalidating the provided token.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["token"],
            properties={
                "token": openapi.Schema(
                    type=openapi.TYPE_STRING, description="JWT token to invalidate"
                )
            },
        ),
        responses={
            status.HTTP_200_OK: "User logged out successfully.",
            status.HTTP_400_BAD_REQUEST: "Token is required to log out.",
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Failed to log out user.",
        },
    )
    def post(self, request):
        logger.info("Logout views")
        token = request.data.get("token")
        if token:
            try:
                refresh_token = RefreshToken(token)
                refresh_token.blacklist()
                return Response(
                    {"Success": "User logged out successfully."},
                    status=status.HTTP_200_OK,
                )
            except Exception as e:
                return Response(
                    {"error": f"Failed to log out user {str(e)}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"error": "Token is required to log out"},
                status=status.HTTP_400_BAD_REQUEST,
            )
