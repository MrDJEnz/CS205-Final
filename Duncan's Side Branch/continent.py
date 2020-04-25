from territories import Territories

class Continent():
    def __init__(self, territories, bonus, name, Map):
        self.bonus = bonus
        self.name = name
        self.territories = []

        # Create the list of territories and append to map
        for i in territories:
            terr = Territories(i, name, Map)
            self.territories.append(terr)
            Map.territories.append(terr)

        self.numTerritories = len(self.territories)

