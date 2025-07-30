from django.db import models
from django.contrib.auth.models import User

class SignboardType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    material = models.CharField(max_length=100)  # ACP, Acrylic, etc.
    price_per_sqft = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='signboards/types/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.material}"

class SignboardSize(models.Model):
    name = models.CharField(max_length=50)  # e.g., "2x3 feet", "4x6 feet"
    width_feet = models.DecimalField(max_digits=5, decimal_places=2)
    height_feet = models.DecimalField(max_digits=5, decimal_places=2)
    area_sqft = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.area_sqft = self.width_feet * self.height_feet
        super().save(*args, **kwargs)

class SignboardFinish(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    additional_cost_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return self.name

class SignboardOrder(models.Model):
    STATUS_CHOICES = [
        ('quote_requested', 'Quote Requested'),
        ('quote_sent', 'Quote Sent'),
        ('approved', 'Approved'),
        ('in_production', 'In Production'),
        ('ready_for_installation', 'Ready for Installation'),
        ('installing', 'Installing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    URGENCY_CHOICES = [
        ('standard', 'Standard (7-10 days)'),
        ('urgent', 'Urgent (3-5 days)'),
        ('express', 'Express (1-2 days)'),
    ]
    
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=20, unique=True)
    business_name = models.CharField(max_length=200)
    signboard_type = models.ForeignKey(SignboardType, on_delete=models.CASCADE)
    size = models.ForeignKey(SignboardSize, on_delete=models.CASCADE)
    finish = models.ForeignKey(SignboardFinish, on_delete=models.CASCADE, blank=True, null=True)
    
    # Design details
    text_content = models.TextField()
    font_preferences = models.CharField(max_length=200, blank=True)
    color_preferences = models.CharField(max_length=200, blank=True)
    logo_upload = models.ImageField(upload_to='signboards/logos/', blank=True, null=True)
    design_file = models.FileField(upload_to='signboards/designs/', blank=True, null=True)
    special_requirements = models.TextField(blank=True)
    
    # Installation details
    installation_required = models.BooleanField(default=True)
    installation_address = models.TextField()
    contact_phone = models.CharField(max_length=15)
    preferred_installation_date = models.DateField(blank=True, null=True)
    
    # Pricing and status
    base_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    installation_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    urgency = models.CharField(max_length=20, choices=URGENCY_CHOICES, default='standard')
    urgency_charges = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='quote_requested')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.order_number} - {self.business_name}"

    def calculate_total_cost(self):
        base_cost = self.signboard_type.price_per_sqft * self.size.area_sqft
        
        if self.finish:
            finish_cost = base_cost * (self.finish.additional_cost_percentage / 100)
            base_cost += finish_cost
        
        # Urgency charges
        urgency_multiplier = {
            'standard': 0,
            'urgent': 0.25,  # 25% extra
            'express': 0.50  # 50% extra
        }
        self.urgency_charges = base_cost * urgency_multiplier.get(self.urgency, 0)
        
        self.base_price = base_cost
        self.total_cost = self.base_price + self.installation_cost + self.urgency_charges
        return self.total_cost

    class Meta:
        ordering = ['-created_at']

class SignboardGallery(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='signboards/gallery/')
    signboard_type = models.ForeignKey(SignboardType, on_delete=models.CASCADE)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Signboard Gallery"
        ordering = ['-is_featured', '-created_at']
