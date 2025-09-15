from django.db import models
from django.contrib.auth.models import AbstractUser
from djongo import models as djongo_models


class User(AbstractUser):
    """Extended User model for OctoFit Tracker"""
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True, help_text="Height in cm")
    weight = models.FloatField(null=True, blank=True, help_text="Weight in kg")
    fitness_level = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
        ],
        default='beginner'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.username} - {self.first_name} {self.last_name}"


class UserProfile(djongo_models.Model):
    """Additional profile information stored in MongoDB"""
    _id = djongo_models.ObjectIdField()
    user_id = models.IntegerField(unique=True)
    bio = models.TextField(blank=True)
    profile_picture = models.URLField(blank=True)
    total_points = models.IntegerField(default=0)
    achievements = djongo_models.JSONField(default=list)
    preferences = djongo_models.JSONField(default=dict)
    
    class Meta:
        abstract = False
        
    def __str__(self):
        return f"Profile for user {self.user_id}"
