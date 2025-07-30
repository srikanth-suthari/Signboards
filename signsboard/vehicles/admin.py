from django.contrib import admin
from .models import VehicleType, Vehicle, Driver, VehicleBooking, VehicleReview

@admin.register(VehicleType)
class VehicleTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'capacity', 'base_rate_per_hour', 'base_rate_per_km']
    search_fields = ['name']

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['make_model', 'license_plate', 'vehicle_type', 'fuel_type', 'is_available']
    list_filter = ['vehicle_type', 'fuel_type', 'is_available', 'ac_available']
    search_fields = ['make_model', 'license_plate']
    list_editable = ['is_available']

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'license_number', 'rating', 'is_available']
    list_filter = ['is_available', 'rating']
    search_fields = ['name', 'phone', 'license_number']
    list_editable = ['is_available']

@admin.register(VehicleBooking)
class VehicleBookingAdmin(admin.ModelAdmin):
    list_display = ['booking_number', 'customer', 'vehicle', 'driver', 'booking_type', 'status', 'total_fare']
    list_filter = ['booking_type', 'status', 'pickup_date']
    search_fields = ['booking_number', 'customer__username']
    readonly_fields = ['booking_number', 'base_fare', 'distance_fare', 'time_fare', 'total_fare']

@admin.register(VehicleReview)
class VehicleReviewAdmin(admin.ModelAdmin):
    list_display = ['booking', 'vehicle_rating', 'driver_rating', 'created_at']
    list_filter = ['vehicle_rating', 'driver_rating']
