from random import shuffle
import numpy as np
from Hyperparams import *
class Deck:
    def __init__(self):
        self.unshuffled_deck = ['AC', 'AS', 'AD', 'AH', '2C', '2S', '2D', '2H', '3C', '3S', '3D', '3H', '4C', '4S', '4D', '4H', '5C', '5S', '5D', '5H', '6C', '6S', '6D', '6H', '7C', '7S', '7D', '7H', '8C', '8S', '8D', '8H', '9C', '9S', '9D', '9H','TC', 'TS', 'TD', 'TH', 'JC', 'JS', 'JD', 'JH', 'QC', 'QS', 'QD', 'QH', 'KC', 'KS', 'KD', 'KH']
        self.deck = self.unshuffled_deck[:]
        shuffle(self.deck)
        self.played_cards = []
    
    def draw_card(self):
        #print(self.deck)
        try:
            card = self.deck.pop(0)
        except:
            self.deck = self.unshuffled_deck[:]
            shuffle(self.deck)
            card = self.deck.pop(0)
        self.played_cards.append(card)
        return card
    
    def __len__(self):
        return len(self.deck)



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
        bet = 0 

        while len(deck) > 15:
            #print(len(deck))
            #global dealer_card
            ##global action
            #global player
            player.count = 0
            #global bet
            dealer_card = 0
            action = 0
            player.count = 0

            #Making the bets
            bet = player.make_bet()

            #sets limits for the bet
            if bet > player.money: bet = player.money
            if player.money <= 0: 
                return 0

            #make a new hand
            dealer_cards = [deck.draw_card()]
            player_cards = [deck.draw_card(), deck.draw_card()]
            new_cards = [dealer_cards[0], player_cards[0], player_cards[1]]
                
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
                player.count = min(max(player.count, -1 * count_size), count_size)  # Clamp count to range [-20, 20]

                action = player.action()
                if action == 0 and player.player_count <= 21:
                    # hit()
                    #print("hit")
                    player.count += player.card_count[deck.draw_card()[0]] 

                    player.player_count += self.get_card_value(card, player_count)
                    if player.player_count > 21:
                        lost = True
                        done = True
                        break
                else:
                    # player stands
                    while player.dealer_count < player.player_count and player.dealer_count < 21:
                        #hit
                        player.count += player.card_count[deck.draw_card()[0]] 
                        
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
        #print(player.card_count)
        player.count = min(max(player.count, -1 * count_size), count_size)
        player.Q[player.player_count, dealer_card, player.count, action] = (1 - learning_rate) * player.Q[player.player_count, player.dealer_count, player.count, action] + \
                                          learning_rate * (reward + discount_factor * np.max(player.Q[player.player_count, dealer_card, player.count]))
        return player.money


