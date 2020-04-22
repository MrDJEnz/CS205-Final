from Territories import Territories
class Continent():
    def __init__(self,pays,bonus,name,Map):
        self.bonus=bonus
        self.name=name
        self.pays=[]
        for p in pays:
            P=Territories(p,name,Map)
            self.pays.append(P)
            Map.pays.append(P)
        self.nb_pays=len(self.pays)
