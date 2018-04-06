#!/usr/local/bin/python3
# Game

from random import randint

from NPC import NPC
from human import Human
from RESTPlayer import RESTPlayer

suits = ['HEARTS', 'DIAMONDS', 'SPADES', 'CLUBS']
ranks = ['ACE', 'KING', 'QUEEN', 'JACK', '10', '9', '8', '7', '6', '5', '4', '3', '2']

deck = [ (i,j) for j in suits for i in ranks ]

class Game:
    def __init__(self):
        # self.players = [Human('player-%d' % (i+1)) for i in range(1)] + [NPC('cpu-%d' % i) for i in range(3)]
        self.players = [RESTPlayer('http://127.0.0.1:8000')] + [NPC('cpu-%d' % i) for i in range(3)]
        self.starting = 0
        self.names = [p.name for p in self.players]
        self.estimates = [0,0,0,0]
        self.won = [0,0,0,0]
        self.points = [0,0,0,0]


    def playGame(self):
        cards = 10
        while (cards <= 13):
            self.playHand(numCards=cards)
            cards += 1
            self.starting = (self.starting + 1) % 4

        self.printScores()


    def playHand(self, numCards):
        # input('Press Enter to continue')
        trumpSuit = suits[randint(0,3)]
        self.deal(numCards)
        self.getEstimates(numCards, trumpSuit)
        self.won = [0,0,0,0]

        for i in range(numCards):
            self.playRound(trumpSuit)

        self.tallyScores(numCards)

        self.starting = (numCards - 3) % 4


    def deal(self, numCards):
        current_deck = self.shuffle(deck)
        player_idx = self.starting
        counter = numCards * 4
        for card in current_deck:
            p = self.players[player_idx]
            p.giveCard(card)
            player_idx = (player_idx + 1) % 4
            counter -= 1
            if counter <= 0:
                break


    def shuffle(self, deck):
        master = [i for i in range(len(deck))]
        shuffled = []

        total = len(master)
        while (total > 0):
            idx = randint(0, total-1)
            shuffled.append(deck[master[idx]])
            del master[idx]
            total = len(master)

        return shuffled


    def getEstimates(self, numCards, trumpSuit):
        invalid = -1
        total = 0
        for i in range(4):
            curr_player_idx = (self.starting + i) % 4
            player = self.players[curr_player_idx]
            if i == 3 and total <= numCards:
                invalid = numCards - total

            est = player.getEstimate(trumpSuit, invalid)
            total += est
            self.estimates[curr_player_idx] = est


    def playRound(self, trumpSuit):
        print('First player is %s' % self.players[self.starting].name)
        # input('Press Enter to continue')
        turns = []
        for i in range(4):
            curr_player = self.players[(self.starting + i) % 4]
            played_card = curr_player.getCard(turns, trumpSuit)
            played_turn = (curr_player.name, *played_card)
            self.printTurn(played_turn)
            turns.append(played_turn)

        self.findWinner(turns, trumpSuit)


    def printTurn(self, turn):
        print('%s played the %s of %s' % turn)


    def findWinner(self, turns, trumpSuit):
        highest = None
        lead_suit = None
        # print('Finding winner in', turns, 'with trump suit', trumpSuit)
        for turn in turns:
            if highest is None:
                highest = turn
                lead_suit = turn[2]
                # print('First turn was', turn)
                continue

            if turn[2] == trumpSuit and highest[2] != trumpSuit:
                highest = turn
                # print('Trumped by', turn)
                continue

            if turn[2] != trumpSuit:
                if turn[2] != lead_suit:
                    continue

                if highest[2] == trumpSuit:
                    continue

            if ranks.index(turn[1]) < ranks.index(highest[1]): # higher cards come first in the list
                # print('Higher card in', turn)
                highest = turn
                continue

        # print('\033c')
        # for card in turns:
        #     print('%s played: %s of %s' % card)
        print('%s won with the %s of %s' % highest)

        winning_player = self.names.index(highest[0])
        # print(winning_player)
        self.won[winning_player] += 1
        self.players[winning_player].roundWon()
        self.starting = winning_player


    def tallyScores(self, numCards):
        for i,est in enumerate(self.estimates):
            won = self.won[i]
            if won == est:
                print('%s estimated %d, won.' % (self.players[i].name, est) )
                self.points[i] += (est + numCards)
            else:
                print('%s estimated %d, won %d rounds' % (self.players[i].name, est, won) )
                self.points[i] -= abs(est - won)
        self.printScores()


    def printScores(self):
        print('Scores are:')
        for i,points in enumerate(self.points):
            print('%s: %d points' % (self.players[i].name, points) )
