import pygame
from map import Map
from playerTurn import PlayerTurn
from runGame import RunGame
import constants as c


class SetupGame():

    def __init__(self, running, screen, background, clock):
        self.running = running
        self.screen = screen
        self.background = background
        self.clock = clock
        self.textList = []  # Contains text overlays
        self.topLevel = []  # Used to hold help and win screen

    # Returns information for text handling
    def textArea(self, text, font, color=(0, 0, 0)):
        textSurface = font.render(text, True, color)
        return textSurface, textSurface.get_rect()



    def startGame(self, numPlayers):

        newMap = Map()

        pturn = PlayerTurn(numPlayers, newMap)
        pturn.initialTroops()
        pturn.distributeTerritories(newMap.territories)

        Continents = newMap.continents

        # Initialize players
        names = ["Duncan", "Isaac", "Lilly", "Finn", "Anna", "Brianna"]
        colors = [c.red, c.green, c.blue, c.yellow, c.purple, c.teal]

        for i in range(numPlayers):
            pturn.players[i].color = colors[i]

            pturn.players[i].name = names[i]


        # Setup and start pygame
        pygame.init()
        pygameWindow = pygame.display.set_mode((c.windowLength, c.windowWidth))

        # Create instance of Game to contain risk objects
        # gameInstance = RunGame(pygameWindow, pturn)
        # gameInstance.functions.append(gameInstance.run)
        # gameInstance.display()
        try:
            gameInstance = RunGame(pygameWindow, pturn)
            gameInstance.functions.append(gameInstance.run)
            gameInstance.display()
        except UnboundLocalError as e:
            print(e)
            print("Colorization of map error, restart game and try again!")




