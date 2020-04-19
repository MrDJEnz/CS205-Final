import NorthAmerica, SouthAmerica, Europe, Asia, Africa, Australia

NA = NorthAmerica.northAmerica
SA = SouthAmerica.southAmerica
EU = Europe.europe
AS = Asia.asia
AF = Africa.africa
AU = Australia.australia

continents = {
    "North America": NA,
    "South America": SA,
    "Europe": EU,
    "Asia": AS,
    "Africa": AF,
    "Australia": AU
}

class CountryInfo:
    def LookupContinentByCountry(self, userCountryName):
        userCountryName = userCountryName.lower()
        for continentName, countryGroup in continents.items():
            for countryName, country in continents[continentName].items():
                if countryName.lower() == userCountryName.lower():
                    return continentName

    def GetBorderingCountries(self, userCountryName):
        userCountryName = userCountryName.lower()
        for continentName, countryGroup in continents.items():
            for countryName, country in continents[continentName].items():
                if countryName.lower() == userCountryName.lower():
                    return country.adjCountries

    def GetCurrentOccupent(self, userCountryName):
        userCountryName = userCountryName.lower()
        for continentName, countryGroup in continents.items():
            for countryName, country in continents[continentName].items():
                if countryName.lower() == userCountryName.lower():
                    return country.curPlayer

    def GetCurrentSoliderCount(self, userCountryName):
        userCountryName = userCountryName.lower()
        for continentName, countryGroup in continents.items():
            for countryName, country in continents[continentName].items():
                if countryName.lower() == userCountryName.lower():
                    return country.curPeople

    def GetCountryNameByClick(self, click):
        import Rectangle
        Rectangle = Rectangle.Rectangle()
        for continentName, countryGroup in continents.items():
            for countryName, country in continents[continentName].items():
                if Rectangle.contains(click, country.colliderPoints):
                    return country.name

    def GetCountryTextPos(self, userCountryName):
        userCountryName = userCountryName.lower()
        for continentName, countryGroup in continents.items():
            for countryName, country in continents[continentName].items():
                if countryName.lower() == userCountryName.lower():
                    return country.textPos

    def ChangeCountryColor(self, userCountryName, newColor):
        for continentName, countryGroup in continents.items():
            for countryName, country in continents[continentName].items():
                if countryName.lower() == userCountryName.lower():
                    country.textColor = newColor

    def ChangeCountryArmyCount(self, userCountryName, numChange):
        for continentName, countryGroup in continents.items():
            for countryName, country in continents[continentName].items():
                if countryName.lower() == userCountryName.lower():
                    country.curPeople += numChange
