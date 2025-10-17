# crm/models.py

from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError
from decimal import Decimal
import re
from django.db.models import Sum

# --- Custom Validator ---
def validate_phone_format(value):
    """Validates phone number formats."""
    # A simple, permissive regex for demonstration:
    if not re.match(r'^(\+\d{1,3}\s?)?(\d{3}[\s.-]?\d{3}[\s.-]?\d{4}|\d{10})$', value):
        raise ValidationError(
            f"'{value}' is not a valid phone number format. Use formats like +1234567890.",
            code='invalid_phone_format'
        )
    return value

# --- Customer Model ---
class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True) 
    phone = models.CharField(max_length=20, blank=True, null=True, validators=[validate_phone_format])
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

# --- Product Model ---
class Product(models.Model):
    name = models.CharField(max_length=255)
    # Price must be positive (min value 0.01)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))]) 
    # Stock cannot be negative
    stock = models.IntegerField(default=0, validators=[MinValueValidator(0)]) 

    def __str__(self):
        return self.name

# --- Order Model ---
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    products = models.ManyToManyField(Product, related_name='orders') 
    order_date = models.DateTimeField(default=timezone.now)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) 

    def calculate_total(self):
        """Calculates total amount as the sum of associated product prices."""
        total = self.products.aggregate(Sum('price'))['price__sum']
        return total if total is not None else Decimal('0.00')

    def __str__(self):
        return f"Order {self.id} for {self.customer.name}"