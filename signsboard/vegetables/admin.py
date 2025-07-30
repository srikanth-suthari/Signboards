from django.contrib import admin
from .models import VegetableCategory, Vegetable, DeliverySlot, VegetableOrder, OrderItem, Cart, CartItem

@admin.register(VegetableCategory)
class VegetableCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']

@admin.register(Vegetable)
class VegetableAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price_per_unit', 'unit', 'is_available', 'is_organic', 'stock_quantity']
    list_filter = ['category', 'is_available', 'is_organic', 'unit']
    search_fields = ['name']
    list_editable = ['price_per_unit', 'is_available', 'stock_quantity']

@admin.register(DeliverySlot)
class DeliverySlotAdmin(admin.ModelAdmin):
    list_display = ['slot_time', 'is_active', 'max_orders']
    list_editable = ['is_active', 'max_orders']

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(VegetableOrder)
class VegetableOrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'customer', 'delivery_date', 'delivery_slot', 'total_amount', 'status']
    list_filter = ['status', 'delivery_date', 'delivery_slot']
    search_fields = ['order_number', 'customer__username']
    inlines = [OrderItemInline]

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']
    inlines = [CartItemInline]
