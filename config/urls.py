from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),

    # Authentication (Register, Login, Profile, JWT)
    path("api/accounts/", include("accounts.urls")),

    # JWT Auth
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Products
    path("api/products/", include("products.urls")),

    # Cart
    path("api/cart/", include("cart.urls")),

    # Orders (includes checkout)
    path("api/orders/", include("orders.urls")),

    # Payments
    path("api/payments/", include("payments.urls")),
]