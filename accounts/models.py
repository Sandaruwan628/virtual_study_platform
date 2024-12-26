from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    STUDENT = 'ST'
    MENTOR = 'MN'
    INSTRUCTOR = 'IN'
    ADMINISTRATOR = 'AD'

    USER_TYPE_CHOICES = [
        (STUDENT, 'Student'),
        (MENTOR, 'Mentor'),
        (INSTRUCTOR, 'Instructor'),
    ]

    user_type = models.CharField(
        max_length=2,
        choices=USER_TYPE_CHOICES,
        default=STUDENT,
    )

    def __str__(self):
        return self.username
