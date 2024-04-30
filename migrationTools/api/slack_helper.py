import requests
import json
import os

class SendNotif():
    def __init__(self, message):
        self.webhook_url = os.environ.get('SLACK_URL')
        self.message = message


    def slack(self):
        payload = {
	        "text": self.message
	    }
        return requests.post(self.webhook_url, data=json.dumps(payload))