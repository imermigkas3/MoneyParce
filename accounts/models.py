from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# This is the income data field which will be stored in the database for each user
class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - $ {self.amount}"