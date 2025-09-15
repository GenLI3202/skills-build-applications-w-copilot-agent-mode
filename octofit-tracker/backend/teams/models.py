from django.db import models
from django.contrib.auth import get_user_model
from djongo import models as djongo_models

User = get_user_model()


class Team(djongo_models.Model):
    """Teams for group challenges and competitions"""
    _id = djongo_models.ObjectIdField()
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    captain_id = models.IntegerField()
    max_members = models.IntegerField(default=10)
    is_public = models.BooleanField(default=True)
    team_code = models.CharField(max_length=8, unique=True)
    total_points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = False
        
    def __str__(self):
        return self.name


class TeamMembership(djongo_models.Model):
    """Team membership tracking"""
    _id = djongo_models.ObjectIdField(primary_key=True)
    team_id = models.CharField(max_length=24)
    user_id = models.IntegerField()
    role = models.CharField(
        max_length=20,
        choices=[
            ('captain', 'Captain'),
            ('member', 'Member'),
        ],
        default='member'
    )
    joined_at = models.DateTimeField(auto_now_add=True)
    points_contributed = models.IntegerField(default=0)
    
    class Meta:
        abstract = False
        
    def __str__(self):
        return f"User {self.user_id} in team {self.team_id}"


class Challenge(djongo_models.Model):
    """Team challenges and competitions"""
    _id = djongo_models.ObjectIdField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    challenge_type = models.CharField(
        max_length=50,
        choices=[
            ('steps', 'Step Challenge'),
            ('duration', 'Duration Challenge'),
            ('points', 'Points Challenge'),
            ('custom', 'Custom Challenge'),
        ]
    )
    target_value = models.IntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    participating_teams = djongo_models.JSONField(default=list)
    rewards = djongo_models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = False
        
    def __str__(self):
        return self.title
