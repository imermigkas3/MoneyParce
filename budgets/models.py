from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


# Create your models here.
class Budget(models.Model):
    CATEGORY_CHOICES = [
        ('FOOD', 'Food'),
        ('RENT', 'Rent'),
        ('UTIL', 'Utilities'),
        ('TRAN', 'Transportation'),
        ('ENTR', 'Entertainment'),
        ('HEAL', 'Health'),
        ('MISC', 'Miscellaneous'),
    ]

    # blank=True tells Django's validation layer (form, admin etc) that it's okay
    # for it to be blank.
    id = models.AutoField(primary_key=True)
    # foreign key relationship to the user model. Budget is associated with a person
    # on_delete=models.CASCADE specifies that if the related user is deleted,
    # the associated budget will also be deleted
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             null=True) # allow null in DB for now
    title = models.CharField(max_length=100,
                             default="Untitled",
                             help_text="A short name for this budget item")
    description = models.TextField(help_text="Optional description or notes",
                                   blank=True)
    amount = models.DecimalField(max_digits=10,
                                 decimal_places=2,
                                 default=0.00, validators=[MinValueValidator(Decimal('0.00'))],
                                 help_text="Amount in your currency (e.g. 1234.56)")
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    duration = models.CharField(max_length=50,
                                blank=True,
                                help_text="weekly, monthly, annually")
    date_created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return (f"{self.title} - {self.description} - Amount: {self.amount} - "
                f"Category: {self.category} - Duration: {self.duration} - "
                f"Created on: {self.date_created.isoformat()}")
