from django.contrib import admin

from .models import *

from allianceauth.services.hooks import get_extension_logger

logger = get_extension_logger(__name__)

@admin.register(Servers)
class ServersAdmin(admin.ModelAdmin):
    list_display = ('server', 'name')
    ordering = ('name',)

    search_fields = ('name',)

@admin.register(AccessTokens)
class AccessTokenAdmin(admin.ModelAdmin):
    list_display = ('token', 'owner')
    ordering = ('owner',)

@admin.register(Channels)
class ChannelsAdmin(admin.ModelAdmin):
    list_display = ('server', 'channel', 'name', 'server_name')
    ordering = ('name',)

    search_fields = ('name','server_name',)

    @staticmethod
    def server_name(obj):
        try:
            return obj.server.name
        except Exception as e:
            logger.error(e)

@admin.register(Messages)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ('message', 'channel_name', 'server_name')
    ordering = ('message',)

    search_fields = ('server_name', 'message_text',)

    @staticmethod
    def channel_name(obj):
        try:
            return obj.channel_id
        except Exception as e:
            logger.error(e)

    @staticmethod
    def server_name(obj):
        try:
            return obj.channel_id.server_id
        except Exception as e:
            logger.error(e)
