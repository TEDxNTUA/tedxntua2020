from django.shortcuts import render
from django.views import View


class AboutView(View):
    template_name = 'about/index.html'

    def get(self, request):
        return render(request, self.template_name, {})
