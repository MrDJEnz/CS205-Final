#South America
class Venezuela:
    def __init__(self):
        self.name = "Venezuela"
        self.adjCountries = ("Central America", "Brazil", "Peru")
        self.curPlayer = ""
        self.curPeople = 0
        self.colliderPoints = [120,380, 260,380, 260,420, 120,420]
        self.textPos = [130,415]
        self.textColor = "ghost white"

class Peru:
    def __init__(self):
        self.name = "Peru"
        self.adjCountries = ("Venezuela", "Brazil", "Argentina")
        self.curPlayer = ""
        self.curPeople = 0
        self.colliderPoints = [120,460, 215,460, 215,535, 120,535]
        self.textPos = [140,490]
        self.textColor = "ghost white"

class Brazil:
    def __init__(self):
        self.name = "Brazil"
        self.adjCountries = ("Venezuela", "Peru", "Argentina", "North Africa")
        self.curPlayer = ""
        self.curPeople = 0
        self.colliderPoints = [220,425, 340,425, 340,600, 220,600]
        self.textPos = [245,470]
        self.textColor = "ghost white"

class Argentina:
    def __init__(self):
        self.name = "Argentina"
        self.adjCountries = ("Peru", "Brazil")
        self.curPlayer = ""
        self.curPeople = 0
        self.colliderPoints = [120,540, 215,540, 215,670, 120,670]
        self.textPos = [160,600]
        self.textColor = "ghost white"

southAmerica = {
    "venezuela": Venezuela(),
    "peru": Peru(),
    "brazil": Brazil(),
    "argentina": Argentina()
}
