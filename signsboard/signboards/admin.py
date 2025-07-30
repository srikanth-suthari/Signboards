from django.contrib import admin
from .models import SignboardType, SignboardSize, SignboardFinish, SignboardOrder, SignboardGallery

@admin.register(SignboardType)
class SignboardTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'material', 'price_per_sqft', 'created_at']
    list_filter = ['material']
    search_fields = ['name', 'material']

@admin.register(SignboardSize)
class SignboardSizeAdmin(admin.ModelAdmin):
    list_display = ['name', 'width_feet', 'height_feet', 'area_sqft']
    search_fields = ['name']

@admin.register(SignboardFinish)
class SignboardFinishAdmin(admin.ModelAdmin):
    list_display = ['name', 'additional_cost_percentage']
    search_fields = ['name']

@admin.register(SignboardOrder)
class SignboardOrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'business_name', 'signboard_type', 'status', 'total_cost', 'created_at']
    list_filter = ['status', 'urgency', 'installation_required', 'created_at']
    search_fields = ['order_number', 'business_name', 'customer__username']
    readonly_fields = ['order_number', 'base_price', 'urgency_charges', 'total_cost']

@admin.register(SignboardGallery)
class SignboardGalleryAdmin(admin.ModelAdmin):
    list_display = ['title', 'signboard_type', 'is_featured', 'created_at']
    list_filter = ['signboard_type', 'is_featured']
    search_fields = ['title']
    list_editable = ['is_featured']
