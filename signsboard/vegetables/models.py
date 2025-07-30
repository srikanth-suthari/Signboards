from django.db import models
from django.contrib.auth.models import User

class VegetableCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='vegetables/categories/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Vegetable Categories"

class Vegetable(models.Model):
    UNIT_CHOICES = [
        ('kg', 'Kilogram'),
        ('g', 'Gram'),
        ('piece', 'Piece'),
        ('bunch', 'Bunch'),
        ('packet', 'Packet'),
    ]
    
    name = models.CharField(max_length=100)
    category = models.ForeignKey(VegetableCategory, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    price_per_unit = models.DecimalField(max_digits=8, decimal_places=2)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default='kg')
    image = models.ImageField(upload_to='vegetables/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    is_organic = models.BooleanField(default=False)
    stock_quantity = models.PositiveIntegerField(default=0)
    nutritional_info = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - ₹{self.price_per_unit}/{self.unit}"

    class Meta:
        ordering = ['category', 'name']

class DeliverySlot(models.Model):
    slot_time = models.CharField(max_length=50)  # e.g., "9:00 AM - 12:00 PM"
    is_active = models.BooleanField(default=True)
    max_orders = models.PositiveIntegerField(default=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.slot_time

class VegetableOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=20, unique=True)
    delivery_address = models.TextField()
    delivery_phone = models.CharField(max_length=15)
    delivery_slot = models.ForeignKey(DeliverySlot, on_delete=models.CASCADE)
    delivery_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    delivery_fee = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    special_instructions = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.order_number} - {self.customer.username}"

    class Meta:
        ordering = ['-created_at']

class OrderItem(models.Model):
    order = models.ForeignKey(VegetableOrder, related_name='items', on_delete=models.CASCADE)
    vegetable = models.ForeignKey(Vegetable, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=8, decimal_places=2)
    price_per_unit = models.DecimalField(max_digits=8, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.vegetable.name} x {self.quantity}"

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.price_per_unit
        super().save(*args, **kwargs)

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart - {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    vegetable = models.ForeignKey(Vegetable, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=8, decimal_places=2, default=1)

    def __str__(self):
        return f"{self.vegetable.name} x {self.quantity}"

    @property
    def total_price(self):
        return self.quantity * self.vegetable.price_per_unit

    class Meta:
        unique_together = ['cart', 'vegetable']
