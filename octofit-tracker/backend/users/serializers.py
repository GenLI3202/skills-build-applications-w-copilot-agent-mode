from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserProfile

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                 'date_of_birth', 'height', 'weight', 'fitness_level', 
                 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for UserProfile model"""
    _id = serializers.CharField(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['_id', 'user_id', 'bio', 'profile_picture', 'total_points', 
                 'achievements', 'preferences']
        read_only_fields = ['_id', 'total_points']
    
    def to_representation(self, instance):
        """Convert ObjectId to string"""
        data = super().to_representation(instance)
        if data.get('_id'):
            data['_id'] = str(data['_id'])
        return data


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 
                 'first_name', 'last_name', 'date_of_birth', 'height', 
                 'weight', 'fitness_level']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        attrs.pop('password_confirm')
        return attrs
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        
        # Create associated UserProfile
        UserProfile.objects.create(
            user_id=user.id,
            bio="",
            preferences={}
        )
        
        return user