import pygame
from pygame import *
import constants as c
from interacting import Interacting
from RiskGUI import GUI
import glob
import uiInteractions

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
    def display(self, function = None):

        # Loads png sprites for highlighting selected territories
        worldTerritories = glob.glob(c.mapPath + "*.png")
        territorySprites = []
        highlightedTerritories = []

        spriteSelected = -1

        # Boolean flags for player functions
        selectFlag = False
        attackFlag = False
        helpFlag = False
        gameEnd = False
        startTerritory = None
        targetTerritory = None
        gui = GUI()
        finalLayout = uiInteractions.formatTerr(self, worldTerritories, territorySprites, highlightedTerritories, gui)

        # Event handler
        while (not gameEnd):

            gameEnd, helpFlag, selectFlag, spriteSelected = \
                uiInteractions.eventHandler(self, gameEnd, helpFlag, selectFlag, spriteSelected)

            uiInteractions.sendSurface(self, finalLayout)

            uiInteractions.topLay(self, helpFlag, gui)


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

                    click = uiInteractions.updateVisualGetClick(self, temptroopValID, spriteSelected, spriteLayer)

                    # Placing reinforcements on owned territories
                    if self.turn.list_phase[self.turn.phase] == "Placement":
                        uiInteractions.placing(self, click, temptroopValID)

                    # Attacking neighboring territories with n-1 troops
                    elif self.turn.list_phase[self.turn.phase] == "Attack":

                        attackFlag, selectFlag, startTerritory, targetTerritory = uiInteractions.attacking(self, click, selectFlag, temptroopValID, spriteLayer, attackFlag, gui, territorySprites, finalLayout, startTerritory, targetTerritory)



                    # Moving troops between territories
                    elif self.turn.list_phase[self.turn.phase] == "Movement":
                        # spriteSelected = None
                        # selectFlag, spriteSelected = uiInteractions.moving(self, click, selectFlag, temptroopValID, spriteLayer, startTerritory)
                        # selectFlag = self.moving(click, selectFlag, temptroopValID, spriteLayer, startTerritory)
                        if click[0] == 1 and not selectFlag:  # On left click select territory
                            startTerritory = next((p for p in self.map.territories if p.id == temptroopValID), None)
                            self.selectedTerritory = startTerritory
                            if startTerritory.id_player == self.turn.turnCount and startTerritory.num_troops > 1:
                                self.troopCount = startTerritory.num_troops - 1
                                self.tempTerritoryList.append(spriteLayer.layout)
                                selectFlag = True
                                spriteSelected = temptroopValID

                        elif click[0] == 1:  # On right click unselect territory
                            endTerritory = next((p for p in self.map.territories if p.id == temptroopValID), None)
                            path = self.map.checkValidPath(self.turn.players[self.turn.turnCount - 1].territories,
                                                           startTerritory, endTerritory)
                            selectFlag = False
                            spriteSelected = 0
                            self.tempTerritoryList = []

                            if path and endTerritory.id != startTerritory.id:
                                self.turn.troopMovement(startTerritory, endTerritory, self.troopCount)
                                self.turn.next()


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