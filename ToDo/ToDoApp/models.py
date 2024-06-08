from django.db import models
from django.conf import settings
from django.utils import timezone


class Category(models.Model):
    category_name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        limit_choices_to={"is_superuser": False},
        related_name="categories",
        null=True,
    )

    def __str__(self):
        return self.category_name


"""
class User(models.Model):
    user_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    password = models.CharField(max_length=255, default="")

    def __str__(self):
        return self.user_name
"""


class Task(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tasks"
    )
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, null=True, blank=True
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    fecha_inicio = models.DateTimeField()
    fecha_final = models.DateTimeField()
    completed = models.BooleanField(default=False)
    priority = models.IntegerField(default=1)

    def __str__(self):
        return self.name

    def fechas_vencidas(self):
        return self.fecha_final > timezone.now().date()
