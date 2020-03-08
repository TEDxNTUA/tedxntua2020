from django.conf import settings as dj_settings


ALLOWED_SETTINGS = [
    'TEDXNTUA_DATE',
    'TEDXNTUA_SHOW_UNPUBLISHED',
    'TEDXNTUA_SCHEDULE_ENABLED',
    'TEDXNTUA_TICKETS_ENABLED',
    'TEDXNTUA_TICKETS_URL',
]

def settings(req):
    settings_dict = {
        s: getattr(dj_settings, s, None)
        for s in ALLOWED_SETTINGS
    }
    return {'settings': settings_dict}
