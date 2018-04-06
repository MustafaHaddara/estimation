from player import Player

class Human(Player):
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
            print('%s played: %s of %s' % tuple(card))
        allowed = self.printCards(turnsPlayed[0][2] if turnsPlayed else None)
        print('Trump suit is:', trumpSuit)
        print('You estimated %d and have already won %d' % (self.estimate, self.won) )
        idx = int(input('Which card would you like to play? Enter a number: '))
        while idx not in allowed:
            print('Invalid entry.')
            idx = int(input('Which card would you like to play? Enter a number: '))

        return self.cards.pop(idx-1)

    def roundWon(self):
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

    def getCardKey(self, card):
        # card = [VAL, SUIT]
        face_value = {
            'SPADES': 0,
            'CLUBS': 14,
            'DIAMONDS': 28,
            'HEARTS': 42,
        }
        return face_value[card[1]] + (14-self._getFaceValue(card[0]))
