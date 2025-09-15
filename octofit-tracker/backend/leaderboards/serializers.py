from rest_framework import serializers
from .models import Leaderboard, LeaderboardEntry, Achievement, UserAchievement


class LeaderboardSerializer(serializers.ModelSerializer):
    """Serializer for Leaderboard model"""
    _id = serializers.CharField(read_only=True)
    
    class Meta:
        model = Leaderboard
        fields = ['_id', 'name', 'description', 'leaderboard_type', 'category',
                 'is_active', 'start_date', 'end_date', 'created_at']
        read_only_fields = ['_id', 'created_at']
    
    def to_representation(self, instance):
        """Convert ObjectId to string"""
        data = super().to_representation(instance)
        if data.get('_id'):
            data['_id'] = str(data['_id'])
        return data


class LeaderboardEntrySerializer(serializers.ModelSerializer):
    """Serializer for LeaderboardEntry model"""
    _id = serializers.CharField(read_only=True)
    leaderboard_id = serializers.CharField()
    participant_name = serializers.SerializerMethodField()
    
    class Meta:
        model = LeaderboardEntry
        fields = ['_id', 'leaderboard_id', 'participant_id', 'participant_type',
                 'participant_name', 'score', 'rank', 'last_updated']
        read_only_fields = ['_id', 'last_updated']
    
    def get_participant_name(self, obj):
        """Get the name of the participant (user or team)"""
        if obj.participant_type == 'user':
            try:
                from django.contrib.auth import get_user_model
                User = get_user_model()
                user = User.objects.get(id=obj.participant_id)
                return f"{user.first_name} {user.last_name}"
            except:
                return f"User {obj.participant_id}"
        elif obj.participant_type == 'team':
            try:
                from teams.models import Team
                team = Team.objects.get(_id=obj.participant_id)
                return team.name
            except:
                return f"Team {obj.participant_id}"
        return "Unknown"
    
    def to_representation(self, instance):
        """Convert ObjectId to string"""
        data = super().to_representation(instance)
        if data.get('_id'):
            data['_id'] = str(data['_id'])
        if data.get('leaderboard_id'):
            data['leaderboard_id'] = str(data['leaderboard_id'])
        return data


class AchievementSerializer(serializers.ModelSerializer):
    """Serializer for Achievement model"""
    _id = serializers.CharField(read_only=True)
    
    class Meta:
        model = Achievement
        fields = ['_id', 'name', 'description', 'icon_url', 'criteria',
                 'points_reward', 'achievement_type', 'is_active', 'created_at']
        read_only_fields = ['_id', 'created_at']
    
    def to_representation(self, instance):
        """Convert ObjectId to string"""
        data = super().to_representation(instance)
        if data.get('_id'):
            data['_id'] = str(data['_id'])
        return data


class UserAchievementSerializer(serializers.ModelSerializer):
    """Serializer for UserAchievement model"""
    _id = serializers.CharField(read_only=True)
    achievement_id = serializers.CharField()
    achievement_details = serializers.SerializerMethodField()
    
    class Meta:
        model = UserAchievement
        fields = ['_id', 'user_id', 'achievement_id', 'achievement_details',
                 'earned_at', 'progress_data']
        read_only_fields = ['_id', 'earned_at']
    
    def get_achievement_details(self, obj):
        """Get achievement details"""
        try:
            achievement = Achievement.objects.get(_id=obj.achievement_id)
            return {
                'name': achievement.name,
                'description': achievement.description,
                'icon_url': achievement.icon_url,
                'points_reward': achievement.points_reward
            }
        except Achievement.DoesNotExist:
            return None
    
    def to_representation(self, instance):
        """Convert ObjectId to string"""
        data = super().to_representation(instance)
        if data.get('_id'):
            data['_id'] = str(data['_id'])
        if data.get('achievement_id'):
            data['achievement_id'] = str(data['achievement_id'])
        return data


class LeaderboardStatsSerializer(serializers.Serializer):
    """Serializer for leaderboard statistics"""
    total_participants = serializers.IntegerField()
    top_score = serializers.IntegerField()
    user_rank = serializers.IntegerField()
    user_score = serializers.IntegerField()