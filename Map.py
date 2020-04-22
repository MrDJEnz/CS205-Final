# Team 9 Risk
from Continent import Continent

# Initializes territories and manages paths
class Map():
    def __init__(self):
        self.territories = []  
        self.continents = []
        self.numTerritories = 0

        self.continents.append(Continent(["Congo", "East Africa", "Egypt", "Madagascar", "North Africa", "South Africa"], 3, "Africa", self))
        self.continents.append(Continent(["Alaska", "Alberta", "Central America", "Eastern United States", "Groenland", "Northern Territories", "Ontario", "Quebec", "Northern United States"], 5, "North America", self))
        self.continents.append(Continent(["Venezuela", "Bresil", "Peru", "Argentina"], 2, "South America", self))
        self.continents.append(Continent(["Afghanistan", "China", "India", "Tchita", "Japan", "North Russia", "Middle East", "Mongolia", "Phillipines", "Siberia", "Northern Russia", "Eastern Russia"], 7, "Asia", self))
        self.continents.append(Continent(["Great Britan", "Iceland", "Northern Europe", "Scandanvia", "Southern Europe", "Ukraine", "Western Europe"], 5, "Europe", self))
        self.continents.append(Continent(["Western Austurlia", "Indonesia", "Papa New Guiniea", "Western Austurlia"], 2, "Austrualiaa", self))

        self.continents[0].territories[0].voisins=[2, 5, 6]
        self.continents[0].territories[1].voisins=[1, 3, 4, 5, 26]
        self.continents[0].territories[2].voisins=[2, 5, 36, 26]
        self.continents[0].territories[3].voisins=[2, 6]
        self.continents[0].territories[4].voisins=[1, 2, 3, 17, 36, 38]
        self.continents[0].territories[5].voisins=[1, 2, 4]
        self.continents[1].territories[0].voisins=[8, 12, 25]
        self.continents[1].territories[1].voisins=[7, 12, 13, 15]
        self.continents[1].territories[2].voisins=[15, 10, 19]# central americas
        self.continents[1].territories[3].voisins=[9, 15, 13, 14]#10
        self.continents[1].territories[4].voisins=[12, 13, 14, 33]
        self.continents[1].territories[5].voisins=[7, 8, 13, 11]
        self.continents[1].territories[6].voisins=[8, 15, 10, 14, 11, 12]
        self.continents[1].territories[7].voisins=[10, 13, 11]
        self.continents[1].territories[8].voisins=[9, 10, 8, 13]
        self.continents[2].territories[0].voisins=[17, 18]
        self.continents[2].territories[1].voisins=[16, 18, 19, 5]
        self.continents[2].territories[2].voisins=[16, 17, 19]
        self.continents[2].territories[3].voisins=[18, 17, 9]#Argentine
        self.continents[3].territories[0].voisins=[21, 22, 26, 30, 37]#20
        self.continents[3].territories[1].voisins=[20, 22, 28, 27, 29, 30]
        self.continents[3].territories[2].voisins=[20, 21, 26, 28]
        self.continents[3].territories[3].voisins=[29, 27, 25, 31]
        self.continents[3].territories[4].voisins=[27, 25]
        self.continents[3].territories[5].voisins=[31, 23, 27, 24, 7]
        self.continents[3].territories[6].voisins=[20, 22, 37, 2, 3]
        self.continents[3].territories[7].voisins=[24, 21, 29, 25, 23]
        self.continents[3].territories[8].voisins=[21, 22, 40]
        self.continents[3].territories[9].voisins=[30, 21, 23, 31, 27]
        self.continents[3].territories[10].voisins=[20, 21, 29, 37]#30
        self.continents[3].territories[11].voisins=[29, 23, 25]
        self.continents[4].territories[0].voisins=[33, 35, 34, 38]
        self.continents[4].territories[1].voisins=[32, 35, 11]
        self.continents[4].territories[2].voisins=[32, 35, 37, 36, 38]
        self.continents[4].territories[3].voisins=[37, 32, 33, 34]
        self.continents[4].territories[4].voisins=[38, 34, 37, 3, 26, 5]
        self.continents[4].territories[5].voisins=[35, 34, 36, 20, 26, 30]
        self.continents[4].territories[6].voisins=[32, 34, 36, 5]
        self.continents[5].territories[0].voisins=[42, 41]
        self.continents[5].territories[1].voisins=[42, 41, 28]#40
        self.continents[5].territories[2].voisins=[42, 40, 39]
        self.continents[5].territories[3].voisins=[39, 41, 40]
            

    def checkPathValid(self, playerTerritories,  startTerritory,  endTerritory):
        validTerritories = []
        if startTerritory.id in playerTerritories:
            validTerritories.append(startTerritory.id)
            self.pathCalculation(startTerritory,  playerTerritories,  validTerritories)
            if endTerritory.id in validTerritories:
                print("A path exists")
                return True
            else:
                print("There does not exist a path")
                return False
        else:
            print("Player cannot choose this country")
            return False

    def pathCalculation(self,  territories,  playerTerritories,  validTerritories):
        for pathIndexer in territories.voisins:
            if pathIndexer in playerTerritories and pathIndexer not in validTerritories:
                validTerritories.append(pathIndexer)
                self.pathCalculation(self.territories[pathIndexer - 1],  playerTerritories, validTerritories)


