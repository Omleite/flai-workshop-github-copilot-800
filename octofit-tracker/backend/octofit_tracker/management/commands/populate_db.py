from django.core.management.base import BaseCommand
from pymongo import MongoClient
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Connect to MongoDB
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']
        
        self.stdout.write(self.style.SUCCESS('Connecting to octofit_db database...'))
        
        # Clear existing data
        self.stdout.write('Clearing existing data...')
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})
        
        # Create unique index on email field
        self.stdout.write('Creating unique index on email field...')
        db.users.create_index([('email', 1)], unique=True)
        
        # Insert Teams
        self.stdout.write('Inserting teams...')
        teams_data = [
            {
                'name': 'Team Marvel',
                'description': 'Avengers and Marvel superheroes unite!',
                'created_at': datetime.now().isoformat(),
                'members': []
            },
            {
                'name': 'Team DC',
                'description': 'Justice League and DC heroes assemble!',
                'created_at': datetime.now().isoformat(),
                'members': []
            }
        ]
        teams_result = db.teams.insert_many(teams_data)
        team_marvel_id = teams_result.inserted_ids[0]
        team_dc_id = teams_result.inserted_ids[1]
        
        # Insert Users (Superheroes)
        self.stdout.write('Inserting superhero users...')
        users_data = [
            # Team Marvel
            {
                'name': 'Tony Stark',
                'email': 'ironman@marvel.com',
                'team_id': str(team_marvel_id),
                'team_name': 'Team Marvel',
                'avatar': 'https://i.pravatar.cc/150?img=12',
                'total_points': 2500,
                'created_at': datetime.now().isoformat()
            },
            {
                'name': 'Steve Rogers',
                'email': 'captainamerica@marvel.com',
                'team_id': str(team_marvel_id),
                'team_name': 'Team Marvel',
                'avatar': 'https://i.pravatar.cc/150?img=13',
                'total_points': 2800,
                'created_at': datetime.now().isoformat()
            },
            {
                'name': 'Natasha Romanoff',
                'email': 'blackwidow@marvel.com',
                'team_id': str(team_marvel_id),
                'team_name': 'Team Marvel',
                'avatar': 'https://i.pravatar.cc/150?img=14',
                'total_points': 2400,
                'created_at': datetime.now().isoformat()
            },
            {
                'name': 'Bruce Banner',
                'email': 'hulk@marvel.com',
                'team_id': str(team_marvel_id),
                'team_name': 'Team Marvel',
                'avatar': 'https://i.pravatar.cc/150?img=15',
                'total_points': 2100,
                'created_at': datetime.now().isoformat()
            },
            {
                'name': 'Thor Odinson',
                'email': 'thor@marvel.com',
                'team_id': str(team_marvel_id),
                'team_name': 'Team Marvel',
                'avatar': 'https://i.pravatar.cc/150?img=16',
                'total_points': 2700,
                'created_at': datetime.now().isoformat()
            },
            # Team DC
            {
                'name': 'Bruce Wayne',
                'email': 'batman@dc.com',
                'team_id': str(team_dc_id),
                'team_name': 'Team DC',
                'avatar': 'https://i.pravatar.cc/150?img=17',
                'total_points': 2900,
                'created_at': datetime.now().isoformat()
            },
            {
                'name': 'Clark Kent',
                'email': 'superman@dc.com',
                'team_id': str(team_dc_id),
                'team_name': 'Team DC',
                'avatar': 'https://i.pravatar.cc/150?img=18',
                'total_points': 3100,
                'created_at': datetime.now().isoformat()
            },
            {
                'name': 'Diana Prince',
                'email': 'wonderwoman@dc.com',
                'team_id': str(team_dc_id),
                'team_name': 'Team DC',
                'avatar': 'https://i.pravatar.cc/150?img=19',
                'total_points': 2600,
                'created_at': datetime.now().isoformat()
            },
            {
                'name': 'Barry Allen',
                'email': 'flash@dc.com',
                'team_id': str(team_dc_id),
                'team_name': 'Team DC',
                'avatar': 'https://i.pravatar.cc/150?img=20',
                'total_points': 2300,
                'created_at': datetime.now().isoformat()
            },
            {
                'name': 'Arthur Curry',
                'email': 'aquaman@dc.com',
                'team_id': str(team_dc_id),
                'team_name': 'Team DC',
                'avatar': 'https://i.pravatar.cc/150?img=21',
                'total_points': 2200,
                'created_at': datetime.now().isoformat()
            }
        ]
        users_result = db.users.insert_many(users_data)
        user_ids = users_result.inserted_ids
        
        # Update teams with member IDs
        marvel_members = [str(uid) for uid in user_ids[:5]]
        dc_members = [str(uid) for uid in user_ids[5:]]
        
        db.teams.update_one(
            {'_id': team_marvel_id},
            {'$set': {'members': marvel_members}}
        )
        db.teams.update_one(
            {'_id': team_dc_id},
            {'$set': {'members': dc_members}}
        )
        
        # Insert Workouts
        self.stdout.write('Inserting workout suggestions...')
        workouts_data = [
            {
                'name': 'Super Soldier Training',
                'description': 'High-intensity military training for peak performance',
                'duration_minutes': 45,
                'difficulty': 'Advanced',
                'exercises': ['Push-ups', 'Pull-ups', 'Sprints', 'Burpees'],
                'points_value': 100,
                'created_at': datetime.now().isoformat()
            },
            {
                'name': 'Asgardian Strength Circuit',
                'description': 'Build god-like strength with this power workout',
                'duration_minutes': 60,
                'difficulty': 'Expert',
                'exercises': ['Deadlifts', 'Hammer Curls', 'Battle Ropes', 'Box Jumps'],
                'points_value': 150,
                'created_at': datetime.now().isoformat()
            },
            {
                'name': 'Speed Force Cardio',
                'description': 'Lightning-fast cardio session',
                'duration_minutes': 30,
                'difficulty': 'Intermediate',
                'exercises': ['Sprint Intervals', 'Jump Rope', 'High Knees', 'Mountain Climbers'],
                'points_value': 75,
                'created_at': datetime.now().isoformat()
            },
            {
                'name': 'Amazonian Warrior Training',
                'description': 'Combat-ready fitness training',
                'duration_minutes': 50,
                'difficulty': 'Advanced',
                'exercises': ['Sword Swings', 'Shield Carries', 'Lunges', 'Planks'],
                'points_value': 120,
                'created_at': datetime.now().isoformat()
            },
            {
                'name': 'Bat-Training Routine',
                'description': 'Stealth and agility training',
                'duration_minutes': 40,
                'difficulty': 'Advanced',
                'exercises': ['Ninja Rolls', 'Parkour', 'Core Work', 'Flexibility'],
                'points_value': 110,
                'created_at': datetime.now().isoformat()
            },
            {
                'name': 'Beginner Hero Basics',
                'description': 'Start your superhero journey',
                'duration_minutes': 25,
                'difficulty': 'Beginner',
                'exercises': ['Walking', 'Light Jogging', 'Stretching', 'Basic Squats'],
                'points_value': 50,
                'created_at': datetime.now().isoformat()
            }
        ]
        workouts_result = db.workouts.insert_many(workouts_data)
        workout_ids = workouts_result.inserted_ids
        
        # Insert Activities
        self.stdout.write('Inserting activity logs...')
        activities_data = []
        activity_types = ['Running', 'Cycling', 'Swimming', 'Weightlifting', 'Yoga', 'Boxing', 'HIIT', 'Crossfit']
        
        for i, user_id in enumerate(user_ids):
            user_email = users_data[i]['email']
            user_name = users_data[i]['name']
            
            # Generate 3-5 activities per user
            for j in range(random.randint(3, 5)):
                days_ago = random.randint(0, 30)
                activity_date = datetime.now() - timedelta(days=days_ago)
                
                activities_data.append({
                    'user_id': str(user_id),
                    'user_name': user_name,
                    'user_email': user_email,
                    'activity_type': random.choice(activity_types),
                    'duration_minutes': random.randint(20, 90),
                    'distance_km': round(random.uniform(1, 20), 2),
                    'calories_burned': random.randint(100, 800),
                    'points_earned': random.randint(50, 150),
                    'date': activity_date.isoformat(),
                    'created_at': datetime.now().isoformat()
                })
        
        db.activities.insert_many(activities_data)
        
        # Calculate and insert Leaderboard entries
        self.stdout.write('Calculating leaderboard...')
        leaderboard_data = []
        
        # Individual leaderboard
        sorted_users = sorted(users_data, key=lambda x: x['total_points'], reverse=True)
        for rank, user in enumerate(sorted_users, 1):
            leaderboard_data.append({
                'type': 'individual',
                'rank': rank,
                'user_id': str(user_ids[users_data.index(user)]),
                'user_name': user['name'],
                'user_email': user['email'],
                'team_name': user['team_name'],
                'total_points': user['total_points'],
                'updated_at': datetime.now().isoformat()
            })
        
        # Team leaderboard
        team_marvel_points = sum(u['total_points'] for u in users_data if u['team_name'] == 'Team Marvel')
        team_dc_points = sum(u['total_points'] for u in users_data if u['team_name'] == 'Team DC')
        
        teams_sorted = [
            {'team_id': str(team_dc_id), 'team_name': 'Team DC', 'total_points': team_dc_points},
            {'team_id': str(team_marvel_id), 'team_name': 'Team Marvel', 'total_points': team_marvel_points}
        ]
        teams_sorted.sort(key=lambda x: x['total_points'], reverse=True)
        
        for rank, team in enumerate(teams_sorted, 1):
            leaderboard_data.append({
                'type': 'team',
                'rank': rank,
                'team_id': team['team_id'],
                'team_name': team['team_name'],
                'total_points': team['total_points'],
                'member_count': 5,
                'updated_at': datetime.now().isoformat()
            })
        
        db.leaderboard.insert_many(leaderboard_data)
        
        # Print summary
        self.stdout.write(self.style.SUCCESS('\n=== Database Population Complete ==='))
        self.stdout.write(f'Teams created: {db.teams.count_documents({})}')
        self.stdout.write(f'Users created: {db.users.count_documents({})}')
        self.stdout.write(f'Workouts created: {db.workouts.count_documents({})}')
        self.stdout.write(f'Activities logged: {db.activities.count_documents({})}')
        self.stdout.write(f'Leaderboard entries: {db.leaderboard.count_documents({})}')
        self.stdout.write(self.style.SUCCESS('\n✓ Test data populated successfully!'))
