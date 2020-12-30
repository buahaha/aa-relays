from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


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

    class Protocol_Choice(models.TextChoices):
        DISCORD = 'Discord', _('Discord')
        SLACK = 'Slack', _('Slack')
        XMPP = 'XMPP', _('XMPP')

    server = models.PositiveBigIntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    protocol = models.CharField(max_length=10, default="Discord",
                                choices=Protocol_Choice.choices)

    class Meta:
        verbose_name = 'Server'
        verbose_name_plural = 'Servers'

    def __str__(self):
        return '{}'.format(self.name)


class AccessTokens(models.Model):
    """Access Token"""

    token = models.CharField(max_length=256)
    servers = models.ManyToManyField(Servers, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.SET_NULL, blank=True, null=True)

    appear_offline = models.BooleanField(default=False)

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
        return '"{}" On "{}"'.format(self.name, self.server.name)

    class Meta:
        verbose_name = 'Channel'
        verbose_name_plural = 'Channels'


class Messages(models.Model):
    """Message Storage"""

    channel = models.ForeignKey(Channels, on_delete=models.CASCADE)

    message = models.PositiveBigIntegerField(primary_key=True)
    content = models.CharField(max_length=1000)
    datetime = models.DateTimeField(auto_now=False, auto_now_add=True)
    author = models.PositiveBigIntegerField()
    author_nick = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return '"{}"'.format(self.message)

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'


class DestinationWebhooks(models.Model):
    """Destinations for Relays"""
    webhook = models.CharField(max_length=200)
    name = models.CharField(max_length=50)

    def __str__(self):
        return '"{}"'.format(self.name)

    class Meta:
        verbose_name = 'Destination Webhook'
        verbose_name_plural = 'Destination Webhooks'


class DestinationAADiscordBot(models.Model):
    """Destinaton Channels to be passed to AA-Discord
    Bot DON'T set this to hostile channels you potato"""
    class Message_Type(models.TextChoices):
        CHANNEL_MESSAGE = 'CM', _('Channel Message')
        DIRECT_MESSAGE = 'DM', _('Direct Message')

    destination_type = models.CharField(max_length=2,
                                        choices=Message_Type.choices,
                                        default=Message_Type.CHANNEL_MESSAGE)
    destination = models.ForeignKey(Channels, on_delete=models.CASCADE)

    def __str__(self):
        return '"{}"'.format(self.destination)

    class Meta:
        verbose_name = 'Discord Channel Destination'
        verbose_name_plural = 'Discord Channel Destinations'


class RelayConfigurations(models.Model):
    """In and Out...... Repeat"""
    name = models.CharField(max_length=50)
    token = models.ForeignKey(AccessTokens, on_delete=models.CASCADE)

    attempt_translation = models.BooleanField(default=False)

    message_mention = models.BooleanField(default=True)
    message_non_mention = models.BooleanField(default=False)
    message_regex = models.CharField(max_length=10, default=".^", blank=False,
                                     null=False)

    source_server = models.ManyToManyField(Servers)
    source_server_all = models.BooleanField(default=False)
    source_channel = models.ManyToManyField(Channels)
    source_channel_all = models.BooleanField(default=False)

    destination_webhook = models.ManyToManyField(DestinationWebhooks,
                                                 blank=True)
    destination_aadiscordbot = models.ManyToManyField(DestinationAADiscordBot,
                                                      blank=True)
    destination_db = models.BooleanField(default=False)

    def __str__(self):
        return '"{}"'.format(self.name)

    class Meta:
        verbose_name = 'Relay Configuration'
        verbose_name_plural = 'Relay Configurations'
