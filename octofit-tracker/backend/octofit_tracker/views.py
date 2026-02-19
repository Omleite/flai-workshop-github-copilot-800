from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, Team, Activity, Leaderboard, Workout
from .serializers import (
    UserSerializer, TeamSerializer, ActivitySerializer,
    LeaderboardSerializer, WorkoutSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for User operations
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    @action(detail=False, methods=['get'])
    def by_team(self, request):
        """Get users by team_id"""
        team_id = request.query_params.get('team_id', None)
        if team_id:
            users = User.objects.filter(team_id=team_id)
            serializer = self.get_serializer(users, many=True)
            return Response(serializer.data)
        return Response({'error': 'team_id parameter required'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def by_email(self, request):
        """Get user by email"""
        email = request.query_params.get('email', None)
        if email:
            try:
                user = User.objects.get(email=email)
                serializer = self.get_serializer(user)
                return Response(serializer.data)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'error': 'email parameter required'}, status=status.HTTP_400_BAD_REQUEST)


class TeamViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Team operations
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    
    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        """Get all members of a team"""
        team = self.get_object()
        users = User.objects.filter(team_id=str(team._id))
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class ActivityViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Activity operations
    """
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    
    @action(detail=False, methods=['get'])
    def by_user(self, request):
        """Get activities by user_id"""
        user_id = request.query_params.get('user_id', None)
        if user_id:
            activities = Activity.objects.filter(user_id=user_id).order_by('-date')
            serializer = self.get_serializer(activities, many=True)
            return Response(serializer.data)
        return Response({'error': 'user_id parameter required'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent activities"""
        limit = int(request.query_params.get('limit', 10))
        activities = Activity.objects.all().order_by('-date')[:limit]
        serializer = self.get_serializer(activities, many=True)
        return Response(serializer.data)


class LeaderboardViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Leaderboard operations
    """
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer
    
    @action(detail=False, methods=['get'])
    def individual(self, request):
        """Get individual leaderboard"""
        leaderboard = Leaderboard.objects.filter(type='individual').order_by('rank')
        serializer = self.get_serializer(leaderboard, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def team(self, request):
        """Get team leaderboard"""
        leaderboard = Leaderboard.objects.filter(type='team').order_by('rank')
        serializer = self.get_serializer(leaderboard, many=True)
        return Response(serializer.data)


class WorkoutViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Workout operations
    """
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    
    @action(detail=False, methods=['get'])
    def by_difficulty(self, request):
        """Get workouts by difficulty level"""
        difficulty = request.query_params.get('difficulty', None)
        if difficulty:
            workouts = Workout.objects.filter(difficulty__iexact=difficulty)
            serializer = self.get_serializer(workouts, many=True)
            return Response(serializer.data)
        return Response({'error': 'difficulty parameter required'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def recommend(self, request):
        """Get recommended workouts (random suggestion)"""
        import random
        workouts = list(Workout.objects.all())
        if workouts:
            recommended = random.sample(workouts, min(3, len(workouts)))
            serializer = self.get_serializer(recommended, many=True)
            return Response(serializer.data)
        return Response([])
