from django.db import models
from django.contrib.auth.models import User
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

    def __str__(self):
        return self.user.username

# This is the income data field which will be stored in the database for each user
class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - $ {self.amount}"