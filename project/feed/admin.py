from django.contrib import admin

from project.utils.admin import PartiallyTranslatableAdmin, render_link_field
from .models import Notification

class NotificationAdmin(PartiallyTranslatableAdmin):
    list_display = ('__str__', 'created_at', 'title')
    # ordering = ['start']

    def link_html(self, obj):
        return render_link_field(obj, 'link', new_tab=True)
    link_html.short_description = ('Link')

admin.site.register(Notification, NotificationAdmin)
# Register your models here.
