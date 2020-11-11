import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myauth.settings.local")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

import argparse
import requests
from datetime import datetime
import django
import django.db
from django.conf import settings
import re
import asyncio
import threading

from slackclient import SlackClient

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("runnertokenid")
args = parser.parse_args()

import logging
logger = logging.getLogger(__name__)

from googletrans import Translator
translator = Translator()

django.setup()

from aarelays.models import AccessTokens, RelayConfigurations, Channels, Messages, Servers
from aarelays.app_settings import aadiscordbot_active

if aadiscordbot_active():
    import aadiscordbot.tasks

def now():
    return datetime.utcnow().strftime('%B %d %H:%M')

slacktoken = AccessTokens.objects.get(id=args.runnertokenid)

logger.debug(f"AA Relays config #{args.runnertokenid} Started at: {now()}")
running = False
client = SlackClient(slacktoken.token

run()

def run(self):
    logger.info("{0} - Connecting to Slack server".format(self.name))
    if client.rtm_connect(with_team_state=False):
        logger.info("{0} - Connected to Slack server".format(self.name))
        slackRTM()
    else:
        logger.error("{0} - Connection failed".format(self.name))
        running = False

def replace_user_id_with_name(self, match):
    user_id = match.group(1)
    try:
        user_info = self.client.api_call("users.info", user=user_id)
        return "@" + user_info["user"]["name"]
    except Exception as e:
        logger.warn("{0} - Could not get user name for {1}".format(self.name, user_id))
        return user_id

def slackRTM(self):
    delay = 0
    while self.running:
        try:
            events = self.client.rtm_read()
        except Exception as err:
            logger.error("{0} - Could not get RTM events {1}".format(self.name, err))
            self.running = False
            continue
        if events:
            delay = 0
            if self.messageHandler is not None:
                for event in events:
                    if event["type"] == "message":
                        #Ignore channel joins
                        if "subtype" in event:
                            if event["subtype"] == "channel_join":
                                continue

                        if "text" not in event:
                            continue
                        try:
                            msg = event["text"]
#                                logger.debug("{0} - Got message from Slack RTM: {1}".format(self.name, msg))
                        except Exception:
                            logger.debug("{0} - Got message from Slack RTM: (Can't display)".format(self.name))

                        #Get sender
                        try:
                            user_info = self.client.api_call("users.info", user=event["user"])
                            user = user_info["user"]["name"]
                        except Exception as err:
                            logger.warn("{0} - Could not get user info {1}".format(self.name, err))
                            user = "Unknown ({0})".format(event["user"])
                        #Get channel
                        if event["channel"].startswith("C"):
                            try:
                                channel_info = self.client.api_call("channels.info", channel=event["channel"])
                                channel = channel_info["channel"]["name"]
                            except Exception as err:
                                logger.warn("{0} - Could not get channel info {1}".format(self.name, err))
                                channel = "Unknown ({0})".format(event["channel"])
                            #Channel filter
                            if channel not in self.channel_list:
#                                   logger.debug("{0} - Channel '{1}' is not listened to".format(self.name, channel))
                                continue
                        elif event["channel"].startswith("D"):
                            channel = "Direct Message"
                            #PM Filter
                            if user not in self.pm_list:
                                logger.debug("{0} - User '{1}' is not listened to".format(self.name, user))
                                continue
                        #Get time
                        timestamp = float(event["ts"])
                        msgTime = datetime.fromtimestamp(timestamp)

                        #Username replacement
                        regex = re.compile(r"<@([\w\d]+)>")
                        msg = regex.sub(self.replace_user_id_with_name, msg)

                        message = Message(self, msg, user, channel, self.server, msgTime)
                        self.relay_message(message)

        else:
            delay += 1
            delay = min(delay, 10)
        time.sleep(delay)
    logger.error("{0} - RTM disconnected".format(self.name))