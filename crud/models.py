from django.db import models

class Categories(models.Model):
    category_id = models.BigAutoField(primary_key=True)
    category_name = models.CharField(max_length=55)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class InventoryItems(models.Model):
    item_id = models.BigAutoField(primary_key=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=55)
    unit = models.CharField(max_length=55)
    current_stock = models.IntegerField(default=0)
    reorder_level = models.IntegerField(default=0)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Suppliers(models.Model):
    supplier_id = models.BigAutoField(primary_key=True)
    supplier_name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Admins(models.Model):
    admin_id = models.BigAutoField(primary_key=True, blank=False)
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    username = models.CharField(max_length=55, blank=False, unique=True)
    email = models.EmailField(max_length=55, blank=True)
    password = models.CharField(max_length=255, blank=False)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    
class AuditLogs(models.Model):
    ACTION_CHOICES = [
        ('create', 'Create'),
        ('delete', 'Delete'),
        ('updated', 'Update'),
    ]
    
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=50)
    description = models.TextField()
    performed_at = models.DateTimeField(auto_now_add=True)
    performed_by = models.ForeignKey(
        Admins,
        null=True,
        on_delete=models.SET_NULL,
        related_name='audit_logs'
    )

class PendingVerification(models.Model):
    CHANGE_TYPE_CHOICES = [
        ('email', 'Email Change'),
        ('password', 'Password Change'),
    ]
    admin = models.ForeignKey(Admins, on_delete=models.CASCADE)
    token = models.CharField(max_length=64, unique=True)
    change_type = models.CharField(max_length=20, choices=CHANGE_TYPE_CHOICES)
    new_value = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_expired(self):
        from django.utils import timezone
        return timezone.now() > self.expires_at