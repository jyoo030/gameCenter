from Card_Deck import Deck

class Blackjack:
    def __init__(self, player_list, player):
        self.player_list = player_list
        self.equals_10 = ["J", "Q", "K"]
        self.hit_stand_list = ["h", "s"]
        self.dealer = player
        self.deck = Deck()

        self.play_game()

    def play_game(self):
        self.players_phase()
        self.dealer_phase()
        self.end_phase()

    def players_phase(self):
        self.deck.shuffle()
        for player_num in range(len(self.player_list)):
            if self.player_list[player_num].money == 0:
                print(f"Player {player_num + 1}, you have run out of money.")
                print("You will not be included in game.")
                continue

            print(f"Player {player_num + 1}, you have {self.player_list[player_num].money} money.")
            print(f"How much would you like to bet?")
            while True:
                try:
                    self.player_list[player_num].pot = int(input())
                    if self.player_list[player_num].pot > self.player_list[player_num].money:
                        print("You do not have enough money to bet that much.")
                        print("Please enter a valid number: ")
                        continue
                except ValueError:
                    print("Please enter a valid number: ")
                    continue
                break

            self.player_list[player_num].money -= self.player_list[player_num].pot

            print(f"Player {player_num + 1}, your starting cards are: ")

            self.player_list[player_num].cardlist.append(self.deck.draw_card())
            self.player_list[player_num].cardlist.append(self.deck.draw_card())

            player_sum = self.hand_sum(player_num)

            if player_sum == 21:
                print("Blackjack!")
                self.player_list[player_num].sum = self.hand_sum(player_sum)
                self.player_list[player_num].blackjack = True
                continue

            while self.hit_or_stand(player_num) != "s":
                player_sum = self.hand_sum(player_num)
                if player_sum  == -1:
                    print(f"Player {player_num + 1}, you have a bust! Try again next time!")
                    break
            
            self.player_list[player_num].sum = player_sum

            if self.hand_sum(player_num) != -1:
                print(f"Player {player_num + 1}, your total is {player_sum}.")
    
    def dealer_phase(self):
        print("The dealer's starting cards are: ")
        self.dealer.cardlist.append(self.deck.draw_card())
        self.dealer.cardlist.append(self.deck.draw_card())

        dealer_sum = self.hand_sum()
        while dealer_sum < 17 and dealer_sum != -1:
            print("The dealer hits: ")
            self.dealer.cardlist.append(self.deck.draw_card())
            dealer_sum = self.hand_sum()

        if dealer_sum == -1:
            print("The dealer has busted!")
            dealer_sum = 0
        else:
            print("The dealer stands.")
            print(f"The dealer's total is {dealer_sum}.")
        
        self.dealer.sum = dealer_sum

    def end_phase(self):
        print("Now it is time to compare hands!")
        for player_num in range(len(self.player_list)):
            if self.player_list[player_num].blackjack:
                self.player_blackjack(player_num)
            elif self.player_list[player_num].sum > self.dealer.sum:
                self.player_win(player_num)
            elif self.player_list[player_num].sum < self.dealer.sum:
                self.player_lose(player_num)
            else: # self.player_list[player_num].sum == self.dealer.sum:
                self.player_match(player_num)

        self.dealer.sum = 0
        self.dealer.cardlist = []

    def player_blackjack(self, player_num):
        print(f"Player {player_num + 1}, you got a Blackjack! You earn double your pot!!!")
        self.player_list[player_num].pot *= 3
        self.player_list[player_num].money += self.player_list[player_num].pot
        self.end_round_reset(player_num)

    def player_win(self, player_num):
        print(f"Player {player_num + 1}, you win! Your pot is doubled.")
        self.player_list[player_num].pot *= 2
        self.player_list[player_num].money += self.player_list[player_num].pot
        self.end_round_reset(player_num)

    def player_lose(self, player_num):
        print(f"Player {player_num + 1}, you lose. You lose your pot.")
        self.end_round_reset(player_num)

    def player_match(self, player_num):
        print(f"Player {player_num + 1}, you have matched the dealer.")
        print("You neither double nor lose your pot.")
        self.player_list[player_num].money += self.player_list[player_num].pot
        self.end_round_reset(player_num)

    def end_round_reset(self, player_num):
        self.player_list[player_num].pot = 0
        print(f"Your total money is now: {self.player_list[player_num].money}.")
        self.player_list[player_num].sum = 0
        self.player_list[player_num].cardlist = []
        self.player_list[player_num].blackjack = False

    def hit_or_stand(self, player_num):
        print("Please input <h> to hit, and <s> to stand: ")

        hit_or_stand = input()

        while hit_or_stand not in self.hit_stand_list:
            print("That is not a valid option.")
            print("Please input <h> to hit, and <s> to stand: ")
            hit_or_stand = input()
            
        if hit_or_stand == "h":
            self.player_list[player_num].cardlist.append(self.deck.draw_card())
        return hit_or_stand

    def hand_sum(self, player_num=None):
        if player_num is None:
            player = self.dealer
        else:
            player = self.player_list[player_num]

        temp_sum = 0
        num_aces = 0

        # Add up sum assuming no Aces
        for card in player.cardlist:
            card_value = self.card_value(card)
            temp_sum += card_value
            num_aces += 1 if card_value == 11 else 0

        while num_aces > 0:
            if temp_sum > 21:
                temp_sum -= 10
            num_aces -= 1
            
        if temp_sum > 21:
            return -1
        return temp_sum
    
    def card_value(self, card):
        if type(card.value) == int:
            return card.value
        if card.value in self.equals_10:
            return 10
        if card.value == "A":
            return 11