import pygame
from pygame import *
from sprites import Sprites
from RiskGUI import GUI
import constants as c
import  glob

class Interacting():

    def formatTerr(self, worldTerritories, territorySprites, highlightedTerritories, gui, colorTerritories, textList):
        # Format territory sprites and add to surface
        for i, j in enumerate(worldTerritories):
            surface = pygame.image.load(j).convert()
            resize = c.windowLength / surface.get_width()

            surface = pygame.transform.scale(surface, (
                int(resize * surface.get_width()), int(resize * surface.get_height())))

            territorySprite = Sprites(surface, j)
            initialSpriteLayer = Sprites(surface.copy(), j)

            gui.setSurfaceColor(initialSpriteLayer, (1, 1, 1), 150)
            territorySprites.append(territorySprite)
            highlightedTerritories.append(initialSpriteLayer)

        # Creates final layer of all connected sprites
        colorTerritories(territorySprites, gui)
        for i, j in enumerate(territorySprites):
            if i == 0:
                finalLayout = j.layout.copy()
            else:
                finalLayout.blit(j.layout, (0, 0))

        # Update visual troop numbers
        gui.troopDisplay(textList, territorySprites, map)
        return finalLayout

    def eventHandler(self, gameEnd, helpFlag, selectFlag, selectedTerritory, troopCount, turn):
        for event in pygame.event.get():  # Checks every mouse and key action in window
            if event.type == QUIT:
                print("Ending game!")
                gameEnd = True

            # Handling key presses
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:  # Exit program on key press
                    print("Ending game!")
                    gameEnd = True

                elif event.key == K_n:  # Proceed to next round
                    try:
                        turn.next()
                    except ValueError as e:
                        print(e.args)

                    self.tempTerritoryList = []  # Resets selected territory for next player
                    selectFlag = False
                    selectedTerritory = 0

                elif event.key == K_h:  # Help screen
                    helpFlag = not helpFlag

            # Handling mouse-clicks/scrolls
            elif event.type == MOUSEBUTTONDOWN:
                try:
                    if event.button == 3:  # Right mouse-click to unselect (selected) territory
                        tempTerritoryList = []
                        selectFlag = False
                        selectedTerritory = 0

                    elif event.button == 4:  # Scroll mousewheel down to increase selected troops
                        troopCount += 1

                    elif event.button == 5:  # Scroll mousewheel down to decrease selected troops
                        if troopCount > 0:
                            troopCount -= 1

                except AttributeError as e:
                    print(e)
                    print("You should select a country first ...")
                except ValueError as e:
                    print(e.args)
        return gameEnd, helpFlag, selectFlag, selectedTerritory

    def sendSurface(self, finalLayout, surfaces, pygameWindow, textList, interfaceText, tempTerritoryList, topLevel, interfaceDice, functions):
        # Sends layers to surface of pygame
        for surface in surfaces:
            pygameWindow.blit(surface[0], surface[1])

        for dice in interfaceDice:
            pygameWindow.blit(dice[0], dice[1])

        pygameWindow.blit(finalLayout, (0, 0))

        for tempTerritoryList in tempTerritoryList:
            pygameWindow.blit(tempTerritoryList, (0, 0))

        for text in textList:
            pygameWindow.blit(text[0], text[1])

        for t in interfaceText:
            pygameWindow.blit(t[0], t[1])

        for final in topLevel:
            pygameWindow.blit(final[0], final[1])

        if functions != []:
            for f in functions:
                f()

    def topLay(self, helpFlag, gui, turn, pygameWindow, players):
        # Shows victory screen if player completes domination goal
        if turn.players[turn.turnCount - 1].obj.getGoalStatus() == True:
            topLevel = []

            topLayer = pygame.Surface(pygameWindow.get_size())
            topLayer = topLayer.convert()
            topLayer.fill(c.black)
            topLayer.set_alpha(180)

            topLevel.append([topLayer, (0, 0)])
            gui.display_win(topLevel, players)

        # Uses same top layer to contain help screen
        else:
            if helpFlag:
                topLevel = []

                topLayer = pygame.Surface(pygameWindow.get_size())
                topLayer = topLayer.convert()
                topLayer.fill(c.black)
                topLayer.set_alpha(180)

                topLevel.append([topLayer, (0, 0)])
                gui.display_help(topLevel)
            else:
                topLevel = []

    def updateVisualGetClick(self, temptroopValID, selectedTerritory, spriteLayer, pygameWindow):
        # Update selected territory visuals
        if temptroopValID != selectedTerritory:
            pygameWindow.blit(spriteLayer.layout, (0, 0))
            pygame.display.update(spriteLayer.layout.get_rect())

        # On click, check phase and territory function validity
        click = pygame.mouse.get_pressed()
        return click

    def placing(self, click, temptroopValID, map, turn, troopCount):
        if click[0] == 1:
            playerTerritory = next((p for p in map.territories if p.id == temptroopValID),
                                   None)
            if playerTerritory.id_player == turn.turnCount:
                turn.placeTroops(playerTerritory, troopCount)
                pygame.time.wait(100)
            else:
                print("This territory does not belong to the player!")

    def moving(self, click, selectFlag, temptroopValID, spriteLayer, startTerritory, map, turn, tempTerritoryList, troopCount):
        if click[0] == 1 and not selectFlag:  # On left click select territory
            startTerritory = next((p for p in map.territories if p.id == temptroopValID), None)
            selectedTerritory = startTerritory
            if startTerritory.id_player == turn.turnCount and startTerritory.num_troops > 1:
                troopCount = startTerritory.num_troops - 1
                tempTerritoryList.append(spriteLayer.layout)
                selectFlag = True
                selectedTerritory = temptroopValID

        elif click[0] == 1:  # On right click unselect territory
            endTerritory = next((p for p in map.territories if p.id == temptroopValID), None)
            path = map.checkValidPath(turn.players[turn.turnCount - 1].territories,
                                           startTerritory, endTerritory)
            selectFlag = False
            selectedTerritory = 0
            self.tempTerritoryList = []

            if path and endTerritory.id != startTerritory.id:
                turn.troopMovement(startTerritory, endTerritory, troopCount)
                turn.next()
        return selectFlag