from django.contrib import admin
from .models import ActivityType, Activity, WorkoutSuggestion


@admin.register(ActivityType)
class ActivityTypeAdmin(admin.ModelAdmin):
    """Admin configuration for ActivityType model"""
    list_display = ('name', 'category', 'points_per_minute', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('name',)


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    """Admin configuration for Activity model"""
    list_display = ('user_id', 'activity_type_id', 'duration_minutes', 'intensity', 'points_earned', 'date_logged')
    list_filter = ('intensity', 'date_logged', 'created_at')
    search_fields = ('user_id', 'notes')
    readonly_fields = ('_id', 'created_at')
    ordering = ('-date_logged',)


@admin.register(WorkoutSuggestion)
class WorkoutSuggestionAdmin(admin.ModelAdmin):
    """Admin configuration for WorkoutSuggestion model"""
    list_display = ('title', 'user_id', 'difficulty_level', 'estimated_duration', 'is_completed', 'created_at')
    list_filter = ('difficulty_level', 'is_completed', 'created_at')
    search_fields = ('title', 'description', 'user_id')
    readonly_fields = ('_id', 'created_at')
    ordering = ('-created_at',)
