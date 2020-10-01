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

## Planned Features

 - Slack Source
 - Web UI for Viewing Messages
 - Message Filters

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

## Perimssions

Name | Purpose | Code
-- | -- | --
Can Access This App  | Allow users to submit Access Tokens from the Front-End | `relays.basic_access`
