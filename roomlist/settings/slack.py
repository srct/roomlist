# standard library imports
from __future__ import absolute_import, print_function
# standard library imports
import json
# third party imports
import requests
# imports from your apps
from .secret import SLACK_WEBHOOK_URL


webhook_url = SLACK_WEBHOOK_URL


def slack_post(text, channel, username, icon_emoji):
    try:
        payload = {'text': text, 'channel': channel,
                   'username': username, 'icon_emoji': icon_emoji, }
        r = requests.post(webhook_url, data=json.dumps(payload))
        r.raise_for_status()
        print(r.status_code)
    except requests.exceptions.RequestException as e:
        print("Error posting to Slack:", e)

# Examples

# slack_post(text="A terrible, awful thing happened on the server!",
#            channel='#bot-test',
#            username='Roomlist Server Errors',
#            icon_emoji=':fire:')

# slack_post(text="Congratulations! You've passed 150 users registrations!",
#            channel='#bot-test',
#            username='Roomlist User Milestones',
#            icon_emoji=':tada:')
