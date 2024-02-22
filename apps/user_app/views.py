from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from .serializers import CustomRegisterSerializer
from rest_framework.response import Response
from rest_framework import status
from apps.user_app.tasks import send_otp_code
import logging

logger = logging.getLogger("main")


class ClientRegisterAPIView(APIView):
    @swagger_auto_schema(
        request_body=CustomRegisterSerializer,
        responses={201: "Code send successfully", 400: "Bad request"},
    )
    def post(self, request):
        logger.info("client register class")
        serializer = CustomRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            send_otp_code.delay(user.id)
            return Response(
                {"massage": "Code send successfully", "user email": user.email},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
