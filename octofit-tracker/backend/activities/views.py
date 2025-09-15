from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import ActivityType, Activity, WorkoutSuggestion
from .serializers import ActivityTypeSerializer, ActivitySerializer, WorkoutSuggestionSerializer


class ActivityTypeViewSet(viewsets.ModelViewSet):
    """ViewSet for ActivityType model"""
    queryset = ActivityType.objects.all()
    serializer_class = ActivityTypeSerializer
    permission_classes = [IsAuthenticated]


class ActivityViewSet(viewsets.ModelViewSet):
    """ViewSet for Activity model"""
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter activities based on user permissions"""
        if self.request.user.is_staff:
            return Activity.objects.all()
        return Activity.objects.filter(user_id=self.request.user.id)
    
    def perform_create(self, serializer):
        """Set user_id when creating new activity"""
        serializer.save(user_id=self.request.user.id)
    
    @action(detail=False, methods=['get'])
    def my_activities(self, request):
        """Get current user's activities"""
        activities = Activity.objects.filter(user_id=request.user.id)
        serializer = self.get_serializer(activities, many=True)
        return Response(serializer.data)


class WorkoutSuggestionViewSet(viewsets.ModelViewSet):
    """ViewSet for WorkoutSuggestion model"""
    queryset = WorkoutSuggestion.objects.all()
    serializer_class = WorkoutSuggestionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter workout suggestions based on user permissions"""
        if self.request.user.is_staff:
            return WorkoutSuggestion.objects.all()
        return WorkoutSuggestion.objects.filter(user_id=self.request.user.id)
    
    def perform_create(self, serializer):
        """Set user_id when creating new workout suggestion"""
        serializer.save(user_id=self.request.user.id)
