import numpy as np
import random
from Game import *
from Hyperparams import *

class Player:
    def __init__(self, card_count, bet_func, prob_tol):
        self.Q = np.zeros((31, 11, 41, 2 + max_bet))
        self.player_count = 0
        self.dealer_count = 0
        self.card_count = card_count
        self.bet_function = bet_func
        self.prob_tolerance = prob_tol
        self.money = 300
        self.count = 0
        self.known_deck = ['AC', 'AS', 'AD', 'AH', '2C', '2S', '2D', '2H', '3C', '3S', '3D', '3H', '4C', '4S', '4D', '4H', '5C', '5S', '5D', '5H', '6C', '6S', '6D', '6H', '7C', '7S', '7D', '7H', '8C', '8S', '8D', '8H', '9C', '9S', '9D', '9H','TC', 'TS', 'TD', 'TH', 'JC', 'JS', 'JD', 'JH', 'QC', 'QS', 'QD', 'QH', 'KC', 'KS', 'KD', 'KH']

    def get_reward(self, player_hand, dealer_hand, bet):
        if player_hand > 21:  # player busts
            return -bet
        elif dealer_hand > 21:  # dealer busts
            return bet
        elif player_hand > dealer_hand:  # player wins
            return bet
        elif player_hand < dealer_hand:  # dealer wins
            return -bet
        else:  # draw
            return 0

    def get_count_value(self, card):
        if 2 <= card <= 6:
            return 1
        elif 7 <= card <= 9:
            return 0
        else:
            return -1

    def make_bet(self):
        # Choose bet using epsilon-greedy policy
        if np.random.rand() < epsilon:
            bet_action = np.random.randint(2, 2 + max_bet)  # Explore betting
        else:
            bet_action = np.argmax(self.Q[player_hand, dealer_card, count, 2:2 + max_bet]) + 2  # Exploit betting

        bet_amount = bet_action - 1  # convert action to actual bet
        return bet_amount

    def action(self):
        # Choose action (hit or stand) using epsilon-greedy policy
        if np.random.rand() < epsilon:
            action = np.random.choice([0, 1])  # Explore hit or stand
        else:
            action = np.argmax(self.Q[player_hand, dealer_card, count, :2])  # Exploit hit or stand

        return action
        

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
for _ in range(num_episodes):
    g.play_shoe(p, deck.unshuffled_deck)
print("Money made?:" + str(p.money))

