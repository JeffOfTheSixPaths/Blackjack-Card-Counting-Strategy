import numpy as numpy
import random
from Game import *


class Player:
    def __init__(self, card_count, bet_func, prob_tol):
        self.card_count = card_count
        self.bet_function = bet_func
        self.prob_tolerance = prob_tol
        self.money = 300
        self.count = 0
        self.known_deck = ['AC', 'AS', 'AD', 'AH', '2C', '2S', '2D', '2H', '3C', '3S', '3D', '3H', '4C', '4S', '4D', '4H', '5C', '5S', '5D', '5H', '6C', '6S', '6D', '6H', '7C', '7S', '7D', '7H', '8C', '8S', '8D', '8H', '9C', '9S', '9D', '9H','TC', 'TS', 'TD', 'TH', 'JC', 'JS', 'JD', 'JH', 'QC', 'QS', 'QD', 'QH', 'KC', 'KS', 'KD', 'KH']

    def bet_func(self,count, bet_function):
        mon = 20
        for pair in bet_function:
            mon += pair[0] * ( count ** pair[1] )
        return mon

    def make_bet(self):
        return self.bet_func(self.count, self.bet_function)

hilo = {
    '2':1,
    '3':1,
    '4':1,
    '5':1,
    '6':1,
    '7':0,
    '8':0,
    '9':0,
    'T':-1,
    'J':-1,
    'Q':-1,
    'K':-1,
    'A':-1,
    
}
bet = [[1, 1], [2,2]]
pt = 1

p = Player(hilo, bet, pt)
deck = Deck()
g = Game(p, deck.deck)
#print(deck.unshuffled_deck)
print(g.play_shoe(p, deck.unshuffled_deck))