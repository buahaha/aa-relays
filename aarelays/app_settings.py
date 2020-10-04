from django.conf import settings

def aadiscordbot_active():
    return 'aa-discordbot' in settings.INSTALLED_APPS

"""
EXAMPLE_SETTING_ONE = getattr(
    settings, 
    'EXAMPLE_SETTING_ONE', 
    None
)
"""