# estimation
cmdline implementation of a card game called Estimation

# Rules
Exactly 4 players may play.

Randomly select a trump suit.
Using a standard 52-card deck, deal 3 cards to each player.
Each player takes turns estimating the number of rounds they will win. Player to the right of the dealer goes first. 
When it comes to the dealer's turn to estimate, they are not allowed to make an estimate which would make the sum of all of the players' estimates equal to the number of cards dealt. 
    For example, if the players estimate: 3, 4, and 4, then the dealer may NOT estimate "2".

Each round proceeds as follows: 
    One player leads by playing a single card.
        On the first round, this is the player to the right of the dealer
        On subsequent rounds, this is the player who won the previous round
    Play proceeds to the right.
    The next player plays a card.
        This card MUST follow the same suit as the suit of the player who lead the round. 
        If this player does not have any of that suit, they may play any card.
    The next two players play a card in order, following the suit of the first player if they have cards in that suit. 

    The winner of the round is the player who plays the highest card. 
        Cards are ranked as follows: Ace, King, Queen, Jack, and then in numerical order.
        Any card in the trump suit will beat any card in any other suit. (So if the trump suit is Hearts, a 2 of Hearts will beat an Ace of Spades)

    The next round proceeds in the same manner, but deal out 1 more card to each player than in the previous round (so the second round has 4 cards, the third round has 5 cards, etc.)

Any player who wins the exact amount of rounds as they estimated earns points. The amount of points they win is equal to the number of cards in the hand (13) plus their estimate. 

Any player who does not win the amount they estimated loses points. They lose the difference between their estimate and the amount they won; if a player estimates 3 and only wins 1 round, that player loses 2 points (3 - 1 = 2)

After playing a round with 13 cards, deal out all 13 cards for the final _sans_ round. This is the last round of the game, and is played without a trump suit.

The player with the most points at the end is the winner.