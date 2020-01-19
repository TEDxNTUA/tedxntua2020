from django.urls import path

from .views import ScheduleView, PresenterView


urlpatterns = [
    path('schedule/', ScheduleView.as_view(), name='schedule'),
    # TODO: Use slugs
    path('presenter/<int:id>', PresenterView.as_view(), name='presenter'),
]
