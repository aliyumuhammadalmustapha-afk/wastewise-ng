from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Feature 1: Custom User Model with Roles
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'Regular User'),
        ('admin', 'Administrator'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    
    def __str__(self):
        return f"{self.username} ({self.role})"

# Feature 3: Scan History Database
class ScanRecord(models.Model):
    WASTE_CLASSES = (
        ('Plastic', 'Plastic'),
        ('Metal', 'Metal'),
        ('Glass', 'Glass'),
        ('Paper', 'Paper & Cardboard'),
        ('Organic', 'Organic'),
        ('E-Waste', 'E-Waste'),
        ('Textile', 'Textile'),
        ('Hazardous', 'Hazardous'),
        ('General', 'General / Residual'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='scan_records')
    image = models.ImageField(upload_to='scans/%Y/%m/%d/')
    predicted_class = models.CharField(max_length=20, choices=WASTE_CLASSES)
    confidence_score = models.FloatField() 
    specific_item = models.CharField(max_length=100, blank=True, null=True)
    specific_item_name = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    @property
    def waste_class(self):
        return self.predicted_class

    @property
    def confidence(self):
        return self.confidence_score

    @property
    def timestamp(self):
        return self.created_at

    def __str__(self):
        return f"{self.user.username} scanned {self.predicted_class}"

class Scan(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='scans')
    waste_class = models.CharField(max_length=50)
    confidence = models.FloatField()
    predicted_index = models.IntegerField()
    # Phase 1: specific item identification
    specific_item = models.CharField(max_length=100, blank=True, null=True)
    specific_item_name = models.CharField(max_length=100, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        label = self.specific_item_name or self.waste_class
        return f"{self.user} - {label} - {self.confidence}%"