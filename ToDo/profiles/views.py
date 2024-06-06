from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAdminUser
from django.contrib.auth import get_user_model
from .models import Profile
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import (
    ProfileCreationSerializer,
    ProfileSerializer,
    CustomTokenObtainPairSerializer,
    PasswordResetSerializer,
)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
import random
import string


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


class ProfileDetailView(generics.ListAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAdminUser]

class PasswordResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        try:
            profile = Profile.objects.get(email=email)
            serializer = PasswordResetSerializer(data=request.data)
            if serializer.is_valid():
                serializer.set_new_password()
                new_password = serializer.validated_data['new_password']
                profile.set_password(new_password)
                profile.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Profile.DoesNotExist:
            return Response({'error': 'Perfil no encontrado.'}, status=status.HTTP_404_NOT_FOUND)