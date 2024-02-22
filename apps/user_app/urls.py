from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.ClientRegisterAPIView.as_view(), name="client_register"),
    path("otp_checker/", views.CheckOtpAPIView.as_view(), name="otp_checker"),
    path("client_login/", views.ClientLoginAPIView.as_view(), name="client_login"),
    path("logout/", views.LogoutAPIView.as_view(), name="logout"),
    path("resent_otp/", views.ResentOtpAPIView.as_view(), name="resent_otp"),
]
