from django.urls import path

from .views import PresenterView


urlpatterns = [
    path('presenter/<int:id>', PresenterView.as_view(), name='presenter'),
]
