from django.conf import settings

def aadiscordbot_active():
    return 'aadiscordbot' in settings.INSTALLED_APPS
