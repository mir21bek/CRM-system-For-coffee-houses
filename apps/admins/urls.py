from django.urls import path
from . import views

urlpatterns = [
    path(
        "employee_create/",
        views.EmployeeCreateAPIView.as_view(),
        name="employee create",
    ),
    path(
        "branches_create/", views.BranchCreateAPIView.as_view(), name="branches create"
    ),
    path("menu_list/", views.MenuAPIView.as_view()),
]
