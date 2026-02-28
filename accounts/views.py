from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model

from .serializers import UserSerializer, RegisterSerializer

User = get_user_model()


# 🔹 Register User
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


# 🔹 Logged-in User Profile
class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


# 🔹 Admin-only User Management
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]