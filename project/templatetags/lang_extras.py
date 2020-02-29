'''
Relevant Django docs:
https://docs.djangoproject.com/en/2.2/howto/custom-template-tags/
'''
from django import template
from django.urls import translate_url


register = template.Library()

@register.filter
def lang_short_name(code):
    short_names = {
      'el': 'ΕΛ',
      'en': 'EN',
    }
    return short_names.get(code, '')

@register.simple_tag(takes_context=True)
def change_lang(context, lang=None, *args, **kwargs):
    """
    Returns the translated version of the current URL.

    Example:
        <a href="{% change_lang 'en' %}">English version</a>

    Adapted from:
    https://stackoverflow.com/a/57578343
    """
    path = context['request'].path
    return translate_url(path, lang)
