from rest_framework import serializers
from .models import ActivityType, Activity, WorkoutSuggestion


class ActivityTypeSerializer(serializers.ModelSerializer):
    """Serializer for ActivityType model"""
    class Meta:
        model = ActivityType
        fields = ['id', 'name', 'description', 'points_per_minute', 'category', 'created_at']
        read_only_fields = ['id', 'created_at']


class ActivitySerializer(serializers.ModelSerializer):
    """Serializer for Activity model"""
    _id = serializers.CharField(read_only=True)
    
    class Meta:
        model = Activity
        fields = ['_id', 'user_id', 'activity_type_id', 'duration_minutes', 
                 'intensity', 'calories_burned', 'notes', 'date_logged', 
                 'points_earned', 'created_at']
        read_only_fields = ['_id', 'points_earned', 'created_at']
    
    def to_representation(self, instance):
        """Convert ObjectId to string"""
        data = super().to_representation(instance)
        if data.get('_id'):
            data['_id'] = str(data['_id'])
        return data


class WorkoutSuggestionSerializer(serializers.ModelSerializer):
    """Serializer for WorkoutSuggestion model"""
    _id = serializers.CharField(read_only=True)
    
    class Meta:
        model = WorkoutSuggestion
        fields = ['_id', 'user_id', 'title', 'description', 'difficulty_level', 
                 'estimated_duration', 'exercises', 'is_completed', 'created_at']
        read_only_fields = ['_id', 'created_at']
    
    def to_representation(self, instance):
        """Convert ObjectId to string"""
        data = super().to_representation(instance)
        if data.get('_id'):
            data['_id'] = str(data['_id'])
        return data


class ActivityLogSerializer(serializers.ModelSerializer):
    """Serializer for creating activity logs with automatic point calculation"""
    activity_type_name = serializers.CharField(source='activity_type.name', read_only=True)
    
    class Meta:
        model = Activity
        fields = ['_id', 'user_id', 'activity_type_id', 'activity_type_name', 
                 'duration_minutes', 'intensity', 'calories_burned', 'notes', 
                 'date_logged', 'points_earned', 'created_at']
        read_only_fields = ['_id', 'points_earned', 'created_at']
    
    def create(self, validated_data):
        # Calculate points based on activity type and duration
        activity_type = ActivityType.objects.get(id=validated_data['activity_type_id'])
        base_points = activity_type.points_per_minute * validated_data['duration_minutes']
        
        # Adjust points based on intensity
        intensity_multipliers = {
            'low': 0.8,
            'moderate': 1.0,
            'high': 1.3,
            'very_high': 1.6
        }
        
        multiplier = intensity_multipliers.get(validated_data.get('intensity', 'moderate'), 1.0)
        validated_data['points_earned'] = int(base_points * multiplier)
        
        return super().create(validated_data)
    
    def to_representation(self, instance):
        """Convert ObjectId to string"""
        data = super().to_representation(instance)
        if data.get('_id'):
            data['_id'] = str(data['_id'])
        return data