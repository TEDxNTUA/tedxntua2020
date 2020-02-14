from django.shortcuts import render, get_object_or_404
from django.views import View

from .models import Presenter, Activity, Stage


class SpeakersView(View):
    template_name = 'program/speakers.html'

    def get(self, request):
        speakers = Presenter.speakers.all()
        return render(request, self.template_name, {'speakers': speakers})

class PerformersView(View):
    template_name = 'program/performers.html'

    def get(self, request):
        performers = Presenter.performers.all()
        return render(request, self.template_name, {'performers': performers})

class SideEventsView(View):
    template_name = 'program/side_events.html'

    def get(self, request):
        side_events = Activity.side_events.all()
        return render(request, self.template_name, {'side_events': side_events})

class PresenterView(View):
    template_name = 'program/presenter.html'

    def get(self, request, slug):
        presenter = get_object_or_404(Presenter, slug=slug)
        return render(request, self.template_name, {
            'presenter': presenter,
        })

class ScheduleView(View):
    template_name = 'program/schedule.html'

    def get(self, request):
        schedule = Activity.objects.get_schedule()
        stages = Stage.get_verbose_names()
        return render(request, self.template_name, {
            'schedule': schedule,
            'stages': stages,
        })
