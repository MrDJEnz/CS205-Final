import random
from card import Card

class Deck:
    def __init__(self):
        self.deck = []
        self.createRiskDeck()

    #generates deck of all risk cards (42.. one for each territory)
    def createRiskDeck(self):
        armyType = ["Infantry", "Cavalry", "Artillery"]

        #creates random army/numbers
        for t in range(1, 43):
            randArmy = random.randint(0, 2)
            self.deck.append(Card("Territory: " + str(t), "Army: " + armyType[randArmy], "Troops: " + str(random.randint(2, 5))))

    #draws 3 cards from deck, and returns them as a list/hand
    def dealThreeCards(self):
        removedCards = []
        for i in range(3):
            removedCards.append(self.deck.pop())
        return removedCards
    
    def showDeck(self):
        for c in self.deck:
            c.showCard()

    def shuffle(self):
        for i in range(len(self.deck) - 1, 0, -1): #iterate backwards pick random index
            rand = random.randint(0, i)
            self.deck[i], self.deck[rand] = self.deck[rand], self.deck[i] #swap positions

    def drawCard(self):
        return self.deck.pop()
