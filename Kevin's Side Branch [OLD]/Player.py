# Team 9 RISK

# Contains datatypes for individual users during the game
class Player():
    def __init__(self, id, Map, turns):
        self.id = id
        self.playerTroops = 0
        self.name = ""
        self.territories = []
        self._bonus = 0
        self._sbyturn = 0
        self._isalive = True
        self.color = (0, 0, 0)
        self.map = Map
        self.turns = turns
        self.obj = None
        self.cards = []
        self.win_land = False


    # Troop bonus from territories
    @property
    def sby(self):
        return max(3, len(self.territories) // 3 + self.bonus)

    # Continent bonus check
    @property
    def bonus(self):
        b = 0
        for c in self.map.continents:
            player_have_cont = True
            for territories in c.territories:
                if territories.id not in self.territories:
                    player_have_cont = False
                    break
            if player_have_cont:
                b += c.bonus
        return b

    # Bool player lost check
    @property
    def isalive(self):
        if len(self.territories) > 0:
            return True
        else:
            return False
