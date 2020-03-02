from django.conf import settings
from django.views.generic import TemplateView
from django.shortcuts import render

from project.program.models import Presenter, Activity


class HomeView(TemplateView):
    template_name = 'home/index.html'

    def get(self, request, *args, **kwargs):
        qs = {
            'speakers': Presenter.speakers,
            'performers': Presenter.performers,
            'side_events': Activity.side_events,
        }
        for key in qs:
            if settings.TEDXNTUA_SHOW_UNPUBLISHED:
                qs[key] = qs[key].all()
            else:
                qs[key] = qs[key].published()

        qs['side_events'] = qs['side_events'].select_related('presenter')

        return render(request, self.template_name, {
            'lineup': qs,
            'placeholders': list(range(4)),
            'event_date': settings.TEDXNTUA_DATE,
        })
