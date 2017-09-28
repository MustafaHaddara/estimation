#!/opt/local/bin/python3
# Player

class Player:
    # every player must have a name
    name = 'TEST'

    def giveCard(self, card):
        # deal a `card` to the player
        # a card object is just a tuple of (rank, suit)
        # no return value
        pass

    def getEstimate(self, trumpSuit, invalid):
        # get an estimate from the player
        # `trumpSuit` is a string of ['CLUBS', 'SPADES', 'DIAMONDS', 'HEARTS']
        #   which represents the trump suit for the upcoming hand
        # `invalid` is an integer guess that is not allowed
        #   if `invalid` is -1, any estimate is allowed
        # must return an integer
        pass

    def getCard(self, turns, trumpSuit):
        # ask the player for a card for this round of cards
        # `turns` is an array of length 0-3 containing 3-tuples with the following contents:
        #   [ <player name>, <card rank>, <card suit> ]
        #   the first turn in the array determines the suit to follow
        # `trumpSuit` is a string of ['CLUBS', 'SPADES', 'DIAMONDS', 'HEARTS']
        #   which represents the trump suit for the current round
        # must return a tuple of [ <card rank>, <card suit> ]
        pass

    def winRound(self):
        # notify the player that they won a round 
        # and that the next round is about to begin
        # no return value
        pass

    # internal implementation used by NPC and Human classes
    def _getFaceValue(self, face):
        if face == 'ACE': return 14
        if face == 'KING': return 13
        if face == 'QUEEN': return 12
        if face == 'JACK': return 11
        else: return int(face)
