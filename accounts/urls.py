from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import UserViewSet, RegisterView, ProfileView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    # 🔹 JWT Authentication
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 🔹 Registration
    path('register/', RegisterView.as_view(), name='register'),

    # 🔹 Logged-in User Profile
    path('profile/', ProfileView.as_view(), name='profile'),

    # 🔹 Admin/User management (ViewSet)
    path('', include(router.urls)),
]