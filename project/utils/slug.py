from django_extensions.db.fields import AutoSlugField
from parler.models import TranslationDoesNotExist


class EnglishAutoSlugField(AutoSlugField):
    """
    AutoSlugField that uses django-parler to select English translation.
    """
    def pre_save(self, model_instance, add):
        curr_language = model_instance.get_current_language()
        model_instance.set_current_language('en')
        try:
            value = super().pre_save(model_instance, add)
        except TranslationDoesNotExist:
            # If English version does not exist, fallback to current one
            model_instance.set_current_language(curr_language)
            value = super().pre_save(model_instance, add)
        return value
