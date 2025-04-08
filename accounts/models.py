from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# Since we want to store more information with each user, we need to use more than Django's built-in
# user class, so this model will allow us to store income
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    income = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.user.username}'s Profile"

# This is the income data field which will be stored in the database for each user
class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - $ {self.amount}"