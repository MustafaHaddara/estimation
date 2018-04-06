import math

from player import Player

class NPC(Player):
    def __init__(self, name=''):
        self.cards = []
        self.name = name
        self.estimate = 0
        self.won = 0

    def giveCard(self, card):
        self.cards.append(card)

    def getEstimate(self, trumpSuit, invalidEstimate=-1):
        cardVals = {
            'ACE': 0.75,
            'KING': 0.75,
            'QUEEN': 0.5,
            'JACK': 0.5,
            '10': 0.25,
        }
        totalPoints = 0
        for card in self.cards:
            faceValue,suit = card
            if faceValue in cardVals:
                totalPoints += cardVals[faceValue]
            if suit == trumpSuit:
                totalPoints += 0.25

        totalPoints = int(math.ceil(totalPoints))
        if totalPoints == invalidEstimate:
            totalPoints += 1

        print('%s estimated %d' % (self.name, int(totalPoints)))
        self.estimate = int(totalPoints)
        self.won = 0
        return self.estimate


    def getCard(self, turnsPlayed, trumpSuit):
        firstSuit = turnsPlayed[0][2] if len(turnsPlayed)>0 else None

        # find the cards we can follow suit with
        filtered = []
        if firstSuit is not None:
            for card in self.cards:
                if card[1] == firstSuit:
                    filtered.append(card)

        # find the highest card we can play
        playedCard = self.findCardToPlay(filtered if len(filtered)>0 else self.cards)

        self.cards.remove(playedCard)
        return playedCard

    def roundWon(self):
        self.won += 1

    def printCards(self, firstSuit=None, playing=True):
        pass

    def findCardToPlay(self, toSearch):
        if self.won < self.estimate:
            return self.findHighest(toSearch)
        else:
            return self.findLowest(toSearch)

    def findHighest(self, toSearch):
        highestCard = None
        highestCardValue = 0

        for card in toSearch:
            faceValue = self._getFaceValue(card[0])
            if faceValue > highestCardValue:
                highestCardValue = faceValue
                highestCard = card
        return highestCard

    def findLowest(self, toSearch):
        lowestCard = None
        lowestCardValue = self._getFaceValue('ACE')+1

        for card in toSearch:
            faceValue = self._getFaceValue(card[0])
            if faceValue < lowestCardValue:
                lowestCardValue = faceValue
                lowestCard = card
        return lowestCard
