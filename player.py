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
