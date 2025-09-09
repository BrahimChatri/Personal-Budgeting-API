from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model extending Django's AbstractUser"""
    
    # Additional fields can be added here if needed
    # For now, we'll use the default Django User fields
    
    class Meta:
        db_table = 'users_user'
    
    def __str__(self):
        return self.username
