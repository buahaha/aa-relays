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

### Step Two - Configure

- Add `aarelays` to INSTALLED_APPS
- Add the below lines to your `local.py` settings file

 ```python
## Settings for AA-Relays ##
AARELAYS_SETTING_ONE = False
```

### Step Three - Update Project

- Run migrations `python manage.py migrate`
- Gather your staticfiles `python manage.py collectstatic`

## Settings

Name | Description | Default
-- | -- | --
AARELAYS_SETTING_ONE | Does Nothing Currently | False

## Permissions

Name | Purpose | Code
-- | -- | --
Can Access This App  | Allow users to submit Access Tokens from the Front-End | `relays.basic_access`


## Logic

Messages are Relayed for a token based on the following logic order

```
Source Server Matches OR All Servers True/False
AND
Source Channel matches OR All Channels True/False
AND
@here/@everyone True/False OR All Messages True/False OR Regex (Default "" To not match, further below)
```

## Regex

Sometimes distinguishing between Mentions and Chatter isn't enough. 

Theoretically the full regex library is supported here, but minimal testing has been done, ymmv.

AA Relays Adds header fields into the message string so these cam be regex-ed upon, like so.

`joined_content_with_headers = f"{message.channel.guild.name}/{message.channel.name}/{message.author}: {joined_content}"`

Examples
```
*supers*
*red pen*

*<@318309023478972417>* For User mentions
*<@&735881663799623710>* for Role Mentions
*supercarriers/318309023478972417/* For a Channel message by a specific Author
```