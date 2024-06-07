from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Profile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import random
import string


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        return token


class PasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField()

    def set_new_password(self):
        new_password = "".join(
            random.choices(string.ascii_letters + string.digits, k=8)
        )
        self.validated_data["new_password"] = new_password
        return new_password


class ProfileCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["username", "password", "email", "bio", "profile_picture"]

    def validate_email(self, value):
        existing_email = Profile.objects.filter(email=value).exists()
        if existing_email:
            raise serializers.ValidationError(
                "Ya existe un usuario con este correo electrónico."
            )
        return value

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data.get("password"))
        user = super(ProfileCreationSerializer, self).create(validated_data)
        if user:
            return {"success": True, "message": "Usuario registrado exitosamente"}
        else:
            return {"success": False, "message": "Error al registrar usuario"}


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "username", "email", "bio", "profile_picture"]
        read_only_fields = ["id"]

    username = serializers.CharField(read_only=True)

    def update(self, instance, validated_data):
        # Actualiza los campos solo si se proporciona un nuevo valor que no esté vacío
        for attr, value in validated_data.items():
            if value is not None and value != "":
                setattr(instance, attr, value)

        # Guarda el objeto actualizado
        instance.save()
        return instance
