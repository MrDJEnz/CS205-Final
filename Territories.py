# Team 9 RISK

# Initializes country data and paths
class Territories():
    def __init__(self, name, continent, Map):
        Map.numTerritories = Map.numTerritories + 1
        self.id = Map.numTerritories
        self.name = name
        self.continent = continent
        self.id_player = 0
        self.nb_troupes = 0
        self.neighbors = []
        
    def voisins(self, territories):
        for t in territories:
            self.neighbors.append(t)
