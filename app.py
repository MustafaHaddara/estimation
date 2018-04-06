# test cli

import json
import sys

import utils
from human import Human

from flask import Flask, request, jsonify

app = Flask( __name__ )

player = Human('human 1')

@app.route('/')
def main():
    return 'Hello world!'

@app.route('/giveCard', methods=['POST'])
def giveCard():
    jsonCard = request.get_json(force=True)
    card = utils.jsonToCard(jsonCard)
    player.giveCard(card)
    return ''

@app.route('/getEstimate', methods=['POST'])
def getEstimate():
    data = request.get_json(force=True)
    estimate = player.getEstimate( data['trumpSuit'], data['invalidGuess'] )
    return jsonify({'estimate': estimate})

@app.route('/getCard', methods=['POST'])
def getCard():
    data = request.get_json(force=True)
    print(data)
    card = player.getCard( data['turns'], data['trumpSuit'] )
    return jsonify(utils.cardToJson(card))

@app.route('/roundWon', methods=['POST'])
def roundWon():
    player.roundWon()
    return ''

if __name__ == ' __main__':
    app.run()
