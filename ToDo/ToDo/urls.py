from django.contrib import admin
from django.urls import include, path
from ToDoApp import views
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from profiles import views as views_profile
from profiles.views import PasswordResetView
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r"categorys", views.CategoryViewSet)
router.register(r"task", views.TaskViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("ToDoApp/", include("ToDoApp.urls")),
    path("token/", obtain_auth_token),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("tokenjwt/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("tokenjwt/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("admin/", admin.site.urls),
    path(
        "users-create/",
        views_profile.ProfileCreationView.as_view(),
        name="profile-create",
    ),
    path(
        "users-list/", views_profile.ProfileDetailView.as_view(), name="profile-detail"
    ),
    path(
        "users-update/id/<int:pk>/",
        views_profile.ProfileUpdateView.as_view(),
        name="profile-update",
    ),
    path(
        "users-update/username/<str:username>/",
        views_profile.ProfileUpdateView.as_view(),
        name="profile-update",
    ),
    path("password-reset/", PasswordResetView.as_view(), name="password-reset"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
