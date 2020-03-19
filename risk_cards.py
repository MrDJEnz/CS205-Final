import random
class Card:
    def __init__(self, territory, army, value):
        self.territory = territory #ex: mexico
        self.army = army #can be infantry, cavalry, artillery
        self.value = value #army size?

    def showCard(self):
        print(self.territory, self.army, self.value)
        
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

##    def addCard(self):
##        return self.deck.append()
    
class Player:
    def __init__(self, name, territoriesOwned):
        self.name = name
        self.hand = []
        self.territoriesOwned = territoriesOwned
        
    def draw(self, deck):
        self.hand.append(deck.drawCard())
        return self

    def trade(self, card):
        pass

    def showHand(self):
        for card in self.hand:
            card.showCard()





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

