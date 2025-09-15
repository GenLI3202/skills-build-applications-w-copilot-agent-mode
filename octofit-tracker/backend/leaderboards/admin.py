from django.contrib import admin
from .models import Leaderboard, LeaderboardEntry, Achievement, UserAchievement


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    """Admin configuration for Leaderboard model"""
    list_display = ('name', 'leaderboard_type', 'category', 'is_active', 'created_at')
    list_filter = ('leaderboard_type', 'category', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('_id', 'created_at')
    ordering = ('-created_at',)


@admin.register(LeaderboardEntry)
class LeaderboardEntryAdmin(admin.ModelAdmin):
    """Admin configuration for LeaderboardEntry model"""
    list_display = ('leaderboard_id', 'participant_id', 'participant_type', 'score', 'rank')
    list_filter = ('participant_type', 'last_updated')
    search_fields = ('leaderboard_id', 'participant_id')
    readonly_fields = ('_id', 'last_updated')
    ordering = ('rank',)


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    """Admin configuration for Achievement model"""
    list_display = ('name', 'achievement_type', 'points_reward', 'is_active')
    list_filter = ('achievement_type', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('_id', 'created_at')
    ordering = ('name',)


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    """Admin configuration for UserAchievement model"""
    list_display = ('user_id', 'achievement_id', 'earned_at')
    list_filter = ('earned_at',)
    search_fields = ('user_id', 'achievement_id')
    readonly_fields = ('_id', 'earned_at')
    ordering = ('-earned_at',)
