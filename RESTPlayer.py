#!/usr/local/bin/python3
# player over REST

import requests

from remotePlayer import RemotePlayer

class RESTPlayer(RemotePlayer):
    def __init__(self, name=''):
        self.url = name

    def _sendMsg(self, endpoint, payload):
        if payload is None:
            requests.post(self.url + '/' + endpoint)
        else:
            print(payload)
            requests.post(self.url + '/' + endpoint, json=payload)

    def _makeRequest(self, endpoint, payload):
        return requests.post(self.url + '/' + endpoint, json=payload)
