import random
from card import Card

class Deck:
    def __init__(self):
        self.deck = []
        self.createDeck()

    def createDeck(self):
        for t in ["PLACEHOLDER FOR LIST OF ALL TERRITORIES"]:
            for a in ["infantry", "cavalry", "artillery"]:
                for v in (3, 20): #army size?
                    self.deck.append(Card(t, a, v))

    def showDeck(self):
        for c in self.deck:
            c.showCard()

    def shuffle(self):
        for i in range(len(self.deck) - 1, 0, -1): #iterate backwards pick random index
            rand = random.randint(0, i)
            self.deck[i], self.deck[rand] = self.deck[rand], self.deck[i] #swap positions

    def drawCard(self):
        return self.deck.pop()
