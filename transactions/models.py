from django.db import models
from django.contrib.auth.models import User


class Transaction(models.Model):
    CATEGORY_CHOICES = [
        ('FOOD', 'Food'),
        ('RENT', 'Rent'),
        ('UTIL', 'Utilities'),
        ('TRAN', 'Transportation'),
        ('ENTR', 'Entertainment'),
        ('HEAL', 'Health'),
        ('MISC', 'Miscellaneous'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.description} - ${self.amount}"
