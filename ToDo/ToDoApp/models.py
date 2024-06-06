from time import timezone
from django.db import models
from django.conf import settings


class Category(models.Model):
    category_name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        limit_choices_to={"is_superuser": False},
        related_name="categorys",
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
    name = models.CharField(max_length=200)
    description = models.TextField()
    fecha_inicio = models.DateField("Fecha de inicio")
    fecha_final = models.DateField("Fecha de vencimiento")
    completed = models.BooleanField(default=False)
    priority = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        limit_choices_to={"is_superuser": False},
        related_name="tasks",
        null=True,
    )

    def __str__(self):
        return self.name

    def fechas_vencidas(self):
        return self.fecha_final > timezone.now()
