from django.views.generic import TemplateView
from django.shortcuts import render

from project.program.models import Presenter


class HomeView(TemplateView):
    template_name = 'home/index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
