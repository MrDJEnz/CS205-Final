from card import Card
from deck import Deck
from player import Player

def main():
    print("Risk")
    card = Card("Mexico", "Infantry", 10)
    card.showCard()
    print("----------------------")
    deck = Deck()
    deck.showDeck()
    print("----------------------")
    deck.shuffle()
    deck.showDeck()
    print("----------------------")
    print("You rempved: ", deck.drawCard())
    print("You rempved: ", deck.drawCard())
    deck.showDeck()
    print("----------------------")
    yoda = Player("Yoda", 6)
    yoda.draw(deck)
    yoda.showHand()
    
main()
