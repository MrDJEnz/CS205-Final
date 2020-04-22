class Map():
    def __init__(self):
        self.continents = []
        self.territories = []
        self.numTerritories = 0

##        self.continents.append(Continent(['Alaska','Alberta','Amerique Centrale','Etats de l\'Est','Groenland','Territoires du Nord-Ouest','Ontario','Quebec','Etats de l\'Ouest'],5,'Amerique du Nord',self))
##        self.continents.append(Continent(['Venezuela','Bresil','Perou','Argentine'],2,'Amerique du Sud',self))
##        self.continents.append(Continent(['Afghanistan','Chine','Inde','Tchita','Japon','Kamchatka','Moyen-Orient','Mongolie','Siam','Siberie','Oural','Yakoutie'],7,'Asie',self))
##        self.continents.append(Continent(['Grande-Bretagne','Islande','Europe du Nord','Scandinavie','Europe du Sud','Ukraine','Europe Occidentale'],5,'Europe',self))
##        self.continents.append(Continent(['Australie Orientale','Indonésie','Nouvelle-Guinée','Australie Occidentale'],2,'Oceanie',self))
##        self.continents.append(Continent(['Congo','Affrique de l\'Est','Egypte','Madagascar','Afrique du Nord','Afrique du Sud'],3,'Afrique',self))
##
##        self.continents[0].pays[0].voisins=[2,5,6]
##        self.continents[0].pays[1].voisins=[1,3,4,5,26]
##        self.continents[0].pays[2].voisins=[2,5,36,26]
##        self.continents[0].pays[3].voisins=[2,6]
##        self.continents[0].pays[4].voisins=[1,2,3,17,36,38]
##        self.continents[0].pays[5].voisins=[1,2,4]
##        self.continents[1].pays[0].voisins=[8,12,25]
##        self.continents[1].pays[1].voisins=[7,12,13,15]
##        self.continents[1].pays[2].voisins=[15,10,19]
##        self.continents[1].pays[3].voisins=[9,15,13,14]#10
##        self.continents[1].pays[4].voisins=[12,13,14,33]
##        self.continents[1].pays[5].voisins=[7,8,13,11]
##        self.continents[1].pays[6].voisins=[8,15,10,14,11,12]
##        self.continents[1].pays[7].voisins=[10,13,11]
##        self.continents[1].pays[8].voisins=[9,10,8,13]
##        self.continents[2].pays[0].voisins=[17,18]
##        self.continents[2].pays[1].voisins=[16,18,19,5]
##        self.continents[2].pays[2].voisins=[16,17,19]
##        self.continents[2].pays[3].voisins=[18,17,9]
##        self.continents[3].pays[0].voisins=[21,22,26,30,37]#20
##        self.continents[3].pays[1].voisins=[20,22,28,27,29,30]
##        self.continents[3].pays[2].voisins=[20,21,26,28]
##        self.continents[3].pays[3].voisins=[29,27,25,31]
##        self.continents[3].pays[4].voisins=[27,25]
##        self.continents[3].pays[5].voisins=[31,23,27,24,7]
##        self.continents[3].pays[6].voisins=[20,22,37,2,3]
##        self.continents[3].pays[7].voisins=[24,21,29,25,23]
##        self.continents[3].pays[8].voisins=[21,22,40]
##        self.continents[3].pays[9].voisins=[30,21,23,31,27]
##        self.continents[3].pays[10].voisins=[20,21,29,37]#30
##        self.continents[3].pays[11].voisins=[29,23,25]
##        self.continents[4].pays[0].voisins=[33,35,34,38]
##        self.continents[4].pays[1].voisins=[32,35,11]
##        self.continents[4].pays[2].voisins=[32,35,37,36,38]
##        self.continents[4].pays[3].voisins=[37,32,33,34]
##        self.continents[4].pays[4].voisins=[38,34,37,3,26,5]
##        self.continents[4].pays[5].voisins=[35,34,36,20,26,30]
##        self.continents[4].pays[6].voisins=[32,34,36,5]
##        self.continents[5].pays[0].voisins=[42,41]
##        self.continents[5].pays[1].voisins=[42,41,28]#40
##        self.continents[5].pays[2].voisins=[42,40,39]
##        self.continents[5].pays[3].voisins=[39,41,40]

        
