from django.db import models
from django.conf import settings  # Import settings
# from django.contrib.auth.models import User  # No longer needed

class StudyGroup(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="created_study_groups")
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="study_groups")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_member_count(self):
        return self.members.count()
