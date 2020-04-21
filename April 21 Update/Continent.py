import Territories as T
class Continent():
    def __init__(self, name, territories, tempMap):
        self.territories = []
        
        for t in territories: #adds countries to map
            T  = T(t, name, tempMap)
            self.territories.append(T)
            tempMap.territories.append(T)
            
        self.numTerritories = len(self.territories)
