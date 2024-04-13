"""A simple Slack integration via webhook

Inspired by slackweb http://qiita.com/satoshi03/items/14495bf431b1932cb90b
"""
import json

import requests


class Slack:

    def __init__(self, url):
        """Config a Slack connection"""
        self.url = url
        # The connection is initiated lazily by requests
        self.session = requests.Session()
        self.session.headers.update({'Content-Type': "application/json"})

    def notify(self, **kwargs):
        """Collect **kwargs as JSON and talk to Slack."""
        return self.send(payload=kwargs)

    def send(self, payload):
        """Send the payload to Slack webhook API.
        Ref: https://api.slack.com/incoming-webhooks

        :param: payload:
            A dict-like object passed as JSON content
        """
        response = self.session.post(
            self.url,
            data=json.dumps(payload)
        )
        return response.status, response.data.decode('utf8')
