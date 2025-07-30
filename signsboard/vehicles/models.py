from django.db import models
from django.contrib.auth.models import User

class VehicleType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    capacity = models.CharField(max_length=100)  # e.g., "5 passengers", "2 tons cargo"
    base_rate_per_hour = models.DecimalField(max_digits=8, decimal_places=2)
    base_rate_per_km = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='vehicles/types/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Vehicle(models.Model):
    FUEL_CHOICES = [
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('cng', 'CNG'),
        ('electric', 'Electric'),
        ('hybrid', 'Hybrid'),
    ]
    
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE)
    make_model = models.CharField(max_length=200)  # e.g., "Maruti Suzuki Swift"
    year = models.PositiveIntegerField()
    license_plate = models.CharField(max_length=20, unique=True)
    fuel_type = models.CharField(max_length=10, choices=FUEL_CHOICES)
    seating_capacity = models.PositiveIntegerField()
    ac_available = models.BooleanField(default=True)
    gps_enabled = models.BooleanField(default=True)
    insurance_valid_until = models.DateField()
    pollution_certificate_valid_until = models.DateField()
    is_available = models.BooleanField(default=True)
    current_location = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='vehicles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.make_model} - {self.license_plate}"

class Driver(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    license_number = models.CharField(max_length=50)
    license_expiry = models.DateField()
    experience_years = models.PositiveIntegerField()
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.00)
    is_available = models.BooleanField(default=True)
    profile_image = models.ImageField(upload_to='drivers/', blank=True, null=True)
    languages_spoken = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.license_number}"

class VehicleBooking(models.Model):
    BOOKING_TYPE_CHOICES = [
        ('hourly', 'Hourly Rental'),
        ('daily', 'Daily Rental'),
        ('one_way', 'One Way Trip'),
        ('round_trip', 'Round Trip'),
        ('airport_transfer', 'Airport Transfer'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('assigned', 'Driver Assigned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    booking_number = models.CharField(max_length=20, unique=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, blank=True, null=True)
    
    # Booking details
    booking_type = models.CharField(max_length=20, choices=BOOKING_TYPE_CHOICES)
    pickup_location = models.TextField()
    pickup_date = models.DateField()
    pickup_time = models.TimeField()
    dropoff_location = models.TextField(blank=True)
    return_date = models.DateField(blank=True, null=True)
    return_time = models.TimeField(blank=True, null=True)
    
    # Contact information
    contact_phone = models.CharField(max_length=15)
    passenger_count = models.PositiveIntegerField()
    special_requirements = models.TextField(blank=True)
    
    # Pricing
    estimated_distance_km = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    estimated_duration_hours = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    base_fare = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    distance_fare = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    time_fare = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    additional_charges = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total_fare = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Trip tracking
    actual_start_time = models.DateTimeField(blank=True, null=True)
    actual_end_time = models.DateTimeField(blank=True, null=True)
    actual_distance_km = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Booking #{self.booking_number} - {self.customer.username}"

    def calculate_fare(self):
        vehicle_type = self.vehicle.vehicle_type
        
        if self.booking_type == 'hourly':
            self.time_fare = self.estimated_duration_hours * vehicle_type.base_rate_per_hour
        
        self.distance_fare = self.estimated_distance_km * vehicle_type.base_rate_per_km
        self.base_fare = 100  # Base booking fee
        
        # Additional charges for airport transfers
        if self.booking_type == 'airport_transfer':
            self.additional_charges = 200
        
        self.total_fare = self.base_fare + self.distance_fare + self.time_fare + self.additional_charges
        return self.total_fare

    class Meta:
        ordering = ['-created_at']

class VehicleReview(models.Model):
    booking = models.OneToOneField(VehicleBooking, on_delete=models.CASCADE)
    vehicle_rating = models.PositiveIntegerField(choices=[(i, f"{i} Star{'s' if i > 1 else ''}") for i in range(1, 6)])
    driver_rating = models.PositiveIntegerField(choices=[(i, f"{i} Star{'s' if i > 1 else ''}") for i in range(1, 6)])
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.booking.booking_number}"
