class Card:
    def __init__(self, territory, army, value):
        self.territory = territory #ex: mexico
        self.army = army #can be infantry, cavalry, artillery
        self.value = value #army size?

    def showCard(self):
        print(self.territory, self.army, self.value)
