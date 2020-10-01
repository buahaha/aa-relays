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

token = AccessTokens.objects.get(id=1).token

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    for guild in list(client.guilds):
        print("".join("-" for _ in range(100)))
        print(f"Server Name: {guild.name}")
        print(f"Server ID: {guild.id}")
        members = list(guild.members)
        for m in members:
            roles = 'None'
            if m.roles:
                roles = ', '.join(x.name for x in m.roles)
            print(f"[*] {m.display_name} aka {m.nick}, {m.id}, {str(m.joined_at)}, "
                  f"\"{roles}\", {m.status}")

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
        Servers.objects.update_or_create(server=message.channel.guild.id, name=message.channel.guild.name, protocol="Discord")
        Channels.objects.update_or_create(name=message.channel.name, channel=message.channel.id, server_id=message.channel.guild.id)
        Messages.objects.create(message=message.id, content=msg,channel_id=message.channel.id)

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
