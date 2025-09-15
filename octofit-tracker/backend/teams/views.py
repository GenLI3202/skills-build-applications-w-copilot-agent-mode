from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Team, TeamMembership, Challenge
from .serializers import TeamSerializer, TeamMembershipSerializer, ChallengeSerializer


class TeamViewSet(viewsets.ModelViewSet):
    """ViewSet for Team model"""
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        """Join a team"""
        team = self.get_object()
        # Check if user is already a member
        existing_membership = TeamMembership.objects.filter(
            team_id=str(team._id), user_id=request.user.id
        ).first()
        
        if existing_membership:
            return Response(
                {'error': 'Already a member of this team'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create membership
        TeamMembership.objects.create(
            team_id=str(team._id),
            user_id=request.user.id,
            role='member'
        )
        
        return Response({'message': 'Successfully joined team'})
    
    @action(detail=False, methods=['get'])
    def my_teams(self, request):
        """Get teams where current user is a member"""
        memberships = TeamMembership.objects.filter(user_id=request.user.id)
        team_ids = [membership.team_id for membership in memberships]
        teams = Team.objects.filter(_id__in=team_ids)
        serializer = self.get_serializer(teams, many=True)
        return Response(serializer.data)


class TeamMembershipViewSet(viewsets.ModelViewSet):
    """ViewSet for TeamMembership model"""
    queryset = TeamMembership.objects.all()
    serializer_class = TeamMembershipSerializer
    permission_classes = [IsAuthenticated]


class ChallengeViewSet(viewsets.ModelViewSet):
    """ViewSet for Challenge model"""
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get active challenges"""
        active_challenges = Challenge.objects.filter(is_active=True)
        serializer = self.get_serializer(active_challenges, many=True)
        return Response(serializer.data)
