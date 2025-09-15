"""octofit_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
import os

# Create router for API endpoints
router = DefaultRouter()

# Import viewsets when they're created
# from users.views import UserViewSet, UserProfileViewSet
# from activities.views import ActivityTypeViewSet, ActivityViewSet, WorkoutSuggestionViewSet
# from teams.views import TeamViewSet, TeamMembershipViewSet, ChallengeViewSet
# from leaderboards.views import LeaderboardViewSet, LeaderboardEntryViewSet, AchievementViewSet

# Register viewsets with router
# router.register(r'users', UserViewSet)
# router.register(r'user-profiles', UserProfileViewSet)
# router.register(r'activity-types', ActivityTypeViewSet)
# router.register(r'activities', ActivityViewSet)
# router.register(r'workout-suggestions', WorkoutSuggestionViewSet)
# router.register(r'teams', TeamViewSet)
# router.register(r'team-memberships', TeamMembershipViewSet)
# router.register(r'challenges', ChallengeViewSet)
# router.register(r'leaderboards', LeaderboardViewSet)
# router.register(r'leaderboard-entries', LeaderboardEntryViewSet)
# router.register(r'achievements', AchievementViewSet)

@api_view(['GET'])
def api_root(request, format=None):
    """API root endpoint"""
    codespace_name = os.environ.get('CODESPACE_NAME')
    if codespace_name:
        base_url = f"https://{codespace_name}-8000.app.github.dev"
    else:
        base_url = "http://localhost:8000"
    
    return Response({
        'message': 'Welcome to OctoFit Tracker API',
        'version': '1.0',
        'base_url': base_url,
        'endpoints': {
            'admin': reverse('admin:index', request=request, format=format),
            'api': reverse('api-root', request=request, format=format),
            'auth': {
                'login': f"{base_url}/api/auth/login/",
                'logout': f"{base_url}/api/auth/logout/",
                'register': f"{base_url}/api/auth/registration/",
            }
        }
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api_root, name='api-root'),
    path('api/', include(router.urls)),
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
]
