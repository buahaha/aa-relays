import discord
import asyncio
import argparse
import requests
from datetime import datetime

def now():
    return datetime.utcnow().strftime('%B %d %H:%M')

client = discord.Client()

@client.event
async def on_ready():
    ## Populate Models on opening the client
    for guild in list(client.guilds):
        Server.objects.update_or_create(server_id=guild.id, server_name=guild.name, server_type="Discord")
        for channel in list(guild.channels):
            Channel.objects.update_or_create(server_id=guild.id, channel_name=channel.name, channel_id=channel.id)

@client.event
async def on_message(message):
    if message.guild.id != int(args.serverid):
        return

    all_content = [f"```\n{message.content}\n```"]
    for e in message.embeds:
        all_content.append(e.url)
    for a in message.attachments:
        all_content.append(a.url)
    joined_content = '\n'.join(all_content)
    msg = f"{message.channel.guild.name}/{message.channel} - " \
        f"{message.author}: {joined_content}"
    print(msg)
    if args.chat_webhook:
        dmsg = f"{message.channel.guild.name}/{message.channel} - " \
               f"**{message.author}**: {joined_content}"
        requests.post(args.chat_webhook, json={"content": dmsg})
    if str(message.channel) in CHANNELS:
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

client.run(args.token, bot=False)
