import pygame
from pygame import *
import constants as c
from interacting import Interacting
from RiskGUI import GUI
import glob
from sprites import Sprites

class RunGame():
    def __init__(self, window, turn):
        self.pygameWindow = window

        # Updates current objects
        self.map = turn.map
        self.players = turn.players
        self.turn = turn

        self.numTroops = 25  # Sets number of troops
        self.selectedTerritory = None

        self.interfaceDice = []  # Contains dice results
        self.functions = []  # Contains function calls
        self.interfaceText = []  # Contains text layers for HUD
        self.surfaces = []  # Contains surface layers
        self.tempTerritoryList = []  # Contains territory layers
        self.textList = []  # Contains text overlays
        self.topLevel = []  # Used to hold help and win screen

    @property  # Decorator overwrites get/set, method checks min deployment troops
    def troopCount(self):
        if self.turn.phase == 0:
            return min(self.numTroops, self.players[
                self.turn.turnCount - 1].num_troops)  # Cannot deploy more then total - 1 troops from territory
        else:
            return self.numTroops

    @troopCount.setter  # Alternative corresponding decorator
    def troopCount(self, troopVal):
        if self.turn.phase == 0:  # Checks troop placement during different phases
            if troopVal < 1:
                self.numTroops = 1
                print("Too few troops")
            elif troopVal > self.players[self.turn.turnCount - 1].num_troops:
                self.numTroops = self.players[self.turn.turnCount - 1].num_troops
                print("Too many troops")
        else:
            if troopVal < 0:
                self.numTroops = 0
                print("Too few troops")
            elif troopVal > self.selectedTerritory.num_troops - 1:
                self.numTroops = self.selectedTerritory.num_troops - 1  # Minimum of 1 troop per territory
                print("Too many troops")

        self.numTroops = troopVal

    # Sets a color layer on territory sprites based on player color
    def colorTerritories(self, sprites, gui):
        for p in self.players:
            for territories in p.territories:
                sprite = next((s for s in sprites if s.id == territories), None)
                gui.setSurfaceColor(sprite, p.color, 255)

    # Method initialzes map surface
    def run(self):
        self.surfaces = []
        background = pygame.image.load(c.imagePath + c.backgroundImage).convert()

        # Auto resize to fit background
        resize = c.windowLength / background.get_width()
        w = int(resize * background.get_width())
        h = int(resize * background.get_height())
        background = pygame.transform.scale(background, (w, h))

        # Auto resize to fit base map
        worldMap = pygame.image.load(c.imagePath + c.mapImages).convert_alpha()
        resize = c.windowLength / worldMap.get_width()
        w = int(resize * worldMap.get_width())
        h = int(resize * worldMap.get_height())
        worldMap = pygame.transform.scale(worldMap, (w, h))

        # Player HUD
        barre = pygame.image.load(c.imagePath + c.bareImage).convert_alpha()
        barre = pygame.transform.scale(barre, (c.windowLength, c.windowWidth - h))

        self.functions = []
        self.surfaces.extend([[background, (0, 0)], [barre, (0, h)], [worldMap, (0, 0)]])

    # ==================================================================================================================
    # Method utilizes overlay methods to update pygameWindow
    def formatTerr(self, worldTerritories, territorySprites, highlightedTerritories, gui):
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
        self.colorTerritories(territorySprites, gui)
        for i, j in enumerate(territorySprites):
            if i == 0:
                finalLayout = j.layout.copy()
            else:
                finalLayout.blit(j.layout, (0, 0))

        # Update visual troop numbers
        gui.troopDisplay(self.textList, territorySprites, self.map)
        return finalLayout

    def eventHandler(self, gameEnd, helpFlag, selectFlag, selectedTerritory):
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
                        self.turn.next()
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
                        self.tempTerritoryList = []
                        selectFlag = False
                        selectedTerritory = 0

                    elif event.button == 4:  # Scroll mousewheel down to increase selected troops
                        self.troopCount += 1

                    elif event.button == 5:  # Scroll mousewheel down to decrease selected troops
                        if self.troopCount > 0:
                            self.troopCount -= 1

                except AttributeError as e:
                    print(e)
                    print("You should select a country first ...")
                except ValueError as e:
                    print(e.args)
        return gameEnd, helpFlag, selectFlag, selectedTerritory

    def sendSurface(self, finalLayout):
        # Sends layers to surface of pygame
        for surface in self.surfaces:
            self.pygameWindow.blit(surface[0], surface[1])

        for dice in self.interfaceDice:
            self.pygameWindow.blit(dice[0], dice[1])

        self.pygameWindow.blit(finalLayout, (0, 0))

        for tempTerritoryList in self.tempTerritoryList:
            self.pygameWindow.blit(tempTerritoryList, (0, 0))

        for text in self.textList:
            self.pygameWindow.blit(text[0], text[1])

        for t in self.interfaceText:
            self.pygameWindow.blit(t[0], t[1])

        for final in self.topLevel:
            self.pygameWindow.blit(final[0], final[1])

        if self.functions != []:
            for f in self.functions:
                f()

    def topLay(self, helpFlag, gui):
        # Shows victory screen if player completes domination goal
        if self.turn.players[self.turn.turnCount - 1].obj.getGoalStatus() == True:
            self.topLevel = []

            topLayer = pygame.Surface(self.pygameWindow.get_size())
            topLayer = topLayer.convert()
            topLayer.fill(c.black)
            topLayer.set_alpha(180)

            self.topLevel.append([topLayer, (0, 0)])
            gui.display_win(self.topLevel, self.players)

        # Uses same top layer to contain help screen
        else:
            if helpFlag:
                self.topLevel = []

                topLayer = pygame.Surface(self.pygameWindow.get_size())
                topLayer = topLayer.convert()
                topLayer.fill(c.black)
                topLayer.set_alpha(180)

                self.topLevel.append([topLayer, (0, 0)])
                gui.display_help(self.topLevel)
            else:
                self.topLevel = []

    def updateVisualGetClick(self, temptroopValID, selectedTerritory, spriteLayer):
        # Update selected territory visuals
        if temptroopValID != selectedTerritory:
            self.pygameWindow.blit(spriteLayer.layout, (0, 0))
            pygame.display.update(spriteLayer.layout.get_rect())

        # On click, check phase and territory function validity
        click = pygame.mouse.get_pressed()
        return click

    def placing(self, click, temptroopValID):
        if click[0] == 1:
            playerTerritory = next((p for p in self.map.territories if p.id == temptroopValID),
                                   None)
            if playerTerritory.id_player == self.turn.turnCount:
                self.turn.placeTroops(playerTerritory, self.troopCount)
                pygame.time.wait(100)
            else:
                print("This territory does not belong to the player!")

    def moving(self, click, selectFlag, temptroopValID, spriteLayer, startTerritory):
        if click[0] == 1 and not selectFlag:  # On left click select territory
            startTerritory = next((p for p in self.map.territories if p.id == temptroopValID), None)
            self.selectedTerritory = startTerritory
            if startTerritory.id_player == self.turn.turnCount and startTerritory.num_troops > 1:
                self.troopCount = startTerritory.num_troops - 1
                self.tempTerritoryList.append(spriteLayer.layout)
                selectFlag = True
                selectedTerritory = temptroopValID

        elif click[0] == 1:  # On right click unselect territory
            endTerritory = next((p for p in self.map.territories if p.id == temptroopValID), None)
            path = self.map.checkValidPath(self.turn.players[self.turn.turnCount - 1].territories,
                                           startTerritory, endTerritory)
            selectFlag = False
            selectedTerritory = 0
            self.tempTerritoryList = []

            if path and endTerritory.id != startTerritory.id:
                self.turn.troopMovement(startTerritory, endTerritory, self.troopCount)
                self.turn.next()
        return selectFlag


    def display(self, function = None):

        # Loads png sprites for highlighting selected territories
        worldTerritories = glob.glob(c.mapPath + "*.png")
        territorySprites = []
        highlightedTerritories = []

        selectedTerritory = -1

        # Boolean flags for player functions
        selectFlag = False
        attackFlag = False
        helpFlag = False
        gameEnd = False
        gui = GUI()
        runcommands = Interacting()
        finalLayout = self.formatTerr(worldTerritories, territorySprites, highlightedTerritories, gui)

        # Event handler
        while (not gameEnd):

            gameEnd, helpFlag, selectFlag, selectedTerritory = \
                self.eventHandler(gameEnd, helpFlag, selectFlag, selectedTerritory)

            self.sendSurface(finalLayout)

            self.topLay(helpFlag, gui)


            # Highlight territories as cursor moves over them
            mouse = pygame.mouse.get_pos()
            try:
                tempColorValue = self.surfaces[2][0].get_at((mouse[0], mouse[1]))
            except IndexError as e:
                print(e)
                pass

            # Setups user GUI layout and enables player functions
            try:
                if tempColorValue != (0, 0, 0, 0) and tempColorValue != (0, 0, 0, 255):
                    temptroopValID = tempColorValue[0] - 100
                    spriteLayer = next((territorySprite for territorySprite in highlightedTerritories if
                                        territorySprite.id == temptroopValID), None)

                    click = self.updateVisualGetClick(temptroopValID, selectedTerritory, spriteLayer)

                    # Placing reinforcements on owned territories
                    if self.turn.list_phase[self.turn.phase] == "Placement":
                        self.placing(click, temptroopValID)

                    # Attacking neighboring territories with n-1 troops
                    elif self.turn.list_phase[self.turn.phase] == "Attack":
                        if click[0] == 1 and not selectFlag:
                            startTerritory = next((p for p in self.map.territories if p.id == temptroopValID), None)
                            self.selectedTerritory = startTerritory
                            if startTerritory.id_player == self.turn.turnCount and startTerritory.num_troops > 1:
                                self.troopCount = startTerritory.num_troops - 1
                                self.tempTerritoryList.append(spriteLayer.layout)
                                selectFlag = True
                                selectedTerritory = temptroopValID

                        elif click[0] == 1:  # Selecting territory to attack
                            endTerritory = next((p for p in self.map.territories if p.id == temptroopValID), None)
                            if attackFlag and endTerritory == targetTerritory and startTerritory.num_troops > 1:
                                self.turn.troopMovement(startTerritory, endTerritory, self.troopCount)
                                selectFlag = False
                                self.tempTerritoryList = []
                                attackFlag = False

                            elif attackFlag:
                                selectFlag = False
                                self.tempTerritoryList = []
                                attackFlag = False

                            elif endTerritory.id_player != self.turn.turnCount and endTerritory.id in startTerritory.neighbors:  # Attack with home troops
                                try:
                                    self.interfaceDice = []
                                    attackResult, diceResults = self.turn.attack(startTerritory, endTerritory,
                                                                                 self.troopCount)
                                    for i, res in enumerate(diceResults):
                                        gui.diceRolls(self, res[0], res[2], 600, territorySprites[
                                            0].layout.get_height() + 10 + i * c.diceSize * 1.1)
                                        gui.diceRolls(self, res[1], res[3], 800, territorySprites[
                                            0].layout.get_height() + 10 + i * c.diceSize * 1.1)
                                    pygame.time.wait(100)
                                except ValueError as e:
                                    print(e.args)
                                    attackResult = False
                                    selectFlag = False
                                    self.tempTerritoryList = []
                                if attackResult:  # On successful attack, update visuals
                                    sprite = next((s for s in territorySprites if s.id == temptroopValID), None)
                                    gui.setSurfaceColor(sprite, self.turn.players[self.turn.turnCount - 1].color, 255)
                                    finalLayout.blit(sprite.layout, (0, 0))
                                    attackFlag = True
                                    targetTerritory = endTerritory
                                    self.troopCount = startTerritory.num_troops - 1
                                else:
                                    selectFlag = False
                                    self.tempTerritoryList = []



                    # Moving troops between territories
                    elif self.turn.list_phase[self.turn.phase] == "Movement":
                        selectFlag = self.moving(click, selectFlag, temptroopValID, spriteLayer, startTerritory)


                    # Update troop text overlay visuals
                    self.textList = []
                    gui.troopDisplay(self.textList, territorySprites, self.map)

            except ValueError as e:
                pass

            # Update HUD text visuals
            self.interfaceText = []
            gui.display_hud(self.troopCount, self.interfaceText, self.turn,
                        (75, territorySprites[0].layout.get_height() + 10))
            pygame.display.flip()
# ==================================================================================================================
# Returns information for text handling