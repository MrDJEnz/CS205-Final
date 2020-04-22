from Continent import Continent

class Map():
    def __init__(self,name):
        self.name=name
        self.pays=[]  
        self.continents=[]
        self.nb_pays=0
        if name=='Terre':
            self.continents.append(Continent(['Congo','East Africa','Egypt','Madagascar','North Africa','South Africa'],3,'Africa',self))
            self.continents.append(Continent(['Alaska','Alberta','Central America','Eastern United States','Groenland','Northern Territories','Ontario','Quebec','Northern United States'],5,'North America',self))
            self.continents.append(Continent(['Venezuela','Bresil','Peru','Argentina'],2,'South America',self))
            self.continents.append(Continent(['Afghanistan','China','India','Tchita','Japan','North Russia','Middle East','Mongolia','Phillipines','Siberia','Northern Russia','Eastern Russia'],7,'Asia',self))
            self.continents.append(Continent(['Great Britan','Iceland','Northern Europe','Scandanvia','Southern Europe','Ukraine','Western Europe'],5,'Europe',self))
            self.continents.append(Continent(['Western Austurlia','Indonesia','Papa New Guiniea','Western Austurlia'],2,'Austrualiaa',self))

            #sets country neighbors
            self.continents[0].pays[0].voisins=[2,5,6]
            self.continents[0].pays[1].voisins=[1,3,4,5,26]
            self.continents[0].pays[2].voisins=[2,5,36,26]
            self.continents[0].pays[3].voisins=[2,6]
            self.continents[0].pays[4].voisins=[1,2,3,17,36,38]
            self.continents[0].pays[5].voisins=[1,2,4]
            self.continents[1].pays[0].voisins=[8,12,25]
            self.continents[1].pays[1].voisins=[7,12,13,15]
            self.continents[1].pays[2].voisins=[15,10,19]# central americas
            self.continents[1].pays[3].voisins=[9,15,13,14]#10
            self.continents[1].pays[4].voisins=[12,13,14,33]
            self.continents[1].pays[5].voisins=[7,8,13,11]
            self.continents[1].pays[6].voisins=[8,15,10,14,11,12]
            self.continents[1].pays[7].voisins=[10,13,11]
            self.continents[1].pays[8].voisins=[9,10,8,13]
            self.continents[2].pays[0].voisins=[17,18]
            self.continents[2].pays[1].voisins=[16,18,19,5]
            self.continents[2].pays[2].voisins=[16,17,19]
            self.continents[2].pays[3].voisins=[18,17,9]#Argentine
            self.continents[3].pays[0].voisins=[21,22,26,30,37]#20
            self.continents[3].pays[1].voisins=[20,22,28,27,29,30]
            self.continents[3].pays[2].voisins=[20,21,26,28]
            self.continents[3].pays[3].voisins=[29,27,25,31]
            self.continents[3].pays[4].voisins=[27,25]
            self.continents[3].pays[5].voisins=[31,23,27,24,7]
            self.continents[3].pays[6].voisins=[20,22,37,2,3]
            self.continents[3].pays[7].voisins=[24,21,29,25,23]
            self.continents[3].pays[8].voisins=[21,22,40]
            self.continents[3].pays[9].voisins=[30,21,23,31,27]
            self.continents[3].pays[10].voisins=[20,21,29,37]#30
            self.continents[3].pays[11].voisins=[29,23,25]
            self.continents[4].pays[0].voisins=[33,35,34,38]
            self.continents[4].pays[1].voisins=[32,35,11]
            self.continents[4].pays[2].voisins=[32,35,37,36,38]
            self.continents[4].pays[3].voisins=[37,32,33,34]
            self.continents[4].pays[4].voisins=[38,34,37,3,26,5]
            self.continents[4].pays[5].voisins=[35,34,36,20,26,30]
            self.continents[4].pays[6].voisins=[32,34,36,5]
            self.continents[5].pays[0].voisins=[42,41]
            self.continents[5].pays[1].voisins=[42,41,28]#40
            self.continents[5].pays[2].voisins=[42,40,39]
            self.continents[5].pays[3].voisins=[39,41,40]
            
    def print_pays(self):
        for pays in self.pays:
            pays.print_carac()

    def chemin_exist(self,pays_joueur, pays1, pays2):
        pays_reachable = []
        if pays1.id in pays_joueur:
            pays_reachable.append(pays1.id)
            self.parcours_profondeur(pays1, pays_joueur, pays_reachable)
            if pays2.id in pays_reachable:
                print("A path exists")
                return True
            else:
                print("There does not exist a path")
                return False
        else:
            print("Player cannot choose this country")
            return False

    def parcours_profondeur(self, pays, pays_joueur, pays_reachable):
        for p_id in pays.voisins:
            if p_id in pays_joueur and p_id not in pays_reachable:
                pays_reachable.append(p_id)
                self.parcours_profondeur(self.pays[p_id-1], pays_joueur,pays_reachable)
