from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from project.partners.models import Partner
from project.program.models import Activity, Presenter
from project.team.models import TeamMember


PERMISSIONS = ['view', 'edit', 'add', 'delete']
GROUP_MODEL_PERMISSIONS = {
    TeamMember.EXPERIENCE: [Activity, Presenter],
    TeamMember.FUNDRAISING: [Partner],
    TeamMember.GRAPHICS: [],
    TeamMember.MEDIA: [Partner, Activity, Presenter],
    TeamMember.SPEAKERS: [Presenter, Activity],
    TeamMember.VENUE_PRODUCTION: [],
}

class Command(BaseCommand):
    help = 'Create group permissions.'

    def handle(self, *args, **kwargs):
        for group, models in GROUP_MODEL_PERMISSIONS.items():
            new_group, _ = Group.objects.get_or_create(name=group)
            for model in models:
                ct = ContentType.objects.get_for_model(model)
                for permission in PERMISSIONS:
                    name = f'Can {permission} {model._meta.verbose_name_plural}'
                    model_add_perm, _ = Permission.objects.get_or_create(
                        name=name,
                        content_type=ct,
                    )
                    new_group.permissions.add(model_add_perm)
