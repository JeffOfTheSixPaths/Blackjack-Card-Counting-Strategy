from random import shuffle
class Deck:
    def __init__(self):
        self.unshuffled_deck = ['AC', 'AS', 'AD', 'AH', '2C', '2S', '2D', '2H', '3C', '3S', '3D', '3H', '4C', '4S', '4D', '4H', '5C', '5S', '5D', '5H', '6C', '6S', '6D', '6H', '7C', '7S', '7D', '7H', '8C', '8S', '8D', '8H', '9C', '9S', '9D', '9H','TC', 'TS', 'TD', 'TH', 'JC', 'JS', 'JD', 'JH', 'QC', 'QS', 'QD', 'QH', 'KC', 'KS', 'KD', 'KH']
        self.deck = self.unshuffled_deck[:]
        shuffle(self.deck)

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
        #
    def play_shoe(self,player, deck):
        # reset player deck
        player.known_deck = deck.unshuffled_deck
        deck = deck.deck
        
        while len(deck) > 10:
            bet = player.make_bet()
            if bet > player.money: bet = player.money
            if bet < 0: bet = 0
            if player.money <= 0: 
                player.default += player.money - 300
                player.money = 300
                raise ValueError('no')
            #make a new hand
            dealer_cards = [deck[0]]
            player_cards = [deck[1], deck[2]]
            new_cards = [deck.pop(0), deck.pop(1), deck.pop(2)]

            #removing cards from possible cards
            for card in new_cards:
                player.known_deck.remove(str(card))
                player.count += player.card_count[card[0]]
                

            #Playing the games
            #getting the initial hand counts
            dealer_count = 0
            for card in dealer_cards:
                dealer_count += self.get_card_value(card, dealer_count)

            player_count = 0
            for card in player_cards:
                player_count += self.get_card_value(card, player_count)

            lost = False
            while(True):
                prob_bust = 0
                for card in player.known_deck:
                    card_value = self.get_card_value(card, player_count)
                    #going to divide by len(known_deck) to get the probability
                    if card_value + player_count > 21: prob_bust += 1

                prob_bust /= len(player.known_deck)
                if prob_bust < player.prob_tolerance:
                    # hit()
                    #print("hit")
                    card = deck[0]
                    player.known_deck.remove(deck.pop(0))
                    player.count += player.card_count[card[0]]

                    player_count += self.get_card_value(card, player_count)
                    if player_count > 21:
                        lost = True
                        break
                else:
                    # stand()
                    while dealer_count < player_count and dealer_count < 21:
                        #hit
                        card = deck[0]
                        player.known_deck.remove(deck.pop(0))
                        player.count += player.card_count[card[0]]
                        
                        dealer_count += self.get_card_value(card, dealer_count)
                    break
            # now both players have had their turn 
            if lost: 
                self.lose(bet)
                print(f"{player_count} {dealer_count} lost with a bet of {bet} -- bal: {self.player.money}")
            else:
                if dealer_count > 21:
                    self.win(bet)
                    print(f"{player_count} {dealer_count} won with a bet of {bet} -- bal: {self.player.money}")
                elif player_count > dealer_count:
                    self.win(bet)
                    print(f"{player_count} {dealer_count} won with a bet of {bet} -- bal: {self.player.money}")
                elif player_count< dealer_count:
                    self.lose(bet)
                    print(f"{player_count} {dealer_count} lost with a bet of {bet} -- bal: {self.player.money}")
                else:
                    print(f"{player_count} {dealer_count} tied with a bet of {bet} -- bal: {self.player.money}")
                
        player.money += player.default      
        return player.money


