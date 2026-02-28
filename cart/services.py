import redis
import json
from django.conf import settings

redis_client = redis.Redis.from_url(settings.CELERY_BROKER_URL)

def get_cart(user_id):
    cart = redis_client.get(f"cart:{user_id}")
    return json.loads(cart) if cart else {}

def save_cart(user_id, cart_data):
    redis_client.set(f"cart:{user_id}", json.dumps(cart_data))

def clear_cart(user_id):
    redis_client.delete(f"cart:{user_id}")