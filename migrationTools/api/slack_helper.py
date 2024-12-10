import requests
import json
import os
from datetime import datetime

class SendNotif():
    def __init__(self, migconfig, db_name, author, message, status, repo_name ):
        self.webhook_url = os.environ.get('SLACK_URL')
        self.message = message
        self.date = datetime.now()
        self.migconfig = migconfig
        self.db_name = db_name
        self.author = author
        self.status = status
        self.repo_name = repo_name


    def slack(self):
        payload = {
            "text": (f"Time: {self.date.strftime('%Y-%m-%d %H:%M')} \n"
                     f"Repository Name: {self.repo_name} \n"
                     f"Config Migration: {self.migconfig} \n"
                     f"Database Name: {self.db_name} \n"
                     f"Author: {self.author} \n"
                     f"Status: {self.status} \n"
                     f"Detail: {self.message} \n"
                     )

	    }
        testing = requests.post(self.webhook_url, data=json.dumps(payload))
