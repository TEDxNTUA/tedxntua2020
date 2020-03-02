from django.conf import settings as dj_settings


ALLOWED_SETTINGS = [
    'TEDXNTUA_DATE',
    'TEDXNTUA_SHOW_UNPUBLISHED',
    'TEDXNTUA_SCHEDULE_ENABLED',
    'TEDXNTUA_TICKETS_ENABLED',
]

def settings(req):
    return {
        s: getattr(dj_settings, s, None)
        for s in ALLOWED_SETTINGS
    }
