import pygame
from map import Map
from playerTurn import PlayerTurn
from runGame import RunGame
# from runGameWithAI import RunGameWithAI
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

    def startGame(self, numPlayers, running, screen, background, clock, numAI):

        print("we Have 1 AI player")

        newMap = Map()

        totalPlayers = numPlayers + numAI
        pturn = PlayerTurn(totalPlayers, newMap)
        pturn.initialTroops()
        pturn.distributeTerritories(newMap.territories)

        Continents = newMap.continents

        # Initialize players
        names = c.names
        colors = c.colors

        aiNames = []
        # Initialize AI
        for i in range(numAI):
            aiNames.append("AI"+str(i))

        print(names)
        print(colors)
        print(numPlayers)
        print(numAI)

        for i in range(totalPlayers):
            pturn.players[i].color = colors[i]
        for i in range(numPlayers):
            pturn.players[i].name = names[i]
        for i in range(numAI):
            pturn.players[i+numPlayers].name = aiNames[i]

        print(pturn.players)

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
            print("Try moving the moving your mouse cursor onto the man's nose while you wait?")

            sGame = SetupGame(running, screen, background, clock)
            sGame.startGame(numPlayers, running, screen, background, clock, numAI)




