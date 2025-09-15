from rest_framework import serializers
from .models import Team, TeamMembership, Challenge


class TeamSerializer(serializers.ModelSerializer):
    """Serializer for Team model"""
    _id = serializers.CharField(read_only=True)
    member_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Team
        fields = ['_id', 'name', 'description', 'captain_id', 'max_members', 
                 'is_public', 'team_code', 'total_points', 'member_count',
                 'created_at', 'updated_at']
        read_only_fields = ['_id', 'team_code', 'total_points', 'created_at', 'updated_at']
    
    def get_member_count(self, obj):
        """Get current number of team members"""
        return TeamMembership.objects.filter(team_id=obj._id).count()
    
    def to_representation(self, instance):
        """Convert ObjectId to string"""
        data = super().to_representation(instance)
        if data.get('_id'):
            data['_id'] = str(data['_id'])
        return data


class TeamMembershipSerializer(serializers.ModelSerializer):
    """Serializer for TeamMembership model"""
    _id = serializers.CharField(read_only=True)
    team_id = serializers.CharField()
    
    class Meta:
        model = TeamMembership
        fields = ['_id', 'team_id', 'user_id', 'role', 'joined_at', 'points_contributed']
        read_only_fields = ['_id', 'joined_at', 'points_contributed']
    
    def to_representation(self, instance):
        """Convert ObjectId to string"""
        data = super().to_representation(instance)
        if data.get('_id'):
            data['_id'] = str(data['_id'])
        if data.get('team_id'):
            data['team_id'] = str(data['team_id'])
        return data


class ChallengeSerializer(serializers.ModelSerializer):
    """Serializer for Challenge model"""
    _id = serializers.CharField(read_only=True)
    
    class Meta:
        model = Challenge
        fields = ['_id', 'title', 'description', 'challenge_type', 'target_value',
                 'start_date', 'end_date', 'participating_teams', 'rewards', 
                 'is_active', 'created_at']
        read_only_fields = ['_id', 'created_at']
    
    def to_representation(self, instance):
        """Convert ObjectId to string"""
        data = super().to_representation(instance)
        if data.get('_id'):
            data['_id'] = str(data['_id'])
        return data


class TeamJoinSerializer(serializers.Serializer):
    """Serializer for joining a team"""
    team_code = serializers.CharField(max_length=8)
    
    def validate_team_code(self, value):
        """Validate that team exists and has space"""
        try:
            team = Team.objects.get(team_code=value)
            current_members = TeamMembership.objects.filter(team_id=team._id).count()
            if current_members >= team.max_members:
                raise serializers.ValidationError("Team is full")
            return value
        except Team.DoesNotExist:
            raise serializers.ValidationError("Invalid team code")


class TeamStatsSerializer(serializers.ModelSerializer):
    """Serializer for team statistics"""
    _id = serializers.CharField(read_only=True)
    member_count = serializers.SerializerMethodField()
    recent_activities = serializers.SerializerMethodField()
    
    class Meta:
        model = Team
        fields = ['_id', 'name', 'total_points', 'member_count', 'recent_activities']
    
    def get_member_count(self, obj):
        return TeamMembership.objects.filter(team_id=obj._id).count()
    
    def get_recent_activities(self, obj):
        # This would need to be implemented to get recent team activities
        return []
    
    def to_representation(self, instance):
        """Convert ObjectId to string"""
        data = super().to_representation(instance)
        if data.get('_id'):
            data['_id'] = str(data['_id'])
        return data