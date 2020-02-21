from django.shortcuts import render
from django.views import View

class FeedView(View):
    template = 'feed/index.html'

    def get(self, request):
        return render(request, self.template)

# Create your views here.
