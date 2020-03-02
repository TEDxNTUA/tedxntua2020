from collections import OrderedDict
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.dispatch import receiver
from versatileimagefield.fields import VersatileImageField
from versatileimagefield.image_warmer import VersatileImageFieldWarmer
from parler.models import TranslatableModel, TranslatedFields
from parler.managers import TranslatableManager


class PartnerManager(TranslatableManager):
    def get_partners_by_type(self, unpublished=False):
        '''
        Table-level method to get all partners grouped by type.

        Parameters
        ----------
        unpublished : bool (default False)
            Controls if unpublished partners are included.

        Returns
        -------
        directory : dict
            A dictionary where partner types from Partner.PARTNER_TYPES
            are the keys and the value is a dictionary with the `title` of
            the team and a `items` array.
            The order of partner types is the same as in PARTNER_TYPES.
        '''
        partners = OrderedDict()
        for type_, title in Partner.PARTNER_TYPES:
            partners[type_] = {
                'title': title,
                'items': [],
            }

        qs = self.get_queryset()
        if not unpublished:
            qs = qs.filter(is_published=True)

        for item in qs:
            partners[item.partner_type]['items'].append(item)
        return partners


class Partner(TranslatableModel):
    '''Model for partners of the TEDxNTUA organization.

    The `partner_type` attribute is represented as a CharField with limited possible
    values. The definition follows the official documentation example:
    https://docs.djangoproject.com/en/2.2/ref/models/fields/#choices

    The `link` attribute is represented as a URLField. The definition follows
    the official documentation example:
    https://docs.djangoproject.com/en/2.2/ref/models/fields/#urlfield
    '''
    PLATINUM_SPONSORS = 'PS'
    GRAND_SPONSORS = 'GS'
    GRAND_CARRIER_SPONSORS = 'GCS'
    GRAND_HOSPITALITY_SPONSORS = 'GHS'
    SPONSORS = 'SPO'
    SUPPORTERS = 'SUP'
    MEDIA_PARTNERS = 'MP'
    COMMUNITY_PARTNERS = 'CP'
    PARTNER_TYPES = (
        (PLATINUM_SPONSORS, _('Platinum Sponsor')),
        (GRAND_SPONSORS, _('Grand Sponsors')),
        (GRAND_CARRIER_SPONSORS, _('Grand Carrier Sponsors')),
        (GRAND_HOSPITALITY_SPONSORS, _('Grand Hospitality Sponsors')),
        (SPONSORS, _('Sponsors')),
        (SUPPORTERS, _('Supporters')),
        (MEDIA_PARTNERS, _('Media Partners')),
        (COMMUNITY_PARTNERS, _('Community Partners')),
    )
    translations = TranslatedFields(
        name=models.CharField(max_length=255, verbose_name='name')
    )
    partner_type = models.CharField(max_length=3, choices=PARTNER_TYPES)
    link = models.URLField()

    image = VersatileImageField(
        'Image',
        upload_to='partners/',
        width_field='image_width',
        height_field='image_height'
    )
    image_height = models.PositiveIntegerField(editable=False, null=True)
    image_width = models.PositiveIntegerField(editable=False, null=True)

    is_published = models.BooleanField(_('Published'), default=True)

    leaflet = models.FileField(
        upload_to='partners/leaflet/',
        null=True,
        blank=True,
    )

    objects = PartnerManager()

    def __str__(self):
        return self.name

@receiver(models.signals.post_save, sender=Partner)
def warm_partner_images(sender, instance, **kwargs):
    '''Ensures images are created post-save.
    Image sizes are stored in base.VERSATILEIMAGEFIELD_RENDITION_KEY_SETS.
    Using a thumbnail__AxA rendition key, the image fits in a AxA rectangle by
    maintaining the aspect ratio.

    Documentation link:
    https://django-versatileimagefield.readthedocs.io/en/latest/overview.html#create-images-wherever-you-need-them
    '''

    img_warmer = VersatileImageFieldWarmer(
        instance_or_queryset=instance,
        rendition_key_set='Sizes',
        image_attr='image',
        verbose=True
    )
    num_created, failed_to_create = img_warmer.warm()
