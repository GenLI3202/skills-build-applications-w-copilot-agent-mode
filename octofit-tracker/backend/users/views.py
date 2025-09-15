from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from .models import UserProfile
from .serializers import UserSerializer, UserProfileSerializer, UserRegistrationSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for User model"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        """Allow registration without authentication"""
        if self.action == 'create':
            return [AllowAny()]
        return super().get_permissions()
    
    def get_serializer_class(self):
        """Use registration serializer for user creation"""
        if self.action == 'create':
            return UserRegistrationSerializer
        return super().get_serializer_class()
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Get current user's profile"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class UserProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for UserProfile model"""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter profiles based on user permissions"""
        if self.request.user.is_staff:
            return UserProfile.objects.all()
        return UserProfile.objects.filter(user_id=self.request.user.id)
