class Territories():
    def __init__(self,name,continent,Map):
        Map.nb_pays=Map.nb_pays+1
        self.id=Map.nb_pays
        self.name=name
        self.continent=continent
        self.id_player=0
        self.nb_troupes=0
        self.voisins=[]
        
    def voisins(self,pays):
        for p in pays:
            self.voisins.append(p)

    def print_carac(self):
        print(self.id,self.name,self.continent,self.id_player,self.nb_troupes,self.voisins)
