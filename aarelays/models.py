from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

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

class Servers(models.Model):
    """Servers and their ID"""

    class Message_Type(models.TextChoices):
        DISCORD = 'Discord', _('Discord')
        SLACK = 'Slack', _('Slack')
        XMPP = 'XMPP', _('XMPP')

    server = models.PositiveBigIntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    protocol = models.CharField(max_length=10, default="Discord", choices=Message_Type.choices)

    class Meta:
        verbose_name = 'Server'
        verbose_name_plural = 'Servers'

    def __str__(self):
        return '{}'.format(self.name)

class AccessTokens(models.Model):
    """Access Token"""

    token = models.CharField(max_length=256)
    servers = models.ManyToManyField(Servers)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return '"{}"'.format(self.token)

    class Meta:
        verbose_name = 'Access Token'
        verbose_name_plural = 'Access Tokens'


class Channels(models.Model):
    """Channel IDs, Names and the Server they belong to"""

    server = models.ForeignKey(Servers, on_delete=models.CASCADE)
    channel = models.PositiveBigIntegerField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return '"{}" On "{}"'.format(self.channel_name, self.server_id.server_name)

    class Meta:
        verbose_name = 'Channel'
        verbose_name_plural = 'Channels'

class Messages(models.Model):
    """Message Storage"""

    channel = models.ForeignKey(Channels, on_delete=models.CASCADE)

    message = models.PositiveBigIntegerField(primary_key=True)
    content = models.CharField(max_length=1000)
    datetime = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return '"{}"'.format(self.message_id)

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

class DestinationWebhooks(models.Model):
    """Destinations for Relays"""
    webhook = models.CharField(max_length=50)

class DestinationAADiscordBot(models.Model):
    """Destinaton Channels to be passed to AA-Discord Bot DONT set this to hostile channels you potato"""
    class Message_Type(models.TextChoices):
        CHANNEL_MESSAGE = 'CM', _('Channel Message')
        DIRECT_MESSAGE = 'DM', _('Direct Message')

    destination_type = models.CharField(max_length=2, choices=Message_Type.choices, default=Message_Type.CHANNEL_MESSAGE)
    destination = models.ForeignKey(Channels, on_delete=models.CASCADE)
    
class RelayConfigurations(models.Model):
    """In and Out.... Repeat"""
    source_server = models.ForeignKey(Servers, on_delete=models.CASCADE)
    source_channel = models.ForeignKey(Channels, on_delete=models.CASCADE)

    destination_webhook = models.ForeignKey(DestinationWebhooks, on_delete=models.CASCADE)
    destination_aadiscordbot = models.ForeignKey(DestinationAADiscordBot, on_delete=models.CASCADE)
