from django.db import models
from django.contrib.auth import get_user_model
from djongo import models as djongo_models

User = get_user_model()


class ActivityType(models.Model):
    """Types of activities available in the system"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    points_per_minute = models.FloatField(default=1.0)
    category = models.CharField(
        max_length=50,
        choices=[
            ('cardio', 'Cardio'),
            ('strength', 'Strength Training'),
            ('flexibility', 'Flexibility'),
            ('sports', 'Sports'),
            ('other', 'Other'),
        ],
        default='other'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class Activity(djongo_models.Model):
    """Individual activity log entries"""
    _id = djongo_models.ObjectIdField()
    user_id = models.IntegerField()
    activity_type_id = models.IntegerField()
    duration_minutes = models.IntegerField()
    intensity = models.CharField(
        max_length=20,
        choices=[
            ('low', 'Low'),
            ('moderate', 'Moderate'),
            ('high', 'High'),
            ('very_high', 'Very High'),
        ],
        default='moderate'
    )
    calories_burned = models.IntegerField(null=True, blank=True)
    notes = models.TextField(blank=True)
    date_logged = models.DateTimeField()
    points_earned = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = False
        
    def __str__(self):
        return f"Activity {self._id} - User {self.user_id}"


class WorkoutSuggestion(djongo_models.Model):
    """Personalized workout suggestions"""
    _id = djongo_models.ObjectIdField()
    user_id = models.IntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    difficulty_level = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
        ]
    )
    estimated_duration = models.IntegerField(help_text="Duration in minutes")
    exercises = djongo_models.JSONField(default=list)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = False
        
    def __str__(self):
        return f"{self.title} for user {self.user_id}"
