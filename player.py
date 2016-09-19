#!/usr/local/bin/python3
# Player

class NPC:
    def __init__(self, name=''):
        self.cards = []
        self.name = name

    def giveCard(self, card):
        self.cards.append(card)

    def getEstimate(self, trumpSuit):
        return 0

    def getCard(self, turnsPlayed):
        pass


class Human(NPC):
    def __init__(self, name=''):
        self.cards = []
        self.name = name
        self.estimate = 0
        self.won = 0

    def giveCard(self, card):
        # print ('You recieved a %s of %s' % card)
        self.cards.append(card)

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
        # print('vvvvvvvvvvvvvvvvvv')
        print('Your turn.')
        # print( turnsPlayed)
        for card in turnsPlayed:
            print('%s played: %s of %s' % card)
        allowed = self.printCards(turnsPlayed[0][2] if turnsPlayed else None)
        print('Trump suit is:', trumpSuit)
        print('You estimated %d and have already won %d' % (self.estimate, self.won) )
        idx = int(input('Which card would you like to play? Enter a number: '))
        while idx not in allowed:
            print('Invalid entry.')
            idx = int(input('Which card would you like to play? Enter a number: '))

        # print('^^^^^^^^^^^^^^^^^^')
        return self.cards.pop(idx-1)

    def winRound(self):
        self.won += 1

    def printCards(self, firstSuit=None, playing=True):
        filtered = []
        canFollowSuit = False
        firstTurn = firstSuit == None
        for card in self.cards:
            canFollowSuit = canFollowSuit or card[1] == firstSuit
            filtered.append( ['  ', 0, *card] )

        print('You have the following cards: ')
        i = 1
        allowed = []
        for tupl in filtered:
            tupl[1] = i
            if playing:
                if canFollowSuit and tupl[3] != firstSuit:
                    tupl[0] = '(invalid)'
                else:
                    tupl[0] = '  (valid)'
                    allowed.append(i)
            # print(tupl)
            print('  %s  %d. %s of %s' % tuple(tupl))
            i += 1

        return allowed
