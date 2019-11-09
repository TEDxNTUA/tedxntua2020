from django import forms
from django.utils.translation import ugettext_lazy as _
from parler.admin import TranslatableModelForm

from ..models import Activity, Presenter


CREATE_ACTIVITY_CHOICES = (
    ('', _('No')), # Add No as option
) + Activity.TYPE_CHOICES

class PresenterModelForm(TranslatableModelForm):
    '''
    Custom admin form for Presenters.

    Adds the option to create empty unpublished activity of given type.
    '''

    create_empty_activity = forms.ChoiceField(
        required=False,
        label=_('Assign empty activity'),
        help_text=_('This will create an empty and unpublished '
                    'activity of the given type with the same '
                    'photo as the presenter\'s'),
        choices=CREATE_ACTIVITY_CHOICES,
    )

    class Meta:
        model = Presenter
        fields = (
            'name',
            'occupation',
            'short_bio',
            'quote',
            'image',
            'link',
            'create_empty_activity',
            'is_published',
        )
