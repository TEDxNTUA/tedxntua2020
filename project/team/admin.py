from django.contrib import admin

from project.utils.admin import PartiallyTranslatableAdmin
from .models import TeamMember


class TeamMemberAdmin(PartiallyTranslatableAdmin):
    list_display = ('__str__', 'team', 'email', 'is_published')
    list_filter = ('team', 'is_published')


admin.site.register(TeamMember, TeamMemberAdmin)
