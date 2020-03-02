from django.conf import settings
from django.views.generic import TemplateView
from django.shortcuts import render

from project.program.models import Presenter, Activity


class HomeView(TemplateView):
    template_name = 'home/index.html'

    def get(self, request, *args, **kwargs):
        speakers = Presenter.speakers.all()
        performers = Presenter.performers.all()
        side_events = Activity.side_events.select_related('presenter').all()
        lineup = {
            'speakers': speakers,
            'performers': performers,
            'side_events': side_events,
        }
        return render(request, self.template_name, {
            'lineup': lineup,
            'placeholders': list(range(4)),
            'event_date': settings.TEDXNTUA_DATE,
        })
