from django.conf import settings
from django.db import models
from django.db import models

from django.contrib.auth.models import Group

from allianceauth.eveonline.models import EveCorporationInfo, EveAllianceInfo

class Relays(models.Model):
    """Meta model for app permissions"""

    class Meta:
        managed = False                         
        default_permissions = ()
        permissions = ( 
            ('basic_access', 'Can access this app'), 
        )

class Server(models.Model):
    """Servers and their ID"""

    SERVER_TYPE_CHOICES = (
        ('Discord', 'Discord'),
        ('Slack', 'Slack'),
        ('XMPP', 'XMPP'),
    )
    server_id = models.IntegerField()
    server_name = models.CharField(max_length=100)
    server_type = models.CharField(max_length=10, default="Discord", choices=SRP_STATUS_CHOICES)

    class Meta:
        verbose_name = 'Server'
        verbose_name_plural = 'Servers'

    def __str__(self):
        return '{}'.format(self.server_name)

class Channel(models.Model):
    """Channel IDs, Names and the Server they belong to"""

    server_id = models.ForeignKey(server_id, on_delete=models.CASCADE)

    channel_name = models.CharField(max_length=100)
    channel_id = models.IntegerField()

    def __str__(self):
        return '"{}" On "{}"'.format(self.channel_name, self.server_id.server_name)

    class Meta:
        verbose_name = 'Channel'
        verbose_name_plural = 'Channels'

class Message(models.Model):
    """Message Storage"""

    channel_id = models.ForeignKey(channel_id, on_delete=models.CASCADE)

    message_id = models.IntegerField()
    message_content = models.CharField(max_length=1000)

    def __str__(self):
        return '"{}"'.format(self.message_content)

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

class AccessToken(models.Model):
    """Access Token"""

    token = models.CharField(max_length=256)
    server_id = models.ForeignKey(server_id, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return '"{}"'.format(self.webhook.name)

    class Meta:
        verbose_name = 'Fleet Signal'
        verbose_name_plural = 'Fleet Signals'