"""A simple Slack integration via webhook

Inspired by slackweb http://qiita.com/satoshi03/items/14495bf431b1932cb90b
"""
import json

import urllib3
import certifi


class Slack:

    def __init__(self, url):
        """Config a Slack connection"""
        self.url = url
        # The connection is initiated lazily by urllib3
        self.pool = urllib3.PoolManager(
            # Always check the HTTPS certificate
            cert_reqs='CERT_REQUIRED',
            ca_certs=certifi.where(),
        )

    def notify(self, **kwargs):
        """Collect **kwargs as JSON and talk to Slack."""
        return self.send(payload=kwargs)

    def send(self, payload):
        """Send the payload to Slack webhook API.
        Ref: https://api.slack.com/incoming-webhooks

        :param: payload:
            A dict-like object passed as JSON content
        """
        response = self.pool.urlopen(
            "POST",
            self.url,
            headers={'Content-Type': "application/json"},
            body=json.dumps(payload)
        )
        return response.status, response.data.decode('utf8')

