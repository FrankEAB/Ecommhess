from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .services import get_cart, save_cart
from products.models import Product


class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity", 1)

        if not product_id:
            return Response({"error": "product_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            quantity = int(quantity)
        except ValueError:
            return Response({"error": "quantity must be a number"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        cart = get_cart(request.user.id)

        cart[str(product_id)] = {
            "name": product.name,
            "price": float(product.price),
            "quantity": quantity,
        }

        save_cart(request.user.id, cart)

        return Response({"message": "Added to cart", "cart": cart}, status=status.HTTP_200_OK)


class ViewCartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart = get_cart(request.user.id)
        return Response({"cart": cart}, status=status.HTTP_200_OK)