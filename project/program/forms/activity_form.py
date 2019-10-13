from django import forms
from django.utils.translation import ugettext_lazy as _
from parler.admin import TranslatableModelForm

from ..models import Activity


class ActivityModelForm(TranslatableModelForm):
    '''
    Custom admin form for Activities.

    Adds the option to get activity image from presenter and sets field order.
    '''

    get_image_from_presenter = forms.BooleanField(
        required=False,
        label=_('Get image from presenter'),
        help_text=_('If selected, the image will be overridden by that of the first presenter'),
    )

    class Meta:
        model = Activity
        fields = (
            'activity_type',
            'is_published',
            'start',
            'end',
            'image',
            'get_image_from_presenter',
            'presenters',
            'title',
            'subtitle',
            'description',
        )

    def save(self, commit=True):
        '''
        Handles form save and get_image_from_presenter toggle.

        Useful links:
        https://docs.djangoproject.com/en/<VAR:DJANGO_VERSION>/topics/forms/modelforms/#the-save-method
        https://stackoverflow.com/a/817364/11114199
        '''
        obj = super().save(commit=False)

        get_im = self.cleaned_data.get('get_image_from_presenter', False)
        presenters = self.cleaned_data.get('presenters', None)
        if get_im and presenters:
            presenter = presenters.first()
            # Set image field to point to first presenter's image
            if presenter.image:
                obj.image.name = presenter.image.name

        if commit:
            obj.save()
            self.save_m2m()

        return obj
