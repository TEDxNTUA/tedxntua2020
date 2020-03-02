from django.conf import settings as dj_settings


ALLOWED_SETTINGS = [
    'TEDXNTUA_DATE', 'SCHEDULE_ENABLED', 'TICKETS_ENABLED',
]

def settings(req):
    return {
        s: getattr(dj_settings, s, None)
        for s in ALLOWED_SETTINGS
    }
