#Africa
class NorthAfrica:
    def __init__(self):
        self.name = "North Africa"
        self.adjCountries = ("Brazil", "Egypt", "Southern Europe", "Western Europe", "East Africa", "Congo")
        self.curPlayer = ""
        self.curPeople = 0
        self.colliderPoints = [370,340, 485,340, 485,500, 370,500]
        self.textPos = [430,425]

class Egypt:
    def __init__(self):
        self.name = "Egypt"
        self.adjCountries = ("North Africa", "Southern Europe", "Middle East", "East Africa")
        self.curPlayer = ""
        self.curPeople = 0
        self.colliderPoints = [485,345, 585,345, 585,390, 485,390]
        self.textPos = [560,370]

class EastAfrica:
    def __init__(self):
        self.name = "East Africa"
        self.adjCountries = ("Egypt", "North Africa", "Middle East", "Congo", "South Africa", "Madagascar")
        self.curPlayer = ""
        self.curPeople = 0
        self.colliderPoints = [560,390, 630,390, 630,515, 560,515]
        self.textPos = [580,410]

class Congo:
    def __init__(self):
        self.name = "Congo"
        self.adjCountries = ("North Africa", "East Africa", "South Africa")
        self.curPlayer = ""
        self.curPeople = 0
        self.colliderPoints = [510,465, 560,465, 560,515, 510,515]
        self.textPos = [540,510]

class SouthAfrica:
    def __init__(self):
        self.name = "South Africa"
        self.adjCountries = ("Madagascar", "Congo", "East Africa")
        self.curPlayer = ""
        self.curPeople = 0
        self.colliderPoints = [495,515, 595,515, 595,635, 495,635]
        self.textPos = [540,585]

class Madagascar:
    def __init__(self):
        self.name = "Madagascar"
        self.adjCountries = ("East Africa", "South Africa")
        self.curPlayer = ""
        self.curPeople = 0
        self.colliderPoints = [605,540, 660,540, 660,600, 605,600]
        self.textPos = [645,585]

africa = {
    "north africa": NorthAfrica(),
    "egypt": Egypt(),
    "east africa": EastAfrica(),
    "congo": Congo(),
    "south africa": SouthAfrica(),
    "madagascar": Madagascar()
}
