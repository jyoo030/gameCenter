import random

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

class Deck:
    def __init__(self):
        self.card_deck = []
        for suit in ["Clubs", "Diamonds", "Hearts", "Spades"]:
            for num in range(2, 11):
                self.card_deck.append(Card(suit, num))
    
            for face in ["J", "Q", "K", "A"]:
                self.card_deck.append(Card(suit, face))
        
    def shuffle(self):
        random.shuffle(self.card_deck)
    
    def draw_card(self):
        print(f"{self.card_deck[0].value} of {self.card_deck[0].suit}")
        return self.card_deck.pop(0)