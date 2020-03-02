from django.db import models
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from parler.models import TranslatableModel, TranslatedFields
from parler.managers import TranslatableManager
from versatileimagefield.fields import VersatileImageField
from versatileimagefield.image_warmer import VersatileImageFieldWarmer


class TeamMemberManager(TranslatableManager):
    def get_teams(self, unpublished=False):
        '''
        Table-level method to get all team members grouped by team.

        Parameters
        ----------
        unpublished : bool (default False)
            Controls if unpublished team members are included.

        Returns
        -------
        directory : dict
            A dictionary where team IDs from TeamMember.TEAM_CHOICES
            are the keys and the value is a dictionary with the `title` of
            the team and a `members` array.

            The order of teams is the same as in TEAM_CHOICES.
        '''
        teams = {}
        for team_id, title in TeamMember.TEAM_CHOICES:
            teams[team_id] = {
                'title': title,
                'members': [],
            }

        qs = self.get_queryset()
        if not unpublished:
            qs = qs.filter(is_published=True)

        for member in qs:
            teams[member.team]['members'].append(member)
        return teams

    def published(self):
        return self.get_queryset().filter(is_published=True)


class TeamMember(TranslatableModel):
    '''
    Model for members of the TEDxNTUA organizing team.

    The `team` attribute is represented as a CharField with limited possible
    values. The definition follows the official documentation example:
    https://docs.djangoproject.com/en/2.2/ref/models/fields/#choices
    '''
    EXPERIENCE = 'experience'
    IT = 'it'
    FUNDRAISING = 'fundraising'
    GRAPHICS = 'graphics'
    MEDIA = 'media'
    SPEAKERS = 'speakers'
    VENUE_PRODUCTION = 'venue-production'
    TEAM_CHOICES = (
        (EXPERIENCE, 'Experience'),
        (IT, 'IT'),
        (FUNDRAISING, 'Fundraising'),
        (GRAPHICS, 'Graphics'),
        (MEDIA, 'Media'),
        (SPEAKERS, 'Speakers'),
        (VENUE_PRODUCTION, 'Venue & Production'),
    )
    translations = TranslatedFields(
        name=models.CharField(max_length=255, default='')
    )
    email = models.EmailField()
    team = models.CharField(max_length=16, choices=TEAM_CHOICES)

    image = VersatileImageField(
        'Image 1',
        upload_to='team/',
        width_field='image_width',
        height_field='image_height',
        null=True,
        blank=True,
    )
    image_height = models.PositiveIntegerField(editable=False, null=True)
    image_width = models.PositiveIntegerField(editable=False, null=True)

    image_alt = VersatileImageField(
        'Image 2',
        upload_to='team/',
        width_field='image_alt_width',
        height_field='image_alt_height',
        null=True,
        blank=True,
    )
    image_alt_height = models.PositiveIntegerField(editable=False, null=True)
    image_alt_width = models.PositiveIntegerField(editable=False, null=True)

    is_published = models.BooleanField(_('Published'), default=True)

    objects = TeamMemberManager()

    def __str__(self):
        '''
        Objects of the TeamMember class are represented as strings by
        their fullname property
        '''
        return self.name


@receiver(models.signals.post_save, sender=TeamMember)
def warm_team_member_images(sender, instance, **kwargs):
    '''
    Ensures images are created post-save.
    Image sizes are stored in base.VERSATILEIMAGEFIELD_RENDITION_KEY_SETS.
    Using a thumbnail__AxA rendition key, the image fits in a AxA rectangle by
    maintaining the aspect ratio.

    Documentation link:
    https://django-versatileimagefield.readthedocs.io/en/latest/overview.html#create-images-wherever-you-need-them
    '''

    for field in ['image', 'image_alt']:
        img_warmer = VersatileImageFieldWarmer(
            instance_or_queryset=instance,
            rendition_key_set='Sizes',
            image_attr=field,
            verbose=True
        )
        img_warmer.warm()
