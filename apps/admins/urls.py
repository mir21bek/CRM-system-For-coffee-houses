from django.urls import path
from . import views

urlpatterns = [
    path(
        "employee_create/",
        views.EmployeeCreateAPIView.as_view(),
        name="employee create",
    ),
]
