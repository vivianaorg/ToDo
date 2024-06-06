from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

app_name = "task"

urlpatterns = [
    #path('task/', views.ToDoApp_list),
    #path('task/<int:pk>/', views.ToDoApp_detail),
]