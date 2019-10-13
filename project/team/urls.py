from django.urls import path

from .views import TeamView


urlpatterns = [
    path('', TeamView.as_view(), name='team'),
]
