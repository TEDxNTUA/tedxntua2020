from django.shortcuts import render, get_object_or_404
from django.views import View

from .models import Presenter, Activity, Stage


class SpeakersView(View):
    template_name = 'program/listing.html'

    def get(self, request):
        items = Presenter.speakers.all()
        return render(request, self.template_name, {
            'listing_type': 'speakers',
            'items': items,
        })

class PerformersView(View):
    template_name = 'program/listing.html'

    def get(self, request):
        items = Presenter.performers.all()
        return render(request, self.template_name, {
            'listing_type': 'performers',
            'items': items,
        })

class SideEventsView(View):
    template_name = 'program/listing.html'

    def get(self, request):
        # Side events view is special in that the listing shows the *activities*
        # instead of their presenters
        items = Activity.side_events.select_related('presenter').all()
        return render(request, self.template_name, {
            'listing_type': 'side_events',
            'items': items,
        })


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
