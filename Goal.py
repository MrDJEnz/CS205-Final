class Goal():
    def __init__(self,Map,turns):
        self.turns=turns
        self.types=['capture continents','capture territories','kill all enemies']
        self.map=Map
        self.randrange=[[0,1,2,3,4,5],[],[x for x in range(1,turns.nb_players+1)]]
