from django.urls import path

from .views import SpeakersView, PresenterView, ScheduleView


urlpatterns = [
    path('speakers/', SpeakersView.as_view(), name='speakers'),
    path('presenter/<int:id>', PresenterView.as_view(), name='presenter'),
    path('schedule/', ScheduleView.as_view(), name='schedule'),
]
