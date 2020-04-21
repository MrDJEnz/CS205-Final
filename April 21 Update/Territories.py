class Territories():
    def __init__(self, name, continent, tempMap):
        tempMap.numTerritories = tempMap.numTerritories + 1 #not using 0 as id
        self.id = tempMap.numTerritories #sets territory id
        self.name = name 
        self.continent = continent #sets continent of territory
        self.playerID = 0 #id of owner
        self.numTroops = 0 #num of occupying troops
        self.neighbors = [] #neighboring territories

    def neighbors(self, territories): #sets the neighboring territories
        for t in territories:
            self.neighbors.append(t)

    def printInfo(self):
        print(self.id, self.name, self.continent, self.playerID, self.numTroops, self.neighbors)
