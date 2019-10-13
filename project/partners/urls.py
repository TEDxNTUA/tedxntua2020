from django.urls import path

from .views import PartnersView


urlpatterns = [
    path('', PartnersView.as_view(), name='partners'),
]
