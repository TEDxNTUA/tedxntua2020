from django.urls import path

from .views import (
    SpeakersView, PerformersView, SideEventsView,
    PresenterView, ScheduleView,
)


urlpatterns = [
    path('speakers/', SpeakersView.as_view(), name='speakers'),
    path('performers/', PerformersView.as_view(), name='performers'),
    path('side-events/', SideEventsView.as_view(), name='side-events'),
    path('event/<slug:slug>', PresenterView.as_view(), name='presenter'),
    path('schedule/', ScheduleView.as_view(), name='schedule'),
]
