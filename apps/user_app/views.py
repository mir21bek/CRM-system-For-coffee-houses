from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from .serializers import CustomRegisterSerializer
from rest_framework.response import Response
from rest_framework import status
from .tasks import user_created


class ClientRegisterAPIView(APIView):
    @swagger_auto_schema(
        request_body=CustomRegisterSerializer,
        responses={201: "User registered successfully", 400: "Bad request"},
    )
    def post(self, request):
        serializer = CustomRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            user_created.delay(user.id)
            return Response(
                {"massage": "User registered successfully", "user email": user.email},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
