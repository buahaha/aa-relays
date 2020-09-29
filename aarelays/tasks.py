from celery import shared_task
from .models import *

import discord
import asyncio
import argparse
import requests
from datetime import datetime

from allianceauth.services.hooks import get_extension_logger

logger = get_extension_logger(__name__)

def now():
    return datetime.utcnow().strftime('%B %d %H:%M')

@shared_task
def discord_populate_models(token):
    #Populate Server and Channel Models from a Slack Token
    #This is a heavily trimmed down version of the Discord Relay Runner that will populate models and close on completion
    
    client = discord.Client()

    @client.event
    async def on_ready():
        ## Populate Models on opening the client
        for guild in list(client.guilds):
            Server.objects.update_or_create(server_id=guild.id, server_name=guild.name, server_type="Discord")
            for channel in list(guild.channels):
                Channel.objects.update_or_create(server_id=guild.id, channel_name=channel.name, channel_id=channel.id)

        await client.close()

    client.run(token, bot=False)

@shared_task
def slack_populate_models():
    #Populate Server and Channel Models from a Slack Token
    pass