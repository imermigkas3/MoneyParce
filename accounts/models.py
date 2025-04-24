from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    STATUS_CHOICES = [
        ('student', 'Student'),
        ('full_time', 'Full-Time'),
        ('part_time', 'Part-Time'),
        ('unemployed', 'Unemployed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=True)
    phone_regex = RegexValidator(
        regex=r'^\d{10}$',
        message="Phone number must be entered in the format: '0000000000' (10 digits)."
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=10,
        blank=True,
        null=True,
    )
    access_token = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.username

# This is the income data field which will be stored in the database for each user
class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - $ {self.amount}"