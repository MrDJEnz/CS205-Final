from card import Card
from deck import Deck
from player import Player

def main():
    print("Starting Risk ...")
    #TODO GUI/GRAPHICAL START
    
##    card = Card("Mexico", "Infantry", 10)
##    card.showCard()
##    print("----------------------")
##    deck = Deck()
##    deck.showDeck()
##    print("----------------------")
##    deck.shuffle()
##    deck.showDeck()
##    print("----------------------")
##    print("You rempved: ", deck.drawCard())
##    print("You rempved: ", deck.drawCard())
##    deck.showDeck()
##    print("----------------------")
##    yoda = Player("Yoda", 6)
##    yoda.draw(deck)
##    yoda.showHand()

def saveGame():
    with open("Game_Save", "rb") as save:
        pickle.dump(tempLoad, save)
    print("Your game has been saved! Exiting ...")
    exit()


def loadGame():
    with open("Game_Save", "rb") as save:
        tempLoad = pickle.load(save)
    print("Your game has been loaded! Resuming ...")
    #TODO method to resume game
    
main()
