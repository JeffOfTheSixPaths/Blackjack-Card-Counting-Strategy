from random import shuffle
import numpy as np
from Hyperparams import *
class Deck:
    def __init__(self):
        self.unshuffled_deck = ['AC', 'AS', 'AD', 'AH', '2C', '2S', '2D', '2H', '3C', '3S', '3D', '3H', '4C', '4S', '4D', '4H', '5C', '5S', '5D', '5H', '6C', '6S', '6D', '6H', '7C', '7S', '7D', '7H', '8C', '8S', '8D', '8H', '9C', '9S', '9D', '9H','TC', 'TS', 'TD', 'TH', 'JC', 'JS', 'JD', 'JH', 'QC', 'QS', 'QD', 'QH', 'KC', 'KS', 'KD', 'KH']
        self.deck = shuffle(self.unshuffled_deck)

class Game:
    def __init__(self,player, deck):
        self.player = player
        self.deck = deck
        self.royals = ['T','J','Q','K']
    
    def get_card_value(self,card, player_count = 0):
        card_value = 0
        #getting the value of the card
        if card[0] in self.royals: card_value = 10
        elif card[0] == 'A':
            if player_count + 11 > 21: 
                card_value = 1
            else: card_value = 11
        else:
            card_value = int(card[0])
        return card_value
    def lose(self,bet):
        self.player.money -= bet
    
    def win(self,bet):
        self.player.money += bet

    def play_shoe(self,player, deck):
        dealer_card = 0
        action = 0
        player.count = 0
        bet = player.make_bet()
        if bet > player.money: bet = player.money
        if player.money == 0: 
            raise ValueError('no money!!')

        while len(deck) > 10:
            #make a new hand
            dealer_cards = [deck[0]]
            player_cards = [deck[1], deck[2]]
            new_cards = [deck.pop(0), deck.pop(1), deck.pop(2)]

            #removing cards from possible cards
            for card in new_cards:
                player.known_deck.remove(card)
                player.count += player.card_count[card[0]]
                

            #Playing the games
            #getting the initial hand counts
            dealer_count = 0
            for card in dealer_cards:
                dealer_count += self.get_card_value(card, dealer_count)

            player.dealer_count = dealer_count
            dealer_card = dealer_count

            player_count = 0
            for card in player_cards:
                player_count += self.get_card_value(card, player_count)

            player.player_count = player_count

            lost = False
            done = False
            while not done:
                # Adjust count based on player's hand
                player.count += player.get_count_value(player.player_count)
                player.count = min(max(player.count, -20), 20)  # Clamp count to range [-20, 20]

                action = player.action()
                if action == 0:
                    # hit()
                    #print("hit")
                    card = deck[0]
                    player.known_deck.remove(deck.pop(0))
                    player.count += player.card_count[card[0]]

                    player.player_count += self.get_card_value(card, player_count)
                    if player.player_count > 21:
                        lost = True
                        done = True
                        break
                else:
                    # stand()
                    while player.dealer_count < player.player_count and player.dealer_count < 21:
                        #hit
                        card = deck[0]
                        player.known_deck.remove(deck.pop(0))
                        player.count += player.card_count[card[0]]
                        
                        player.dealer_count += self.get_card_value(card, dealer_count)
                    done = True
                    break
            # now both players have had their turn 
            if lost: self.lose(bet)
            else:
                if dealer_count > 21:
                    self.win(bet)
                elif player_count > dealer_count:
                    self.win(bet)
                else:
                    self.lose(bet)
                
        player.dealer_count = 0
        player.player_count = 0
        reward = player.get_reward(player.player_count, player.dealer_count, bet)
        player.Q[player.player_count, dealer_card, player.count, action] = (1 - learning_rate) * player.Q[player.player_count, player.dealer_count, player.count, action] + \
                                          learning_rate * (reward + discount_factor * np.max(player.Q[player.player_count, dealer_card, player.count]))
        return player.money


