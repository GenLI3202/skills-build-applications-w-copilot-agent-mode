from django.core.management.base import BaseCommand
from users.models import User, UserProfile
from teams.models import Team, TeamMembership
from activities.models import ActivityType, Activity
from leaderboards.models import Leaderboard, LeaderboardEntry, Achievement, UserAchievement
from django.db import transaction

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        with transaction.atomic():
            # Clear existing data
            UserAchievement.objects.all().delete()
            LeaderboardEntry.objects.all().delete()
            Leaderboard.objects.all().delete()
            Achievement.objects.all().delete()
            Activity.objects.all().delete()
            ActivityType.objects.all().delete()
            TeamMembership.objects.all().delete()
            Team.objects.all().delete()
            UserProfile.objects.all().delete()
            User.objects.all().delete()

            # Create teams
            marvel = Team.objects.create(name='Marvel', description='Marvel Superheroes', captain_id=1, max_members=10, is_public=True, team_code='MARVEL', total_points=0)
            dc = Team.objects.create(name='DC', description='DC Superheroes', captain_id=2, max_members=10, is_public=True, team_code='DC', total_points=0)

            # Create users (superheroes)
            heroes = [
                {'username': 'ironman', 'email': 'ironman@marvel.com', 'first_name': 'Tony', 'last_name': 'Stark', 'fitness_level': 'advanced', 'team': marvel},
                {'username': 'spiderman', 'email': 'spiderman@marvel.com', 'first_name': 'Peter', 'last_name': 'Parker', 'fitness_level': 'intermediate', 'team': marvel},
                {'username': 'captainamerica', 'email': 'cap@marvel.com', 'first_name': 'Steve', 'last_name': 'Rogers', 'fitness_level': 'advanced', 'team': marvel},
                {'username': 'batman', 'email': 'batman@dc.com', 'first_name': 'Bruce', 'last_name': 'Wayne', 'fitness_level': 'advanced', 'team': dc},
                {'username': 'wonderwoman', 'email': 'wonderwoman@dc.com', 'first_name': 'Diana', 'last_name': 'Prince', 'fitness_level': 'advanced', 'team': dc},
                {'username': 'flash', 'email': 'flash@dc.com', 'first_name': 'Barry', 'last_name': 'Allen', 'fitness_level': 'intermediate', 'team': dc},
            ]
            user_objs = []
            for idx, hero in enumerate(heroes, start=1):
                user = User.objects.create(
                    username=hero['username'],
                    email=hero['email'],
                    first_name=hero['first_name'],
                    last_name=hero['last_name'],
                    fitness_level=hero['fitness_level'],
                    password='testpassword',
                )
                UserProfile.objects.create(user_id=user.id, bio=f"{hero['first_name']} {hero['last_name']} is a superhero.", total_points=0)
                TeamMembership.objects.create(team_id=hero['team']._id, user_id=user.id, role='member', points_contributed=0)
                user_objs.append(user)

            # Create activity types
            run = ActivityType.objects.create(name='Running', description='Run fast!', points_per_minute=10, category='cardio')
            lift = ActivityType.objects.create(name='Weight Lifting', description='Lift weights!', points_per_minute=8, category='strength')

            # Create activities for each user
            for user in user_objs:
                Activity.objects.create(user_id=user.id, activity_type_id=run.id, duration_minutes=30, intensity='high', calories_burned=400, notes='Morning run', date_logged='2025-09-15', points_earned=300)
                Activity.objects.create(user_id=user.id, activity_type_id=lift.id, duration_minutes=45, intensity='moderate', calories_burned=350, notes='Gym session', date_logged='2025-09-15', points_earned=360)

            # Create leaderboard and entries
            leaderboard = Leaderboard.objects.create(name='Superhero Leaderboard', description='Top superheroes', leaderboard_type='weekly', category='individual', is_active=True)
            for idx, user in enumerate(user_objs, start=1):
                LeaderboardEntry.objects.create(leaderboard_id=leaderboard._id, participant_id=user.id, participant_type='user', score=idx*100, rank=idx)

            # Create achievements
            achievement = Achievement.objects.create(name='First Workout', description='Completed first workout', icon_url='', criteria={'workouts': 1}, points_reward=50, achievement_type='milestone', is_active=True)
            for user in user_objs:
                UserAchievement.objects.create(user_id=user.id, achievement_id=str(achievement._id), earned_at='2025-09-15', progress_data={'workouts': 1})

            self.stdout.write(self.style.SUCCESS('Test data populated successfully!'))
