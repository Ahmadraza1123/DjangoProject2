from django.db import models
from django.contrib.auth.models import User
from rest_framework.permissions import BasePermission


class UserProfile(models.Model):
    ROLE_CHOICES = (
    ('normal', 'Normal'),
    ('author', 'Author'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profile_pictures', null=True, blank=True)
    social_link = models.URLField(blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='normal')

