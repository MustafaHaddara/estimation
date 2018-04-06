#!/usr/local/bin/python3
# Remote player api

from player import Player
from utils import *

class RemotePlayer(Player):
    def _sendMsg(self, endpoint, payload):
        # must be defined in subclasses
        raise NotImplementedError

    def _makeRequest(self, endpoint, payload):
        # must be defined in subclasses
        raise NotImplementedError

    def giveCard(self, card):
        command = 'giveCard'
        cardObj = cardToJson(card)
        self._sendMsg(command, cardObj)

    # return type: 
    # {
    #   "estimate": <num>
    # }
    def getEstimate(self, trumpSuit, invalid):
        command = 'getEstimate'
        estimateRequest = {
            'trumpSuit': trumpSuit,
            'invalidGuess': invalid
        }
        jsonResponse = self._makeRequest(command, estimateRequest).json()

        return jsonResponse['estimate']

    # return type: 
    # {
    #   "value": <num>,
    #   "suit" : <one of 'CLUBS', 'SPADES', 'DIAMONDS', 'HEARTS' >
    # }
    def getCard(self, turns, trumpSuit):
        command = 'getCard'
        cardRequest = {
            'turns': turns,
            'trumpSuit': trumpSuit
        }
        jsonCard = self._makeRequest(command, cardRequest).json()
        # must return a tuple of [ <card rank>, <card suit> ]
        return jsonToCard(jsonCard)

    def roundWon(self):
        self._sendMsg('roundWon', None)
