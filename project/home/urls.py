from django.urls import path

from .views import HomeView, UIDemoView


urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('uidemo', UIDemoView.as_view(), name='ui-demo'),
]
