'''project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/<VAR:DJANGO_VERSION>/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
'''
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import RedirectView
from django.utils.translation import ugettext_lazy as _


urlpatterns = [
    path('', include('project.home.urls')),
    path('', include('django.conf.urls.i18n')),
    path('schedule/', include('project.program.schedule_urls')),
    path('speakers/', include('project.program.urls')),
    path('partners/', include('project.partners.urls')),
    path('team/', include('project.team.urls')),
    path('about/', include('project.about.urls')),
    path('tickets/', RedirectView.as_view(url='<VAR:TICKETS_URL>'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
)

admin.site.site_header = _('TEDxNTUA <VAR:YEAR> administration')
admin.site.site_title = _('TEDxNTUA <VAR:YEAR> admin')
