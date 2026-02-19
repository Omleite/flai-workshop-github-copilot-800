from django.contrib import admin
from .models import User, Team, Activity, Leaderboard, Workout


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'team_name', 'total_points', 'created_at')
    list_filter = ('team_name',)
    search_fields = ('name', 'email')
    ordering = ('-total_points',)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name',)


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'activity_type', 'duration_minutes', 'points_earned', 'date')
    list_filter = ('activity_type', 'user_name')
    search_fields = ('user_name', 'user_email')
    ordering = ('-date',)


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ('rank', 'type', 'get_name', 'total_points', 'updated_at')
    list_filter = ('type',)
    ordering = ('rank',)
    
    def get_name(self, obj):
        if obj.type == 'individual':
            return obj.user_name
        return obj.team_name
    get_name.short_description = 'Name'


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('name', 'difficulty', 'duration_minutes', 'points_value', 'created_at')
    list_filter = ('difficulty',)
    search_fields = ('name', 'description')
    ordering = ('-points_value',)
