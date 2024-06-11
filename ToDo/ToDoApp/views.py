from .models import Task, Category
from rest_framework import permissions, viewsets
from rest_framework.filters import OrderingFilter
from .serializers import (
    CompletedTaskSerializer,
    PendingTaskSerializer,
    TaskSerializer,
    CategorySerializer,
)
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.decorators import action


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by("category_name")
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return user.categories.all()


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ["priority"]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.tasks.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["user"] = self.request.user
        return context

    @action(detail=False, methods=["get"])
    def completed(self, request):
        completed_tasks = self.get_queryset().filter(completed=True)
        serializer = CompletedTaskSerializer(
            completed_tasks, many=True, context={"request": request}
        )
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def pending(self, request):
        pending_tasks = self.get_queryset().filter(completed=False)
        serializer = PendingTaskSerializer(
            pending_tasks, many=True, context={"request": request}
        )
        return Response(serializer.data)


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.pk, "email": user.email})


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
