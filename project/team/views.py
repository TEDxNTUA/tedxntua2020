from django.shortcuts import render
from django.views import View

from .models import TeamMember


class TeamView(View):
    def get(self, request):
        version = request.GET['v']
        teams = TeamMember.objects.get_teams()
        return render(request, 'team/index' + version + '.html', {'teams': teams})
