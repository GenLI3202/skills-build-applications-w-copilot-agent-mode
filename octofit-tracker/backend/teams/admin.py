from django.contrib import admin
from .models import Team, TeamMembership, Challenge


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """Admin configuration for Team model"""
    list_display = ('name', 'captain_id', 'max_members', 'total_points', 'is_public', 'created_at')
    list_filter = ('is_public', 'created_at')
    search_fields = ('name', 'description', 'team_code')
    readonly_fields = ('_id', 'created_at', 'updated_at')
    ordering = ('-created_at',)


@admin.register(TeamMembership)
class TeamMembershipAdmin(admin.ModelAdmin):
    """Admin configuration for TeamMembership model"""
    list_display = ('user_id', 'team_id', 'role', 'points_contributed', 'joined_at')
    list_filter = ('role', 'joined_at')
    search_fields = ('user_id', 'team_id')
    readonly_fields = ('_id', 'joined_at')
    ordering = ('-joined_at',)


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    """Admin configuration for Challenge model"""
    list_display = ('title', 'challenge_type', 'target_value', 'start_date', 'end_date', 'is_active')
    list_filter = ('challenge_type', 'is_active', 'start_date', 'end_date')
    search_fields = ('title', 'description')
    readonly_fields = ('_id', 'created_at')
    ordering = ('-start_date',)
