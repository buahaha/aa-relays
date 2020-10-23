from django.conf import settings
from .utils import clean_setting


def aadiscordbot_active():
    return 'aa-discordbot' in settings.INSTALLED_APPS

AARELAYS_TRANSLATION_LANGUAGE = clean_setting("AARELAYS_TRANSLATION_LANGUAGE", "en")