from django.conf import settings
from django.shortcuts import render
from django.views import View

from .models import Partner


class PartnersView(View):
    template = 'partners/index.html'

    def get(self, request, *args, **kwargs):
        partners = Partner.objects.get_partners_by_type(
            unpublished=settings.TEDXNTUA_SHOW_UNPUBLISHED,
        )
        return render(request, self.template, {'partners': partners})
