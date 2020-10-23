# AA Relays

This is an Alliance Auth App for forwarding, collating and filtering of messages from various chat services to defined outputs including Database logging.

![License](https://img.shields.io/badge/license-MIT-green) ![python](https://img.shields.io/badge/python-3.6-informational) ![django](https://img.shields.io/badge/django-3.1-informational)

## Features

- Sources
  - Discord

- Destinations
  - Database Logging
  - Discord Webhook
  - Discord Channel Message via AA-DiscordBot

- UI for selecting sources and destinations

- Filtering By
  - Server Source
  - Channel Source
  - Mentions AND/OR non mentions
  - Regex on the Message Content

## Planned Features

- Slack Source
- Web UI for Viewing Messages

## Installation

### Step One - Install

Install the app with your venv active

```bash
pip install aa-relays
```

Pull the Runners

`wget https://gitlab.com/soratidus999/aa-relays/-/raw/master/aarelays/runner_discord.py`

### Step Two - Configure

- Add `aarelays` to INSTALLED_APPS
- Add the below lines to your `local.py` settings file

 ```python
## Settings for AA-Relays ##
AARELAYS_TRANSLATION_LANGUAGE = "en" #https://py-googletrans.readthedocs.io/en/latest/#googletrans-languages
```

### Step Three - Update Project

- Run migrations `python manage.py migrate`
- Gather your staticfiles `python manage.py collectstatic`

### Step Four - Run Relays

The "Runners" need to be ran on your server separately for this to function. While they have the context of Django and Alliance Auth, Each "Relay" own runner process to operate.

Supervisor is one option, which you should have for allianceauth already, this is a sample configuration for starting a runner for discord for the first AccessToken in the database.

```python
[program:runner_1]
command=python runner_discord.py 1
directory=/home/allianceserver/myauth/
user=allianceserver
stdout_logfile=/home/allianceserver/myauth/log/aarelays.log
stderr_logfile=/home/allianceserver/myauth/log/aarelays.log
autostart=true
autorestart=true
startsecs=10
priority=900

[group:aarelays]
programs=runner_1
priority=900
```

## Settings

Name | Description | Default
-- | -- | --
AARELAYS_TRANSLATION_LANGUAGE | When attempting a relay translation, what language do I translate to | "en"

## Permissions

Name | Purpose | Code
-- | -- | --
Can Access This App  | Allow users to submit Access Tokens from the Front-End | `relays.basic_access`

## Logic

For Each Token, looping through each Relay Configuration, Messages are Relayed based on the following logic order

```pseudo
Source Server Matches OR All Servers True/False
AND
Source Channel matches OR All Channels True/False
AND
@here/@everyone True/False OR Non Mentions True/False OR Regex (Default ".^" To not match anything, further below)
```

## Regex

Sometimes distinguishing between Mentions and Chatter isn't enough.

Theoretically the full regex library is supported here, but minimal testing has been done, ymmv.

AA Relays Adds header fields into the message string so these cam be regex-ed upon, like so.

`joined_content_with_headers = f"{message.channel.guild.name}/{message.channel.name}/{message.author}: {joined_content}"`

Examples

```psuedo
*supers*
*red pen*

*<@318309023478972417>* For User mentions
*<@&735881663799623710>* for Role Mentions
*supercarriers/318309023478972417/* For a Channel message by a specific Author
```
