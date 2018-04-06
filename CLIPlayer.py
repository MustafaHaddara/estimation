#!/usr/local/bin/python3
# locally run player subprocess

import json
import subprocess

from remotePlayer import RemotePlayer

class CLIPlayer(RemotePlayer):
    def __init__(self, name=''):
        self.proc = subprocess.Popen(name, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    def _sendMsg(self, endpoint, payload):
        if payload is None:
            payload = {}
        payload['command'] = endpoint
        self.proc.stdin.write(json.dumps(payload))

    def _makeRequest(self, endpoint, payload):
        self._sendMsg(endpoint, payload)
        res = ''
        while res == '':
            res = self.proc.stdout.readline().strip()
        return res
