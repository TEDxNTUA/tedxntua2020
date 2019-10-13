from django.contrib import admin

from ..models import Activity, Presenter
from .activity_admin import ActivityAdmin
from .presenter_admin import PresenterAdmin


admin.site.register(Presenter, PresenterAdmin)
admin.site.register(Activity, ActivityAdmin)
