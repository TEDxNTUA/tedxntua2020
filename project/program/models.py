'''
Models for the "Program" section of the website.

The event consists of Activities presented by Presenters, where each activity
happens on one of the three stages: Main event, Performances, Side events.

In this module you'll find:
- Django models for each entity.
- Post-save signal receivers that generate thumbnails for each entry's image.
- Helper managers for queries like "get all presenters who are speakers".
- The `get_schedule` method of the ActivityManager. It gets all the activities
  and organizes them by start time and stage in order to produce the schedule
  that will be consumed by the ScheduleView.
'''
from enum import Enum
import logging

from django.core.exceptions import ValidationError
from django.db import models
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from versatileimagefield.fields import VersatileImageField
from versatileimagefield.image_warmer import VersatileImageFieldWarmer
from parler.models import TranslatableModel, TranslatedFields
from parler.managers import TranslatableQuerySet, TranslatableManager


logger = logging.getLogger(__name__)

# Stage non-database model

class Stage(Enum):
    '''Enum class that represents the event stages'''
    MAIN = 'main'
    PERFORMANCE = 'performance'
    SIDE = 'side'

    @classmethod
    def get_verbose_names(cls):
        '''The stage labels that will be shown in the schedule page'''
        return {
            cls.MAIN.value: _('Main stage'),
            cls.PERFORMANCE.value: _('Performances'),
            cls.SIDE.value: _('Side events'),
        }

    @classmethod
    def from_activity(cls, activity):
        '''Maps an activity to the corresponding stage according to activity type'''
        map_to_stage = {
            Activity.GENERAL: cls.MAIN.value,
            Activity.TALK: cls.MAIN.value,
            Activity.PERFORMANCE: cls.PERFORMANCE.value,
            Activity.WORKSHOP: cls.SIDE.value,
        }
        # Return None if activity type is not mapped to any stage
        return map_to_stage.get(activity.activity_type, None)


# Activity model & managers

class ActivityManager(TranslatableManager):
    '''
    The main manager of the Activity model providing class-level functionality.
    '''
    def get_schedule(self):
        '''
        Get the schedule of the event organized by time and stages.

        Generates a dictionary with time (hh:mm format) as keys
        (in ascending order) and the activities starting on each stage at that
        time (or None) as values.

        If two activities start at the same time and stage, only one will be
        returned, since the other will be overridden. This is prevented by the
        clean() method of the Activity model.

        Activities with no start or end time will not be included.

        Example result:
        {
            '11:30': {
                'main': <Activity: Exploring space (Talk)>,
                'performance': None,
                'side': None
            },
            '12:20': {
                'main': None,
                'performance': <Activity: Banjo session (Performance)>,
                'side': <Activity: Labyrinth of Senses (Workshop)>
            },
            ...
        }
        '''

        slots = {}
        # Initialize each line to contain None for each stage
        blank_line = {stage.value: None for stage in Stage}

        activities = Activity.objects.filter(
            is_published=True,
            start__isnull=False,
            end__isnull=False,
        )

        for activity in activities:
            # Get time slot
            slot = activity.start_time
            # Get stage name
            stage = Stage.from_activity(activity)
            if stage is None:
                continue

            if slot not in slots:
                # If time slot was unused, declare it
                # and initialize it to empty
                slots[slot] = blank_line.copy()
            # Store activity in time slot and in stage column
            slots[slot][stage] = activity

        # Sort by ascending time
        slots = dict(sorted(slots.items()))
        return slots

    def make_empty(self, **other_values):
        '''
        Generates instance with placeholders for the required fields.

        Other values can also be passed as keyword arguments.
        The instance will not be saved to the database.
        '''
        a = self.model(**other_values)
        for lang in ['el', 'en']:
            a.set_current_language(lang)
            for field in ['title', 'subtitle', 'description']:
                setattr(a, field, '-')
        return a


class ActivityTypeManager(TranslatableManager):
    '''
    Abstract class for managers that return activities of specific type,
    e.g. talks, performances, etc.
    '''
    def __init__(self, type_):
        super().__init__()
        self.type_ = type_

    def get_queryset(self):
        return super().get_queryset().filter(
            activity_type=self.type_,
            is_published=True,
        )


class Activity(TranslatableModel):
    '''
    A thing happening in the event, ie. a talk, a performance, a workshop
    or the hosting of the event.
    '''
    GENERAL = 'G'
    TALK = 'T'
    PERFORMANCE = 'P'
    WORKSHOP = 'W'
    HOSTING = 'H'
    TYPE_CHOICES = (
        (GENERAL, _('General')),
        (TALK, _('Talk')),
        (PERFORMANCE, _('Performance')),
        (WORKSHOP, _('Workshop')),
        (HOSTING, _('Hosting')),
    )

    activity_type = models.CharField(max_length=1, choices=TYPE_CHOICES,
                                     verbose_name='Type')

    start = models.TimeField(null=True, blank=True)
    end = models.TimeField(null=True, blank=True)

    translations = TranslatedFields(
        title=models.CharField(max_length=255),
        subtitle=models.TextField(),
        description=models.TextField(),
    )

    image = VersatileImageField(
        'Image',
        upload_to='activities/',
        width_field='image_width',
        height_field='image_height',
        null=True,
        blank=True,
    )
    image_height = models.PositiveIntegerField(editable=False, null=True)
    image_width = models.PositiveIntegerField(editable=False, null=True)

    is_published = models.BooleanField(_('Published'), default=True)

    '''An activity may be presented by many people and a presenter
    may present many activities respectively

    Documentation for many-to-many relationships may be found here:
    https://docs.djangoproject.com/en/<VAR:DJANGO_VERSION>/topics/db/examples/many_to_many/
    '''
    presenters = models.ManyToManyField('Presenter')

    objects = ActivityManager()
    talks = ActivityTypeManager(TALK)
    performances = ActivityTypeManager(PERFORMANCE)
    workshops = ActivityTypeManager(WORKSHOP)

    def __str__(self):
        return self.title

    @property
    def start_time(self):
        if not self.start:
            return None
        return f'{self.start.hour:02d}:{self.start.minute:02d}'

    @property
    def end_time(self):
        if not self.end:
            return None
        return f'{self.end.hour:02d}:{self.end.minute:02d}'

    @property
    def time_span(self):
        if (not self.start) or (not self.end):
            return None
        return f'{self.start_time}-{self.end_time}'

    def clean(self):
        '''Ensures that only one activity starts at a certain time and stage'''
        same_time_activities = Activity.objects.filter(start=self.start)
        for other in same_time_activities:
            if (self.id != other.id
                and Stage.from_activity(self) == Stage.from_activity(other)):
                # If it's not the same activity and they're happening at the same stage
                raise ValidationError('There exists another activity that ' \
                                      'starts at the same time and stage')

    class Meta:
        verbose_name_plural = 'Activities'


@receiver(models.signals.post_save, sender=Activity)
def warm_activity_images(sender, instance, **kwargs):
    '''Ensures images are created post-save.

    Image sizes are stored in base.VERSATILEIMAGEFIELD_RENDITION_KEY_SETS.
    Using a thumbnail__AxA rendition key, the image fits in a AxA rectangle by
    maintaining the aspect ratio.

    Documentation link:
    https://django-versatileimagefield.readthedocs.io/en/latest/overview.html#create-images-wherever-you-need-them
    '''
    if instance.image:
        img_warmer = VersatileImageFieldWarmer(
            instance_or_queryset=instance,
            rendition_key_set='Sizes',
            image_attr='image',
            verbose=True
        )

        img_warmer.warm()
    else:
        logger.info('No image file added for this activity: %s', instance)


class PresenterManager(TranslatableManager):
    '''Class-level functionality'''
    def get_speakers(self):
        '''Returns a list of all speakers with their talk info.

        Unlike the rest of the models file, here we make the assumption
        that each speaker is presenting only a single talk.
        '''
        speakers = self.get_queryset().filter(
            activity__activity_type=Activity.TALK,
            is_published=True,
        ).distinct()
        for speaker in speakers:
            speaker.talk = speaker.activity_set.filter(is_published=True).first()
        return speakers

    def get_hosts(self):
        '''Returns the host of the event'''
        hosts = self.get_queryset().filter(
            activity__activity_type=Activity.HOSTING,
            is_published=True,
        ).distinct()
        return hosts


# Presenter model & managers

class PresenterTypeManager(TranslatableManager):
    '''
    Abstract class for managers that return presenters of specific activity
    types, e.g. speakers, performers, etc.
    '''
    def __init__(self, type_):
        super().__init__()
        self.type_ = type_

    def get_queryset(self):
        return super().get_queryset().filter(
            activity__activity_type=self.type_,
            is_published=True,
        ).distinct()


class Presenter(TranslatableModel):
    '''
    Person that participates in the event as a guest,
    ie. a speaker, a performer, a workshop presenter or a host.

    First and last name are the only required fields.
    '''
    translations = TranslatedFields(
        first=models.CharField(max_length=255, verbose_name='First name'),
        last=models.CharField(max_length=255, verbose_name='Last name'),
        occupation=models.CharField(max_length=255, blank=True),
        short_bio=models.TextField(blank=True, verbose_name='Short bio'),
        quote=models.CharField(max_length=255, blank=True,
                               verbose_name='Inspirational quote')
    )

    link = models.URLField(blank=True,
                           verbose_name='Website or social media profile')

    image = VersatileImageField(
        'Image',
        upload_to='presenters/',
        width_field='image_width',
        height_field='image_height',
        null=True,
        blank=True,
    )
    image_height = models.PositiveIntegerField(editable=False, null=True)
    image_width = models.PositiveIntegerField(editable=False, null=True)

    is_published = models.BooleanField(_('Published'), default=True)

    # Managers are an easy way to create custom filters for queries.
    #
    # Documentation link:
    # https://docs.djangoproject.com/en/<VAR:DJANGO_VERSION>/topics/db/managers/

    objects = PresenterManager()
    speakers = PresenterTypeManager(Activity.TALK)
    performers = PresenterTypeManager(Activity.PERFORMANCE)
    workshop_presenters = PresenterTypeManager(Activity.WORKSHOP)

    @property
    def fullname(self):
        return ' '.join([self.first, self.last])

    def __str__(self):
        return self.fullname


@receiver(models.signals.post_save, sender=Presenter)
def warm_presenter_images(sender, instance, **kwargs):
    '''Ensures images are created post-save.
    Image sizes are stored in base.VERSATILEIMAGEFIELD_RENDITION_KEY_SETS.
    Using a thumbnail__AxA rendition key, the image fits in a AxA rectangle by
    maintaining the aspect ratio.

    Documentation link:
    https://django-versatileimagefield.readthedocs.io/en/latest/overview.html#create-images-wherever-you-need-them
    '''

    for field in ['image']:
        if getattr(instance, field, None):
            img_warmer = VersatileImageFieldWarmer(
                instance_or_queryset=instance,
                rendition_key_set='Sizes',
                image_attr=field,
                verbose=True
            )
            img_warmer.warm()
