from rest_framework import serializers
from .models import User, Team, Activity, Leaderboard, Workout
from bson import ObjectId


class ObjectIdField(serializers.Field):
    """Custom field to convert ObjectId to string"""
    def to_representation(self, value):
        return str(value)
    
    def to_internal_value(self, data):
        try:
            return ObjectId(data)
        except Exception:
            raise serializers.ValidationError('Invalid ObjectId')


class UserSerializer(serializers.ModelSerializer):
    id = ObjectIdField(source='_id', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'team_id', 'team_name', 'avatar', 'total_points', 'created_at']
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Remove the _id field if present and use id
        if '_id' in data:
            data.pop('_id')
        return data


class TeamSerializer(serializers.ModelSerializer):
    id = ObjectIdField(source='_id', read_only=True)
    
    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'created_at', 'members']
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if '_id' in data:
            data.pop('_id')
        return data


class ActivitySerializer(serializers.ModelSerializer):
    id = ObjectIdField(source='_id', read_only=True)
    
    class Meta:
        model = Activity
        fields = ['id', 'user_id', 'user_name', 'user_email', 'activity_type', 
                  'duration_minutes', 'distance_km', 'calories_burned', 
                  'points_earned', 'date', 'created_at']
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if '_id' in data:
            data.pop('_id')
        return data


class LeaderboardSerializer(serializers.ModelSerializer):
    id = ObjectIdField(source='_id', read_only=True)
    
    class Meta:
        model = Leaderboard
        fields = ['id', 'type', 'rank', 'user_id', 'user_name', 'user_email', 
                  'team_name', 'team_id', 'member_count', 'total_points', 'updated_at']
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if '_id' in data:
            data.pop('_id')
        # Remove null fields for cleaner response
        return {k: v for k, v in data.items() if v is not None}


class WorkoutSerializer(serializers.ModelSerializer):
    id = ObjectIdField(source='_id', read_only=True)
    
    class Meta:
        model = Workout
        fields = ['id', 'name', 'description', 'duration_minutes', 'difficulty', 
                  'exercises', 'points_value', 'created_at']
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if '_id' in data:
            data.pop('_id')
        return data
