from django.contrib import admin
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html_join

from project.utils.admin import PartiallyTranslatableAdmin, render_link_field
from ..models import Activity
from ..forms import PresenterModelForm


class PresenterAdmin(PartiallyTranslatableAdmin):
    form = PresenterModelForm
    list_display = ('__str__', 'slug', 'occupation', 'link_html', 'activity_list', 'is_published')
    list_filter = ('activity__activity_type', 'is_published')

    def link_html(self, obj):
        return render_link_field(obj, 'link', new_tab=True)
    link_html.short_description = _('Link')

    def activity_list(self, obj):
        '''
        Creates list of links for change view of presenter's activities.
        '''
        return format_html_join(', ', '<a href="{}">{}</a>', (
            (
                reverse('admin:program_activity_change', args=[activity.id]),
                activity,
            ) for activity in obj.activity_set.all()
        ))
    activity_list.short_description = _('Activities')

    def save_related(self, request, form, formsets, change):
        '''
        If create_empty_activity is set, it creates an empty
        and unpublished activity of given type, with the same
        image as of the presenter's and assigns it to the
        presenter.

        The save_related has to be used since we are interfering
        with a many-to-many relationship. It is called after
        save_form and save_model.

        Resources:
        https://timonweb.com/posts/many-to-many-field-save-method-and-the-django-admin/
        '''
        super().save_related(request, form, formsets, change)

        activity_type = form.cleaned_data.get('create_empty_activity', '')
        if activity_type:
            presenter = form.instance
            # Make empty unpublished activity
            a = Activity.objects.make_empty(
                activity_type=activity_type,
                is_published=False,
            )
            # Get image from presenter
            if presenter.image:
                a.image.name = presenter.image.name
            a.save()
            # Assign activity to presenter
            presenter.activity_set.add(a)
