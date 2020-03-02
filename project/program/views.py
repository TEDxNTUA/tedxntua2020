from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.views import View

from .models import Presenter, Activity, Stage
from project.utils.url import is_url_same_domain


class SpeakersView(View):
    template_name = 'program/listing.html'

    def get(self, request):
        if settings.TEDXNTUA_SHOW_UNPUBLISHED:
            items = Presenter.speakers.all()
        else:
            items = Presenter.speakers.published()

        return render(request, self.template_name, {
            'listing_type': 'speakers',
            'items': items,
            'placeholders': list(range(4)),
        })

class PerformersView(View):
    template_name = 'program/listing.html'

    def get(self, request):
        if settings.TEDXNTUA_SHOW_UNPUBLISHED:
            items = Presenter.performers.all()
        else:
            items = Presenter.speakers.published()

        return render(request, self.template_name, {
            'listing_type': 'performers',
            'items': items,
            'placeholders': list(range(4)),
        })

class SideEventsView(View):
    template_name = 'program/listing.html'

    def get(self, request):
        # Side events view is special in that the listing shows the *activities*
        # instead of their presenters
        if settings.TEDXNTUA_SHOW_UNPUBLISHED:
            items = Activity.side_events.select_related('presenter')
        else:
            items = Activity.side_events.published().select_related('presenter')

        return render(request, self.template_name, {
            'listing_type': 'side_events',
            'items': items,
            'placeholders': list(range(4)),
        })


class PresenterView(View):
    template_name = 'program/presenter.html'

    def get(self, request, slug):
        # Add link to previous page if it was on the same domain
        go_back_url = request.META.get('HTTP_REFERER')
        if not is_url_same_domain(request, go_back_url):
            go_back_url = ''

        filter_dict = {}
        if not settings.TEDXNTUA_SHOW_UNPUBLISHED:
            filter_dict = {'is_published': True}

        presenter = get_object_or_404(Presenter, slug=slug, **filter_dict)
        return render(request, self.template_name, {
            'presenter': presenter,
            'go_back_url': go_back_url,
        })

class ScheduleView(View):
    template_name = 'program/schedule.html'

    def get(self, request):
        schedule = Activity.objects.get_schedule(
            unpublished=settings.TEDXNTUA_SHOW_UNPUBLISHED,
        )
        stages = Stage.get_verbose_names()
        return render(request, self.template_name, {
            'schedule': schedule,
            'stages': stages,
        })
