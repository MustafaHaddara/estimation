#!/opt/local/bin/python3
# Player

import math

class NPC:
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

    def winRound(self):
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
            faceValue = self.getFaceValue(card[0])
            if faceValue > highestCardValue:
                highestCardValue = faceValue
                highestCard = card
        return highestCard

    def findLowest(self, toSearch):
        lowestCard = None
        lowestCardValue = self.getFaceValue('ACE')+1

        for card in toSearch:
            faceValue = self.getFaceValue(card[0])
            if faceValue < lowestCardValue:
                lowestCardValue = faceValue
                lowestCard = card
        return lowestCard

    def getFaceValue(self, face):
        if face == 'ACE': return 14
        if face == 'KING': return 13
        if face == 'QUEEN': return 12
        if face == 'JACK': return 11
        else: return int(face)

class Human(NPC):
    def __init__(self, name=''):
        self.cards = []
        self.name = name
        self.estimate = 0
        self.won = 0

    def giveCard(self, card):
        self.cards.append(card)
        self.cards.sort( key=(lambda card: self.getCardKey( card )) )

    def getEstimate(self, trumpSuit, invalidEstimate=-1):
        print('\033c')
        self.printCards(None, False)
        print('The trump suit is: %s' % trumpSuit)
        if invalidEstimate >= 0:
            print('Can not estimate %d' % invalidEstimate)

        
        while True:
            try:
                self.estimate = int(input('Enter the number of rounds you estimate to win: '))
                assert self.estimate != invalidEstimate
                break
            except:
                print('Invalid entry.')

        self.won = 0
        return self.estimate

    def getCard(self, turnsPlayed, trumpSuit):
        print('\033c')
        self.cards.sort(key=self.getCardKey)
        print('Your turn.')
        for card in turnsPlayed:
            print('%s played: %s of %s' % card)
        allowed = self.printCards(turnsPlayed[0][2] if turnsPlayed else None)
        print('Trump suit is:', trumpSuit)
        print('You estimated %d and have already won %d' % (self.estimate, self.won) )
        idx = int(input('Which card would you like to play? Enter a number: '))
        while idx not in allowed:
            print('Invalid entry.')
            idx = int(input('Which card would you like to play? Enter a number: '))

        return self.cards.pop(idx-1)

    def winRound(self):
        self.won += 1

    def printCards(self, firstSuit=None, playing=True):
        filtered = {
            'SPADES': [],
            'CLUBS': [],
            'DIAMONDS': [],
            'HEARTS': []
        }
        canFollowSuit = False
        firstTurn = firstSuit == None
        for card in self.cards:
            canFollowSuit = canFollowSuit or card[1] == firstSuit
            filtered[card[1]].append( ['  ', *card] )

        print('You have the following cards: ')
        allowed = []
        for suit in filtered:
            for tupl in filtered[suit]:
                if playing:
                    if canFollowSuit and tupl[2] != firstSuit:
                        tupl[0] = '(invalid)'
                    else:
                        tupl[0] = '  (valid)'
                allowed.append(tupl)

        allowed_idx = []
        i = 0
        for card in allowed:
            print('  %s  %d. %s of %s' % (card[0],(i+1),*card[1:]) )
            if card[0] == '  (valid)':
                allowed_idx.append(i+1)
            i+=1

        return allowed_idx

    def getCardKey(self,card):
        # card = [VAL, SUIT]
        face_value = {
            'SPADES': 0,
            'CLUBS': 14,
            'DIAMONDS': 28,
            'HEARTS': 42,
        }
        return face_value[card[1]] + (14-self.getFaceValue(card[0]))
