import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myauth.settings.local")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

import discord
from discord.ext import commands, tasks
import asyncio
import argparse
import requests
from datetime import datetime
import django
import django.db
from django.conf import settings
import re


import logging
logger = logging.getLogger(__name__)

django.setup()

from aarelays.models import *
from aarelays.app_settings import aadiscordbot_active

if aadiscordbot_active():
    import aadiscordbot.tasks

def now():
    return datetime.utcnow().strftime('%B %d %H:%M')


relayconfiguration = RelayConfigurations.objects.get(id=1)


client = discord.Client()

print(f"Intel Bot Started at: {now()}")

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

@client.event
async def on_message(message):
    logger.debug("Message Event Received")
    if message.channel.guild.id in relayconfiguration.source_server or relayconfiguration.source_server_all == True:
        logger.debug("Matched Server {}".format(message.channel.guild.id))
        if message.channel.id in relayconfiguration.source_channel or relayconfiguration.source_channel_all == True:
            logger.debug("Matched Channel {}".format(message.channel.id))

            # Its important to collate the whole message here or we miss embeds and attachments
            all_content = [f"```\n{message.content}\n```"]
            for e in message.embeds:
                all_content.append(e.url)
            for a in message.attachments:
                all_content.append(a.url)
            joined_content = '\n'.join(all_content)

            joined_content_with_headers = f"{message.channel.guild.name}/{message.channel.name}/{message.author}: {joined_content}"

            #finally lets run our regex over the entire joined message plus headers in case people want to be fancy

            if message.mention_everyone == relayconfiguration.message_mention or message.mention_everyone == relayconfiguration.message_non_mention or re.search(relayconfiguration.message_regex, joined_content_with_headers):
                logger.debug("Matched MentionConfig or Regex")

                if relayconfiguration.destination_db == True: # Are we logging to DB?
                    logger.debug("DB Logging Message")
                    try:
                        Messages.objects.create(message=message.id, content=joined_content,channel_id=message.channel.id)
                    except Exception as e:
                        logger.error(e)

                if relayconfiguration.destination_webhook != None: # Are we sending to a webhook?
                    logger.debug("Sending Message as a Webhook")
                    try:
                        msg = f"EVE Time: {now()}\n" \
                            f"From: **{message.channel.guild.name}**/{message.author}\n" \
                            f"Channel: {message.channel}\n" \
                            f"Content:\n{joined_content}"
                        requests.post(relayconfiguration.destination_webhook.webhook, json={"content": msg})
                    except Exception as e:
                        logger.error(e)
                
                if relayconfiguration.destination_aadiscordbot != None and aadiscordbot_active(): # AA Discord Bot queue it framework
                    logger.debug("Sending Message to AADiscordBot")
                    try:
                        if relayconfiguration.destination_aadiscordbot.destination_type == 'DM'
                            aadiscordbot.tasks.send_direct_message(relayconfiguration.destination_aadiscordbot.destination, joined_content)
                        elif relayconfiguration.destination_aadiscordbot.destination_type == 'CM'
                            aadiscordbot.tasks.send_channel_message(relayconfiguration.destination_aadiscordbot.destination, joined_content))
                        else:

                    except Exception as e:
                        logger.error(e)
                else:
                    logger.debug("Did not act on message")

client.run(relayconfiguration.token, bot=False)