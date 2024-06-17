from django.contrib.auth import get_user_model
from ToDoApp.models import Category, Task
from datetime import datetime
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.urls import reverse

class TaskTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(
            username="prueba", email="prueba@gmail.com", password="1234"
        )
        cls.token, created = Token.objects.get_or_create(user=cls.user)

        cls.category = Category.objects.create(
            category_name="General", description="Tareas generales", user=cls.user
        )
        # Use timezone.now() to get the current time with timezone information
        now = timezone.now()
        cls.task = Task.objects.create(
            name="prueba",
            description="prueba",
            fecha_inicio=now,
            fecha_final=now,
            completed=False,
            priority=1,
            category=cls.category,
            user=cls.user,
        )

    def setUp(self):
        self.client.force_authenticate(user=self.user, token=self.token)

    def test_get_task_list(self):
        url = reverse("task-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")), 1)

    def test_get_task_detail(self):
        url = reverse("task-detail", kwargs={"pk": self.task.id})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("name"), self.task.name)
