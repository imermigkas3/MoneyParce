from django.db import models
from django.contrib.auth.models import User
# Create your models here.


# Create your models here.
class Budget(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    cost = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.id) + ' - ' + self.name