#North America
class Alaska:
    def __init__(self):
        self.name = "Alaska"
        self.adjCountries = ("Northwest Territory", "Alberta", "Kamchatka")
        self.curPlayer = ""
        self.curPeople = 0
        self.colliderPoints = [0,0,75,0,75,125,0,125]
        self.textPos = [55,75]
        self.textColor = "ghost white"

class NWTerritory:
    def __init__(self):
        self.name = "Northwest Territory"
        self.adjCountries = ("Alaska", "Alberta", "Greenland", "Ontario")
        self.curPlayer = ""
        self.curPeople = 0
        self.colliderPoints = [80,15, 205,15, 205,105, 80,105]
        self.textPos = [105,40]
        self.textColor = "ghost white"

class Greenland:
    def __init__(self):
        self.name = "Greenland"
        self.adjCountries = ("Northwest Territory", "Ontario", "Quebec", "Iceland")
        self.curPlayer = ""
        self.curPeople = 0
        self.colliderPoints = [210,0, 440,0, 440,110, 210,110]
        self.textPos = [400,25]
        self.textColor = "ghost white"

class Alberta:
    def __init__(self):
        self.name = "Alberta"
        self.adjCountries = ("Northwest Territory", "Ontario", "Western United States", "Alaska")
        self.curPlayer = ""
        self.curPeople = 0
        self.colliderPoints = [80,110, 170,110, 170,185, 80,185]
        self.textPos = [115,145]
        self.textColor = "ghost white"

class Ontario:
    def __init__(self):
        self.name = "Ontario"
        self.adjCountries = ("Alberta", "Northwest Territory", "Quebec", "Greenland", "Eastern United States")
        self.curPlayer = ""
        self.curPeople = 0
        self.colliderPoints = [180,110, 250,110, 250,200, 180,200]
        self.textPos = [205,145]
        self.textColor = "ghost white"

class Quebec:
    def __init__(self):
        self.name = "Quebec"
        self.adjCountries = ("Ontario", "Eastern United States", "Greenland")
        self.curPlayer = ""
        self.curPeople = 0
        self.colliderPoints = [265,115, 350,115, 350,215, 265,215]
        self.textPos = [275,190]
        self.textColor = "ghost white"

class WestUS:
    def __init__(self):
        self.name = "Western United States"
        self.adjCountries = ("Alberta", "Central America", "Eastern United States", "Ontario")
        self.curPlayer = ""
        self.curPeople = 0
        self.colliderPoints = [60,195, 150,195, 150,280, 60,280]
        self.textPos = [70,225]
        self.textColor = "ghost white"

class EastUS:
    def __init__(self):
        self.name = "Eastern United States"
        self.adjCountries = ("Ontario", "Western United States", "Quebec", "Central America")
        self.curPlayer = ""
        self.curPeople = 0
        self.colliderPoints = [160,225, 295,225, 295,305, 160,305]
        self.textPos = [200,220]
        self.textColor = "ghost white"

class CentralAmerica:
    def __init__(self):
        self.name = "Central America"
        self.adjCountries = ("Western United States", "Eastern United States", "Venezuela")
        self.curPlayer = ""
        self.curPeople = 0
        self.colliderPoints = [70,285, 155,285, 155,370, 70,370]
        self.textPos = [120,310]
        self.textColor = "ghost white"

northAmerica = {
    "alaska": Alaska(),
    "northwest territory": NWTerritory(),
    "greenland": Greenland(),
    "alberta": Alberta(),
    "ontario": Ontario(),
    "quebec": Quebec(),
    "western united states": WestUS(),
    "eastern united states": EastUS(),
    "central america": CentralAmerica()
}
