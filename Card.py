import copy
import random

class Card():
    def __init__(self):
        self.types=['Solider','Calvalry','Cannon']
        bonus=[5,8,10,12]
        rand=random.randint(0,2)
        self.type=self.types[rand]
        self.bonus=bonus[rand]
        print(self.bonus)
        self.max_bonus=bonus[-1]
    def __repr__(self):
        return str(self.type)
