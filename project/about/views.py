from django.shortcuts import render
from django.views import View

from project.team.models import TeamMember


class AboutView(View):
    template_name = 'about/index.html'

    def get(self, request):
        members = TeamMember.objects.all()
        return render(request, self.template_name, {
            'members': members,
        })
