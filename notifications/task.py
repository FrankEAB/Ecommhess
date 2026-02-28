from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_order_confirmation(email):
    send_mail(
        "Order Confirmation",
        "Your order has been placed successfully!",
        "store@example.com",
        [email],
    )