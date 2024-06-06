from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Task, Category

"""
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'password']
"""


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "category_name",
            "description",
        )

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.none(), allow_null=True, required=False
    )

    class Meta:
        model = Task
        fields = (
            "id",
            "category",
            "name",
            "description",
            "fecha_inicio",
            "fecha_final",
            "completed",
            "priority",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context.get("user")
        if user:
            self.fields["category"].queryset = Category.objects.filter(user=user)

    def validate(self, data):
        user = self.context["request"].user
        fecha_inicio = data.get("fecha_inicio")
        fecha_final = data.get("fecha_final")
        overlapping_tasks = Task.objects.filter(
            user=user, fecha_inicio__lt=fecha_final, fecha_final__gt=fecha_inicio
        ).exists()

        if overlapping_tasks:
            raise serializers.ValidationError(
                "La fecha de esta tarea se cruzan con otra tarea existente."
            )

        return data

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.completed = validated_data.get("completed", instance.completed)
        instance.priority = validated_data.get("priority", instance.priority)
        instance.save()
        return instance


# personalizar aca la parte de la contraseña y todo eso
# agregar foto de perfil, cambiar contraseña, olvide la contraseña, validar correo
# validar que la hora no este ocupado, que no haya cruce de tarea
# listado de tareas pendientes, y tareas hechas
