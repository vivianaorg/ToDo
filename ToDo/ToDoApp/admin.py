from django.contrib import admin

from .models import Task, Category

admin.site.register(Task)
admin.site.register(Category)
# admin.site.register(User)


class TaskAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "description", "priority", "user", "completed"]
    search_fields = ["name"]
