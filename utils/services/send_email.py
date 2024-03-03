import random

from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


def generate_code_for_send_mail(length=4):
    otp = "".join(random.choice("0123456789") for _ in range(length))
    return otp


def check_and_activate(user, otp):
    if user:
        if not user.is_verify:
            user.is_verify = True
            user.otp = None
            user.save()
            refresh = RefreshToken.for_user(user)
            return Response(
                {"refresh": str(refresh), "access": str(refresh.access_token)},
                status=status.HTTP_201_CREATED,
            )
    else:
        return Response(
            {"message": "User is already verified."},
            status=status.HTTP_400_BAD_REQUEST,
        )
