from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Leaderboard, LeaderboardEntry, Achievement, UserAchievement
from .serializers import LeaderboardSerializer, LeaderboardEntrySerializer, AchievementSerializer, UserAchievementSerializer


class LeaderboardViewSet(viewsets.ModelViewSet):
    """ViewSet for Leaderboard model"""
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['get'])
    def entries(self, request, pk=None):
        """Get entries for a specific leaderboard"""
        leaderboard = self.get_object()
        entries = LeaderboardEntry.objects.filter(
            leaderboard_id=str(leaderboard._id)
        ).order_by('-points')
        serializer = LeaderboardEntrySerializer(entries, many=True)
        return Response(serializer.data)


class LeaderboardEntryViewSet(viewsets.ModelViewSet):
    """ViewSet for LeaderboardEntry model"""
    queryset = LeaderboardEntry.objects.all()
    serializer_class = LeaderboardEntrySerializer
    permission_classes = [IsAuthenticated]


class AchievementViewSet(viewsets.ModelViewSet):
    """ViewSet for Achievement model"""
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    permission_classes = [IsAuthenticated]


class UserAchievementViewSet(viewsets.ModelViewSet):
    """ViewSet for UserAchievement model"""
    queryset = UserAchievement.objects.all()
    serializer_class = UserAchievementSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter user achievements based on permissions"""
        if self.request.user.is_staff:
            return UserAchievement.objects.all()
        return UserAchievement.objects.filter(user_id=self.request.user.id)
    
    @action(detail=False, methods=['get'])
    def my_achievements(self, request):
        """Get current user's achievements"""
        achievements = UserAchievement.objects.filter(user_id=request.user.id)
        serializer = self.get_serializer(achievements, many=True)
        return Response(serializer.data)
