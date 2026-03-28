from django.contrib import admin

from .models import BuyerDemand, ChatMessage, Order, Product, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "role", "phone_number", "location_name", "is_phone_verified", "created_at")
    search_fields = ("full_name", "phone_number", "email", "location_name")
    list_filter = ("role", "is_phone_verified", "farmer_type")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("crop_name", "farmer", "price", "quantity_available", "unit", "status", "updated_at")
    search_fields = ("crop_name", "farmer__full_name")
    list_filter = ("status", "unit")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("buyer_name", "farmer", "product", "quantity", "status", "total_amount", "delivery_mode")
    search_fields = ("buyer_name", "farmer__full_name", "product__crop_name")
    list_filter = ("status", "delivery_mode")


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("buyer_name", "farmer", "is_unread", "created_at")
    search_fields = ("buyer_name", "farmer__full_name", "message")
    list_filter = ("is_unread",)


@admin.register(BuyerDemand)
class BuyerDemandAdmin(admin.ModelAdmin):
    list_display = ("crop_name", "farmer", "quantity_needed", "distance_km", "created_at")
    search_fields = ("crop_name", "farmer__full_name")
