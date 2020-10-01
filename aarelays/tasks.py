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
    logger.debug("Beginning Discord_Populate_Models for token {}".format(token))
    client = discord.Client()
    
    @client.event
    async def on_ready():
        print(f"Intel Bot on_ready at: {now()}")
        ## Populate Models on opening the client
        for guild in list(client.guilds):
            print(f"Server Name: {guild.name}")
            print(f"Server ID: {guild.id}")
            Servers.objects.update_or_create(server=guild.id, defaults = {'name': guild.name, 'protocol': "Discord"})
            for channel in list(guild.channels):
                print(f"Channel Name: {channel.name}")
                print(f"Channel ID: {channel.id}")
                Channels.objects.update_or_create(channel=channel.id, defaults={'server_id': guild.id, 'name': channel.name})

        await client.close()

    client.run(token, bot=False)

@shared_task
def slack_populate_models():
    #Populate Server and Channel Models from a Slack Token
    pass