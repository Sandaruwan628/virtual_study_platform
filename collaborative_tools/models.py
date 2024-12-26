from django.db import models
from django.conf import settings

class Whiteboard(models.Model):
    name = models.CharField(max_length=200, unique=True, null=True)  # Allow null temporarily
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
