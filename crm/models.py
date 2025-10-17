# crm/models.py (Snippet - Focus on Customer Model)

# ... (above imports and validate_phone_format function) ...

# --- Customer Model ---
class Customer(models.Model):
    # FIX 1: max_length must be 100
    name = models.CharField(max_length=100) 
    
    # Check 2: email: models.EmailField()
    email = models.EmailField(unique=True) 
    
    # FIX 3: max_length must be 15 (and keep the custom validator)
    phone = models.CharField(max_length=15, blank=True, null=True, validators=[validate_phone_format])
    
    created_at = models.DateTimeField(default=timezone.now)

    # Check 4: def __str__ method exists and returns self.name
    def __str__(self):
        return self.name

# ... (rest of the models: Product, Order) ...
