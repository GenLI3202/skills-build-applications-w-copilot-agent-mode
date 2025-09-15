from django.db import models
from django.contrib.auth import get_user_model
from djongo import models as djongo_models

User = get_user_model()


class Leaderboard(djongo_models.Model):
    """Different types of leaderboards"""
    _id = djongo_models.ObjectIdField()
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    leaderboard_type = models.CharField(
        max_length=50,
        choices=[
            ('weekly', 'Weekly'),
            ('monthly', 'Monthly'),
            ('all_time', 'All Time'),
            ('challenge', 'Challenge Specific'),
        ]
    )
    category = models.CharField(
        max_length=50,
        choices=[
            ('individual', 'Individual'),
            ('team', 'Team'),
        ]
    )
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = False
        
    def __str__(self):
        return f"{self.name} - {self.leaderboard_type}"


class LeaderboardEntry(djongo_models.Model):
    """Individual entries in leaderboards"""
    _id = djongo_models.ObjectIdField()
    leaderboard_id = djongo_models.ObjectIdField()
    participant_id = models.IntegerField()  # Can be user_id or team_id
    participant_type = models.CharField(
        max_length=20,
        choices=[
            ('user', 'User'),
            ('team', 'Team'),
        ]
    )
    score = models.IntegerField()
    rank = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = False
        
    def __str__(self):
        return f"Rank {self.rank} - {self.participant_type} {self.participant_id}"


class Achievement(djongo_models.Model):
    """Achievement badges and rewards"""
    _id = djongo_models.ObjectIdField()
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon_url = models.URLField(blank=True)
    criteria = djongo_models.JSONField(default=dict)
    points_reward = models.IntegerField(default=0)
    achievement_type = models.CharField(
        max_length=50,
        choices=[
            ('milestone', 'Milestone'),
            ('consistency', 'Consistency'),
            ('challenge', 'Challenge'),
            ('social', 'Social'),
        ]
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = False
        
    def __str__(self):
        return self.name


class UserAchievement(djongo_models.Model):
    """Track user achievements"""
    _id = djongo_models.ObjectIdField()
    user_id = models.IntegerField()
    achievement_id = djongo_models.ObjectIdField()
    earned_at = models.DateTimeField(auto_now_add=True)
    progress_data = djongo_models.JSONField(default=dict)
    
    class Meta:
        abstract = False
        
    def __str__(self):
        return f"User {self.user_id} - Achievement {self.achievement_id}"
