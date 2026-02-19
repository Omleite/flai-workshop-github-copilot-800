from djongo import models


class User(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    team_id = models.CharField(max_length=100, blank=True, null=True)
    team_name = models.CharField(max_length=200, blank=True, null=True)
    avatar = models.URLField(blank=True, null=True)
    total_points = models.IntegerField(default=0)
    created_at = models.CharField(max_length=100)

    class Meta:
        db_table = 'users'
        
    def __str__(self):
        return self.name


class Team(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_at = models.CharField(max_length=100)
    members = models.JSONField(default=list)

    class Meta:
        db_table = 'teams'
        
    def __str__(self):
        return self.name


class Activity(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    user_id = models.CharField(max_length=100)
    user_name = models.CharField(max_length=200)
    user_email = models.EmailField()
    activity_type = models.CharField(max_length=100)
    duration_minutes = models.IntegerField()
    distance_km = models.FloatField(default=0.0)
    calories_burned = models.IntegerField(default=0)
    points_earned = models.IntegerField(default=0)
    date = models.CharField(max_length=100)
    created_at = models.CharField(max_length=100)

    class Meta:
        db_table = 'activities'
        
    def __str__(self):
        return f"{self.user_name} - {self.activity_type}"


class Leaderboard(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    type = models.CharField(max_length=50)  # 'individual' or 'team'
    rank = models.IntegerField()
    
    # For individual entries
    user_id = models.CharField(max_length=100, blank=True, null=True)
    user_name = models.CharField(max_length=200, blank=True, null=True)
    user_email = models.EmailField(blank=True, null=True)
    team_name = models.CharField(max_length=200, blank=True, null=True)
    
    # For team entries
    team_id = models.CharField(max_length=100, blank=True, null=True)
    member_count = models.IntegerField(blank=True, null=True)
    
    # Common fields
    total_points = models.IntegerField(default=0)
    updated_at = models.CharField(max_length=100)

    class Meta:
        db_table = 'leaderboard'
        ordering = ['rank']
        
    def __str__(self):
        if self.type == 'individual':
            return f"#{self.rank} - {self.user_name}"
        return f"#{self.rank} - {self.team_name}"


class Workout(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    duration_minutes = models.IntegerField()
    difficulty = models.CharField(max_length=50)
    exercises = models.JSONField(default=list)
    points_value = models.IntegerField(default=0)
    created_at = models.CharField(max_length=100)

    class Meta:
        db_table = 'workouts'
        
    def __str__(self):
        return self.name
