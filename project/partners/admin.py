from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from project.utils.admin import PartiallyTranslatableAdmin, render_link_field
from .models import Partner


class PartnerAdmin(PartiallyTranslatableAdmin):
    list_display = ('__str__', 'partner_type', 'link_html', 'is_published')
    list_filter = ('partner_type', 'is_published')
    ordering = ['partner_type']

    def link_html(self, obj):
        return render_link_field(obj, 'link', new_tab=True)
    link_html.short_description = _('Link')


admin.site.register(Partner, PartnerAdmin)
