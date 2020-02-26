from django.db import models
import datetime

from parler.models import TranslatableModel, TranslatedFields, TranslationDoesNotExist
from parler.managers import TranslatableQuerySet, TranslatableManager

class ActivityTypeManager(TranslatableManager):
    def get_queryset(self):
        return super().get_queryset().filter(
            is_published=True,
        )

class Notification(TranslatableModel):

    # GENERAL = 'G'
    # TALK = 'T'
    # PERFORMANCE = 'P'
    # SIDE_EVENT = 'S'
    # HOSTING = 'H'
    # SPONSOR = 'SP'
    # TYPE_CHOICES = (
    #     (GENERAL, _('General')),
    #     (TALK, _('Talk')),
    #     (PERFORMANCE, _('Performance')),
    #     (SIDE_EVENT, _('Side event')),
    #     (HOSTING, _('Hosting')),
    #     (SPONSOR, _('Sponsor')),
    # )

    # message_type = models.CharField(max_length=1, choices=TYPE_CHOICES,
    #                                  verbose_name='Type')

    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    translations = TranslatedFields(
        title=models.CharField(max_length=255),
        message=models.TextField(),
    )

    # is_published = models.BooleanField(_('Published'), default=True)

    # user_id = models.ForeignKey(
    #     'User',
    #     null=True,
    #     on_delete=models.SET_NULL,
    # )

# Create your models here.
