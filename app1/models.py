from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ("farmer", "Farmer"),
        ("buyer", "Buyer"),
    ]

    FARMER_TYPE_CHOICES = [
        ("small", "Small Scale Farmer"),
        ("organic", "Organic Farmer"),
        ("dairy", "Dairy Farmer"),
        ("grain", "Grain Farmer"),
        ("vegetable", "Vegetable Farmer"),
        ("fruit", "Fruit Farmer"),
    ]
    LANGUAGE_CHOICES = [
        ("en", "English"),
        ("hi", "Hindi"),
        ("or", "Odia"),
    ]
    VERIFICATION_CHOICES = [
        ("verified", "Verified"),
        ("pending", "Pending"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    full_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(blank=True)
    location_name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    farmer_type = models.CharField(max_length=30, choices=FARMER_TYPE_CHOICES, blank=True)
    is_phone_verified = models.BooleanField(default=False)
    preferred_language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default="en")
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.8)
    bank_upi_details = models.CharField(max_length=200, blank=True)
    profile_image = models.FileField(upload_to="profiles/", blank=True)
    verification_status = models.CharField(max_length=20, choices=VERIFICATION_CHOICES, default="verified")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.get_role_display()})"


class Product(models.Model):
    STATUS_CHOICES = [
        ("available", "Available"),
        ("sold_out", "Sold Out"),
    ]

    farmer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="products")
    crop_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_available = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=20, default="kg")
    product_image = models.FileField(upload_to="products/", blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="available")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.crop_name} - {self.farmer.full_name}"


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("delivered", "Delivered"),
        ("rejected", "Rejected"),
    ]

    farmer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="orders")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders")
    buyer_name = models.CharField(max_length=150)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_mode = models.CharField(max_length=30, default="Self delivery")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["status", "-created_at"]

    def __str__(self):
        return f"{self.buyer_name} - {self.status}"


class ChatMessage(models.Model):
    farmer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="chat_messages")
    buyer_name = models.CharField(max_length=150)
    message = models.TextField()
    is_unread = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Chat with {self.buyer_name}"


class BuyerDemand(models.Model):
    farmer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="nearby_demands")
    crop_name = models.CharField(max_length=100)
    quantity_needed = models.CharField(max_length=100)
    distance_km = models.DecimalField(max_digits=5, decimal_places=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["distance_km", "-created_at"]

    def __str__(self):
        return f"{self.crop_name} demand near {self.farmer.full_name}"
