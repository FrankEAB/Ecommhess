import stripe
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from orders.models import Order, OrderItem
from cart.services import get_cart, clear_cart

stripe.api_key = settings.STRIPE_SECRET_KEY


# ✅ CREATE PAYMENT INTENT
def create_payment_intent(amount, user_id):
    return stripe.PaymentIntent.create(
        amount=int(amount * 100),  # convert to cents
        currency="usd",
        metadata={"user_id": str(user_id)},  # store as string (Stripe standard)
    )


# ✅ CHECKOUT VIEW
class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart = get_cart(request.user.id)

        if not cart:
            return Response(
                {"error": "Cart is empty"},
                status=status.HTTP_400_BAD_REQUEST
            )

        total = sum(
            item["price"] * item["quantity"]
            for item in cart.values()
        )

        intent = create_payment_intent(total, request.user.id)

        return Response({
            "client_secret": intent["client_secret"]
        })


# ✅ STRIPE WEBHOOK
class StripeWebhookView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        payload = request.body
        sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

        try:
            event = stripe.Webhook.construct_event(
                payload,
                sig_header,
                settings.STRIPE_WEBHOOK_SECRET
            )
        except (ValueError, stripe.error.SignatureVerificationError):
            return Response(
                {"error": "Invalid webhook"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if event.get("type") == "payment_intent.succeeded":

            intent = event["data"]["object"]

            user_id = intent.get("metadata", {}).get("user_id")
            payment_intent_id = intent.get("id")

            if not user_id:
                return Response(
                    {"error": "Missing user_id in metadata"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user_id = int(user_id)

            # 🔒 Prevent duplicate orders
            if Order.objects.filter(
                    stripe_payment_intent=payment_intent_id
            ).exists():
                return Response({"status": "Already processed"})

            cart = get_cart(user_id)

            if not cart:
                return Response(
                    {"error": "Cart empty"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            total_amount = sum(
                item["price"] * item["quantity"]
                for item in cart.values()
            )

            order = Order.objects.create(
                user_id=user_id,
                total_amount=total_amount,
                status="paid",
                stripe_payment_intent=payment_intent_id
            )

            for product_id, item in cart.items():
                OrderItem.objects.create(
                    order=order,
                    product_id=int(product_id),
                    quantity=item["quantity"],
                    price=item["price"]
                )

            clear_cart(user_id)

        return Response({"status": "success"})