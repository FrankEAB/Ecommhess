from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom user model with optional vendor flag.
    """
    is_vendor = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    # No direct 'address' field here to avoid reverse clash

    def __str__(self):
        return self.username


class Address(models.Model):
    """
    Address linked to a user. One user can have multiple addresses.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='addresses'  # Avoids reverse name clash with User fields
    )
    line1 = models.CharField(max_length=255)
    line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.line1}, {self.city}"


class Profile(models.Model):
    """
    Optional extended profile for the user.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'  # Safe one-to-one relation
    )
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s profile"