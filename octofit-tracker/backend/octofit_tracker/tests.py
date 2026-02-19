from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from datetime import datetime
from .models import User, Team, Activity, Leaderboard, Workout


class UserModelTest(TestCase):
    """Test cases for User model"""
    
    def setUp(self):
        self.user = User.objects.create(
            name='Test Hero',
            email='testhero@test.com',
            team_name='Test Team',
            total_points=100,
            created_at=datetime.now().isoformat()
        )
    
    def test_user_creation(self):
        """Test user is created successfully"""
        self.assertEqual(self.user.name, 'Test Hero')
        self.assertEqual(self.user.email, 'testhero@test.com')
        self.assertEqual(self.user.total_points, 100)
    
    def test_user_string_representation(self):
        """Test user string representation"""
        self.assertEqual(str(self.user), 'Test Hero')


class TeamModelTest(TestCase):
    """Test cases for Team model"""
    
    def setUp(self):
        self.team = Team.objects.create(
            name='Test Avengers',
            description='Test team description',
            created_at=datetime.now().isoformat(),
            members=[]
        )
    
    def test_team_creation(self):
        """Test team is created successfully"""
        self.assertEqual(self.team.name, 'Test Avengers')
        self.assertEqual(self.team.description, 'Test team description')
    
    def test_team_string_representation(self):
        """Test team string representation"""
        self.assertEqual(str(self.team), 'Test Avengers')


class ActivityModelTest(TestCase):
    """Test cases for Activity model"""
    
    def setUp(self):
        self.activity = Activity.objects.create(
            user_id='123',
            user_name='Test Hero',
            user_email='testhero@test.com',
            activity_type='Running',
            duration_minutes=30,
            distance_km=5.0,
            calories_burned=300,
            points_earned=50,
            date=datetime.now().isoformat(),
            created_at=datetime.now().isoformat()
        )
    
    def test_activity_creation(self):
        """Test activity is created successfully"""
        self.assertEqual(self.activity.user_name, 'Test Hero')
        self.assertEqual(self.activity.activity_type, 'Running')
        self.assertEqual(self.activity.duration_minutes, 30)
        self.assertEqual(self.activity.points_earned, 50)


class WorkoutModelTest(TestCase):
    """Test cases for Workout model"""
    
    def setUp(self):
        self.workout = Workout.objects.create(
            name='Test Workout',
            description='Test workout description',
            duration_minutes=45,
            difficulty='Intermediate',
            exercises=['Push-ups', 'Squats'],
            points_value=100,
            created_at=datetime.now().isoformat()
        )
    
    def test_workout_creation(self):
        """Test workout is created successfully"""
        self.assertEqual(self.workout.name, 'Test Workout')
        self.assertEqual(self.workout.difficulty, 'Intermediate')
        self.assertEqual(self.workout.points_value, 100)


class UserAPITest(APITestCase):
    """Test cases for User API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            name='API Test Hero',
            email='apitest@test.com',
            team_name='API Test Team',
            total_points=200,
            created_at=datetime.now().isoformat()
        )
    
    def test_get_users_list(self):
        """Test retrieving list of users"""
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
    
    def test_get_user_detail(self):
        """Test retrieving a single user"""
        response = self.client.get(f'/api/users/{self.user._id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'API Test Hero')


class TeamAPITest(APITestCase):
    """Test cases for Team API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.team = Team.objects.create(
            name='API Test Team',
            description='API test team description',
            created_at=datetime.now().isoformat(),
            members=[]
        )
    
    def test_get_teams_list(self):
        """Test retrieving list of teams"""
        response = self.client.get('/api/teams/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
    
    def test_get_team_detail(self):
        """Test retrieving a single team"""
        response = self.client.get(f'/api/teams/{self.team._id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'API Test Team')


class ActivityAPITest(APITestCase):
    """Test cases for Activity API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.activity = Activity.objects.create(
            user_id='test123',
            user_name='Test Hero',
            user_email='test@test.com',
            activity_type='Cycling',
            duration_minutes=40,
            distance_km=15.0,
            calories_burned=400,
            points_earned=75,
            date=datetime.now().isoformat(),
            created_at=datetime.now().isoformat()
        )
    
    def test_get_activities_list(self):
        """Test retrieving list of activities"""
        response = self.client.get('/api/activities/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
    
    def test_get_recent_activities(self):
        """Test retrieving recent activities"""
        response = self.client.get('/api/activities/recent/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WorkoutAPITest(APITestCase):
    """Test cases for Workout API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.workout = Workout.objects.create(
            name='API Test Workout',
            description='API test workout description',
            duration_minutes=50,
            difficulty='Advanced',
            exercises=['Burpees', 'Pull-ups'],
            points_value=120,
            created_at=datetime.now().isoformat()
        )
    
    def test_get_workouts_list(self):
        """Test retrieving list of workouts"""
        response = self.client.get('/api/workouts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
    
    def test_get_workout_detail(self):
        """Test retrieving a single workout"""
        response = self.client.get(f'/api/workouts/{self.workout._id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'API Test Workout')


class APIRootTest(APITestCase):
    """Test cases for API root endpoint"""
    
    def test_api_root(self):
        """Test API root endpoint returns proper structure"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertIn('endpoints', response.data)
        self.assertIn('users', response.data['endpoints'])
        self.assertIn('teams', response.data['endpoints'])
        self.assertIn('activities', response.data['endpoints'])
        self.assertIn('workouts', response.data['endpoints'])
