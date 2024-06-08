from rest_framework import serializers
from .models import Task, Category
from django.utils import timezone
from datetime import timedelta
import tzlocal


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

    def validate_name(self, value):
        user = self.context.get("request").user
        existing_category = Category.objects.filter(user=user, name=value).exists()
        if existing_category:
            raise serializers.ValidationError(
                "Ya existe una categoría con el mismo nombre."
            )
        return value


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

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)

    def validate_name(self, value):
        category = self.context.get("request").data.get("category")
        if category:
            try:
                category_instance = Category.objects.get(id=category)
            except Category.DoesNotExist:
                raise serializers.ValidationError(
                    "La categoría proporcionada no existe."
                )
            existing_task = Task.objects.filter(
                category=category_instance, name=value
            ).exists()
            if existing_task:
                raise serializers.ValidationError(
                    "Ya existe una tarea con el mismo nombre en esta categoría."
                )
        existing_task_null = Task.objects.filter(
            category__isnull=True, name=value
        ).exists()
        if existing_task_null:
            raise serializers.ValidationError(
                "Ya existe una tarea con el mismo nombre en esta categoría."
            )
        return value

    def validate_date_to_do(self, value):
        local_tz = tzlocal.get_localzone()
        now = timezone.now().astimezone(local_tz)
        value_with_tz = value.replace(tzinfo=local_tz)
        if value_with_tz <= now:
            raise serializers.ValidationError(
                "La fecha de realización de la tarea no puede ser anterior o igual a la fecha actual."
            )

        one_hour_before = value - timedelta(minutes=59)
        one_hour_after = value + timedelta(minutes=59)

        conflicting_tasks = Task.objects.filter(
            date_to_do__gte=one_hour_before,
            date_to_do__lte=one_hour_after,
            user=self.context["request"].user,
        )

        if conflicting_tasks.exists():
            raise serializers.ValidationError(
                "Ya existe una tarea con una fecha y hora similar. Las tareas deben tener al menos una hora de diferencia."
            )

        return value

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.fecha_inicio = validated_data.get(
            "fecha_inicio", instance.fecha_inicio
        )
        instance.fecha_final = validated_data.get("fecha_final", instance.fecha_final)
        instance.completed = validated_data.get("completed", instance.completed)
        instance.priority = validated_data.get("priority", instance.priority)
        instance.save()
        return instance
