from django.shortcuts import render
from django.views import View

from .models import Presenter, Activity, Stage


class SpeakersView(View):
    template_name = 'program/speakers.html'

    def get(self, request, *args, **kwargs):
        speakers = Presenter.objects.get_speakers()
        hosts = Presenter.objects.get_hosts()
        return render(request, self.template_name, {
            'speakers': speakers,
            'hosts': hosts,
        })


class PresenterView(View):
    template_name = 'program/speaker.html'

    def get(self, request, *args, **kwargs):
        try:
            presenter = Presenter.objects.get(id=kwargs['id'])
            return render(request, self.template_name, {
                'presenter': presenter,
            })
        except Presenter.DoesNotExist:
            # TODO
            pass


class ScheduleView(View):
    template_name = 'program/schedule.html'

    def get(self, request):
        schedule = Activity.objects.get_schedule()
        stages = Stage.get_verbose_names()
        return render(request, self.template_name, {
            'schedule': schedule,
            'stages': stages,
            'day': '<VAR:EVENT_DATE>',
        })
