class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.territoriesOwned = 0
        
    def draw(self, deck):
        self.hand.append(deck.drawCard())
        return self

    def trade(self, card):
        pass

    def showHand(self):
        for card in self.hand:
            card.showCard()

    def getHand(self):
        return self.hand
            
    def setHand(self, newHand):
        self.hand = newHand

    def getName(self):
        return self.name
