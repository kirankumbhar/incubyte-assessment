from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
 
 
class Employee(models.Model):
    full_name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    salary = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    class Meta:
        ordering = ["id"]
 
    def __str__(self):
        return f"{self.full_name} — {self.job_title} ({self.country})"
