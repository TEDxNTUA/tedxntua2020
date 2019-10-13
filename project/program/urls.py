from django.urls import path

from .views import SpeakersView


urlpatterns = [
    path('', SpeakersView.as_view(), name='speakers'),
]
