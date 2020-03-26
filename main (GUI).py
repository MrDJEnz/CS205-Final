from card import Card
from deck import Deck
from player import Player

def main():
    print("Starting Risk ...")
    
    numPlayers = int(input("How many players are playing?: "))
    while (numPlayers < 2 or numPlayers > 5):
        numPlayers = int(input("How many players are playing?: "))

    startGame(numPlayers)
    
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


def startGame(numPlayers):
    currentGroup = {}
    players = {}
    items = {}
    
    deck = Deck()


    #deck.showDeck()
    
    #initial = 0
    #creates players and gives them first 3 cards... IF USERS ENTER SAME NAME
    #THE DICTIONARY PLACE IS OVERWRITTEN
    for i in range(numPlayers):
        print(i)
        if (i == 0):
            tempName = input("Player " + str(i) + ", what is your name?: ")
            player0 = Player(tempName)
            player0.setHand(deck.dealThreeCards())
        elif (i == 1):
            tempName = input("Player " + str(i) + ", what is your name?: ")
            player1 = Player(tempName)
            player1.setHand(deck.dealThreeCards())
        elif (i == 2):
            tempName = input("Player " + str(i) + ", what is your name?: ")
            player2 = Player(tempName)
            player2.setHand(deck.dealThreeCards())
        elif (i == 3):
            tempName = input("Player " + str(i) + ", what is your name?: ")
            player3 = Player(tempName)
            player3.setHand(deck.dealThreeCards())
        elif (i == 4):
            tempName = input("Player " + str(i) + ", what is your name?: ")
            player4 = Player(tempName)
            player4.setHand(deck.dealThreeCards())

        currentGroup[tempName] = [] #sets player hands to empty
        i += 1
        
    print(currentGroup)
    player0.showHand()

def missions():
    pass
    #create 12 missions, give one to each player, check if mission is complete every turn

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
