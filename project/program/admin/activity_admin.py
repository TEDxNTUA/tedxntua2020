from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html

from project.utils.admin import PartiallyTranslatableAdmin
from ..models import Activity
from ..forms import ActivityModelForm


class ActivityAdmin(PartiallyTranslatableAdmin):
    form = ActivityModelForm
    list_display = ('__str__', 'activity_type', 'presenter_link', 'start_time', 'end_time', 'is_published')
    list_filter = ('activity_type', 'is_published')
    ordering = ['start']

    def presenter_link(self, obj):
        '''
        Creates link for change view of activity's presenter.
        '''
        if not obj.presenter:
            return '-'
        return format_html('<a href="{}">{}</a>',
            reverse('admin:program_presenter_change', args=[obj.presenter.id]),
            obj.presenter,
        )
    presenter_link.short_description = _('Presenter')
