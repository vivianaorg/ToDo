from django.contrib import admin
from .models import Profile
#pq

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "first_name",
        "last_name",
        "username",
        "email",
        "is_superuser",
    ]
    search_fields = ["username"]
