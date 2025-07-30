from django.contrib import admin
from .models import ContractorCategory, Contractor, ContractorBooking, ContractorReview

@admin.register(ContractorCategory)
class ContractorCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']

@admin.register(Contractor)
class ContractorAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'hourly_rate', 'rating', 'is_verified', 'is_available']
    list_filter = ['category', 'is_verified', 'is_available', 'rating']
    search_fields = ['name', 'email', 'phone']
    list_editable = ['is_verified', 'is_available']

@admin.register(ContractorBooking)
class ContractorBookingAdmin(admin.ModelAdmin):
    list_display = ['project_title', 'contractor', 'customer', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['project_title', 'contractor__name', 'customer__username']

@admin.register(ContractorReview)
class ContractorReviewAdmin(admin.ModelAdmin):
    list_display = ['booking', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
