from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class GraphGenerationLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    graph_type = models.CharField(max_length=100)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.user.username} generated {self.graph_type} at {self.timestamp}"
