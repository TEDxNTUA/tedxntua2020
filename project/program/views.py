from django.shortcuts import render, get_object_or_404
from django.views import View

from .models import Presenter, Activity, Stage


class ScheduleView(View):
    template_name = 'program/schedule.html'

    def get(self, request):
        schedule = Activity.objects.get_schedule()
        stages = Stage.get_verbose_names()
        return render(request, self.template_name, {
            'schedule': schedule,
            'stages': stages,
        })

class PresenterView(View):
    template_name = 'program/presenter.html'

    def get(self, request, slug):
        presenter = get_object_or_404(Presenter, slug=slug)
        return render(request, self.template_name,{
            'presenter': presenter,
        })
