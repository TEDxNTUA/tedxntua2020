from django.shortcuts import render
from django.views import View


class AboutView(View):
    template_name = 'about/index{}.html'

    def get(self, request):
        version = request.GET.get('v', 'A')
        return render(request, self.template_name.format(version), {})
