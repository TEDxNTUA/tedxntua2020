from django.conf import settings
from django.shortcuts import render
from django.views import View

from project.team.models import TeamMember


class AboutView(View):
    template_name = 'about/index.html'

    def get(self, request):
        if settings.TEDXNTUA_SHOW_UNPUBLISHED:
            members = TeamMember.objects.all()
        else:
            members = TeamMember.objects.published()

        return render(request, self.template_name, {
            'members': members,
        })
