from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAdminUser
from django.contrib.auth import get_user_model
from .models import Profile
from rest_framework.response import Response
from .serializers import (
    ProfileCreationSerializer,
    ProfileSerializer,
    CustomTokenObtainPairSerializer,
    PasswordResetSerializer,
    ForgotPasswordSerializerCustom,
)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.http import Http404


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class ProfileCreationView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = ProfileCreationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_data = serializer.save()

        if response_data.get("success"):
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class ProfileUpdateView(generics.UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "username"

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        # Intenta obtener el perfil por ID
        pk = self.kwargs.get("pk")
        if pk is not None:
            return get_object_or_404(queryset, pk=pk)

        # Intenta obtener el perfil por nombre de usuario
        username = self.kwargs.get("username")
        if username is not None:
            return get_object_or_404(queryset, username=username)

        # Si no se proporciona ni pk ni username, lanza un error
        raise Http404("No se proporcionó pk o username.")

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # Si 'prefetch_related' se ha aplicado al queryset, debemos
            # forzar la evaluación de los resultados para evitar errores.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class ForgotPasswordCustomView(generics.UpdateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = ForgotPasswordSerializerCustom
    permission_classes = [AllowAny]

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_data = serializer.save()

        return Response(response_data, status=status.HTTP_200_OK)


class ProfileDetailView(generics.ListAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAdminUser]


class PasswordResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        try:
            profile = Profile.objects.get(email=email)
            serializer = PasswordResetSerializer(data=request.data)
            if serializer.is_valid():
                serializer.set_new_password()
                new_password = serializer.validated_data["new_password"]
                profile.set_password(new_password)
                profile.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Profile.DoesNotExist:
            return Response(
                {"error": "Perfil no encontrado."}, status=status.HTTP_404_NOT_FOUND
            )
