import getpass

from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand

from project.team.models import TeamMember


class Command(BaseCommand):
    help = 'Create user.'

    def add_arguments(self, parser):
        parser.add_argument('name', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('team', type=str)

    def handle(self, *args, **kwargs):
        name = kwargs['name']
        email = kwargs['email']
        team = kwargs['team']
        password = getpass.getpass()
        if team == TeamMember.IT:
            User.objects.create_superuser(name, email, password)
        else:
            user = User.objects.create_user(name, email, password)
            user.is_staff = True
            user.save()
            group = Group.objects.get(name=team)
            group.user_set.add(user)
