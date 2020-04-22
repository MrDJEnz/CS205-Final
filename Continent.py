# Team 9 RISK
from Territories import Territories

# Contains set territories to be used for troop bonuses
class Continent():
    def __init__(self, territories, bonus, name, Map):
        self.bonus = bonus
        self.name = name
        self.territories = []
        
        for i in territories:
            T = Territories(i, name, Map)
            self.territories.append(T)
            Map.territories.append(T)
            
        self.numTerritories = len(self.territories)
