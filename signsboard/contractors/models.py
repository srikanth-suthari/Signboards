from django.db import models
from django.contrib.auth.models import User

class ContractorCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Contractor Categories"

class Contractor(models.Model):
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    category = models.ForeignKey(ContractorCategory, on_delete=models.CASCADE)
    description = models.TextField()
    experience_years = models.PositiveIntegerField()
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    profile_image = models.ImageField(upload_to='contractors/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    rating = models.PositiveIntegerField(choices=RATING_CHOICES, default=5)
    total_projects = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.category.name}"

    class Meta:
        ordering = ['-rating', '-total_projects']

class ContractorBooking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE)
    project_title = models.CharField(max_length=200)
    project_description = models.TextField()
    estimated_duration = models.CharField(max_length=100)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    contact_phone = models.CharField(max_length=15)
    project_address = models.TextField()
    preferred_start_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.project_title} - {self.contractor.name}"

    class Meta:
        ordering = ['-created_at']

class ContractorReview(models.Model):
    booking = models.OneToOneField(ContractorBooking, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=Contractor.RATING_CHOICES)
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.booking.contractor.name} - {self.rating} stars"
