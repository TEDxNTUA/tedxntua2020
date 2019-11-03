'''
Relevant Django docs:
https://docs.djangoproject.com/en/2.2/howto/custom-template-tags/
'''
from django import template


register = template.Library()

@register.filter
def lookup(dictionary, key):
    '''
    Returns the value dictionary[key].

    Template syntax: dict|lookup:attr

    Example (suppose dict={a: 1} and attr="a"):
        dict|lookup:attr
        Output: 1

    Stolen from:
    https://stackoverflow.com/a/8000091/11114199
    '''
    return dictionary.get(key)

@register.filter
def make_row_id(counter, stage=''):
    '''
    Formats counter to have two digits and outputs a string like {stage}-row-{number}.

    Template syntax: number|make_row_id or number|make_row_id:stage

    Example (suppose forloop.counter=2 and stage="performance"):
        forloop.counter|make_row_id
        Output: row-02

        forloop.counter|make_row_id:stage
        Output: performance-row-02
    '''
    if stage:
        stage += '-'
    counter = f'{counter:02d}'
    return f'{stage}row-{counter}'
