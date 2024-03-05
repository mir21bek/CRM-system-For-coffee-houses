from django.test import TestCase
from rest_framework.test import APIClient
from apps.user_app.models import CustomUser
from rest_framework import status


class EmployeeCreateAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_employee_as_admin(self):
        # Создаем администратора
        admin = CustomUser.objects.create_user(
            email="admin@example.com",
            full_name="Admin User",
            login="admin",
            password="adminpassword",
            role="admin",
        )
        admin.is_superuser = True
        admin.save()

        # Аутентификация администратора
        self.client.force_authenticate(user=admin)

        # Создаем данные для нового сотрудника
        employee_data = {
            "role": "barista",
            "email": "barista@example.com",
            "full_name": "Barista User",
            "date_of_birth": "1990-01-01",
            "phone_number": "+996553124323",
            "password": "baristapassword",
            "login": "barista_user",
        }

        # Отправляем POST-запрос на создание сотрудника
        response = self.client.post("/api/admins/employee_create/", employee_data)
        response_data = response.json()
        print(response_data)

        # Проверяем, что ответ имеет статус 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Проверяем, что сотрудник был создан
        self.assertTrue(
            CustomUser.objects.filter(email=employee_data["email"]).exists()
        )
