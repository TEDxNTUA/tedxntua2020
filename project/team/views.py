from django.shortcuts import render
from django.views import View

from .models import TeamMember


class TeamView(View):
    template_name = 'team/index.html'

    def get(self, request):
        teams = TeamMember.objects.get_teams()
        return render(request, self.template_name, {'teams': teams})
