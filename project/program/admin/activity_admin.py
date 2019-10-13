from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html_join

from project.utils.admin import PartiallyTranslatableAdmin
from ..models import Activity
from ..forms import ActivityModelForm


class ActivityAdmin(PartiallyTranslatableAdmin):
    form = ActivityModelForm
    list_display = ('__str__', 'activity_type', 'presenter_list', 'start_time', 'end_time', 'is_published')
    list_filter = ('activity_type', 'is_published')
    ordering = ['start']

    def presenter_list(self, obj):
        '''
        Creates list of links for change view of activity's presenters.
        '''
        return format_html_join(', ', '<a href="{}">{}</a>', (
            (
                reverse('admin:program_presenter_change', args=[presenter.id]),
                presenter,
            ) for presenter in obj.presenters.all()
        ))
    presenter_list.short_description = _('Presenters')
