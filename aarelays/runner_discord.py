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

django.setup()

import aadiscordbot.tasks
from aarelays.models import *

from asgiref.sync import sync_to_async


def now():
    return datetime.utcnow().strftime('%B %d %H:%M')

token = AccessTokens.objects.get(id=2).token

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
        
    # Its important to collate the whole message here or we miss embeds and attachments
    all_content = [f"```\n{message.content}\n```"]
    for e in message.embeds:
        all_content.append(e.url)
    for a in message.attachments:
        all_content.append(a.url)
    joined_content = '\n'.join(all_content)
    msg = f"{message.channel.guild.name}/{message.channel} - " \
        f"{message.author}: {joined_content}"

    if True == True: #db logging check
        try:
            Messages.objects.create(message=message.id, content=msg,channel_id=message.channel.id)
        except Exception as e:
            logger.error(e)

    if False == True: #webhook framwork idk
        msg = f"EVE Time: {now()}\n" \
              f"From: **{message.channel.guild.name}**/{message.author}\n" \
              f"Channel: {message.channel}\n" \
              f"Content:\n{joined_content}"
        if args.exclude_from:
            msg = f"EVE Time: {now()}\n" \
                f"Channel: {message.channel}\n" \
                f"Content:\n{joined_content}"
        print(f"[!] relaying ping: {msg}")
        requests.post(args.webhook, json={"content": msg})
    
    if False == True: # AA Discord Bot queue it framework
        if 'DM' == 'DM':
            aadiscordbot.tasks.send_direct_message()
        if 'CM' == 'CM':
            aadiscordbot.tasks.send_channel_message()

client.run(token, bot=False)
