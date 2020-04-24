# Team 9 RISK
# Game can be run by itself for debugging, run the RiskGUI to setup player settings

# Imports needed modules
import functools
import glob
import pickle
import pygame
from pygame import *
from Sprites import Sprites

import Constants as c

# Class contains pygame methods
class Game():
    def __init__(self, pygameWindow, Turn): #Initializes surfaces for pygame given pygame and round instances
        self.pygameWindow = pygameWindow

        # Updates current objects
        self.map = Turn.map
        self.players = Turn.players
        self.Turn = Turn

        self.numTroops = 25 #Sets number of troops
        self.selectedTerritory = None

        self.interfaceDice = [] #Contains dice results
        self.functions = [] #Contains function calls
        self.interfaceText = [] #Contains text layers for HUD
        self.surfaces = [] #Contains surface layers
        self.tempTerritoryList = [] #Contains territory layers
        self.textList = [] #Contains text overlays
        self.topLevel = [] #Used to hold help and win screen

    @property # Decorator overwrites get/set, method checks min deployment troops
    def troopCount(self):
        if self.Turn.phase == 0:
            return min(self.numTroops, self.players[self.Turn.turnCount-1].nb_troupes) #Cannot deploy more then total - 1 troops from territory
        else:
            return self.numTroops

    @troopCount.setter # Alternative corresponding decorator
    def troopCount(self, troopVal):
        if self.Turn.phase == 0: #Checks troop placement during different phases
            if troopVal < 1:
                self.numTroops = 1
                print("Too few troops")
            elif troopVal > self.players[self.Turn.turnCount - 1].nb_troupes:
                self.numTroops = self.players[self.Turn.turnCount - 1].nb_troupes
                print("Too many troops")
        else: 
            if troopVal < 0:
                self.numTroops = 0
                print("Too few troops")
            elif troopVal > self.selectedTerritory.nb_troupes - 1:
                self.numTroops = self.selectedTerritory.nb_troupes - 1 #Minimum of 1 troop per territory
                print("Too many troops")
                
        self.numTroops = troopVal

    # Sets a color layer on territory sprites based on player color
    def colorTerritories(self, sprites):
        for p in self.players:
            for territories in p.territories:
                sprite = next((s for s in sprites if s.id == territories), None)
                setSurfaceColor(sprite, p.color, 255)


##    # Displays initial menu
##    def menu(self):
##        print(1)
##
##        self.surfaces = []
##        menuBackground = pygame.image.load(c.imagePath + c.menuBackgroundImage).convert()
##
##        #Auto resize to fit menuBackground
##        resize = c.windowLength/menuBackground.get_width()
##        w = int(resize * menuBackground.get_width())
##        h = int(resize * menuBackground.get_height())
##        menuBackground = pygame.transform.scale(menuBackground, (w, h))
##
##        self.functions = []
##        self.surfaces.extend([[menuBackground, (0, 0)]])
        

    # Method initialzes map surface
    def run(self):
        self.surfaces=[]
        background = pygame.image.load(c.imagePath + c.backgroundImage).convert()

        #Auto resize to fit background
        resize = c.windowLength/background.get_width()
        w = int(resize * background.get_width())
        h = int(resize * background.get_height())
        background = pygame.transform.scale(background, (w, h))

        #Auto resize to fit base map
        worldMap = pygame.image.load(c.imagePath + c.mapImages).convert_alpha()
        resize = c.windowLength/worldMap.get_width()
        w = int(resize * worldMap.get_width())
        h = int(resize * worldMap.get_height())
        worldMap = pygame.transform.scale(worldMap, (w, h))

        #Player HUD
        barre = pygame.image.load(c.imagePath + c.bareImage).convert_alpha()
        barre = pygame.transform.scale(barre, (c.windowLength, c.windowWidth - h))

        self.functions = []
        self.surfaces.extend([[background, (0, 0)], [barre, (0, h)], [worldMap, (0, 0)]])

    # Method utilizes overlay methods to update pygameWindow
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


        # Format territory sprites and add to surface
        for i, j in enumerate(worldTerritories):
            surface = pygame.image.load(j).convert()
            resize = c.windowLength/surface.get_width()
            
            surface = pygame.transform.scale(surface, (int(resize * surface.get_width()), int(resize * surface.get_height())))
            
            territorySprite = Sprites(surface, j)
            initialSpriteLayer = Sprites(surface.copy(), j)
            
            setSurfaceColor(initialSpriteLayer, (1, 1, 1), 150)
            territorySprites.append(territorySprite)
            highlightedTerritories.append(initialSpriteLayer)

        # Creates final layer of all connected sprites
        self.colorTerritories(territorySprites)
        for i, j in enumerate(territorySprites):
            if i == 0:
                finalLayout = j.layout.copy()
            else:
                finalLayout.blit(j.layout, (0, 0))

        # Update visual troop numbers
        troopDisplay(self.textList, territorySprites, self.map)

        # Event handler
        while (not gameEnd):
            for event in pygame.event.get(): #Checks every mouse and key action in window
                if event.type == QUIT:
                    print("Ending game!")
                    gameEnd = True

                # Handling key presses
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE: #Exit program on key press
                        print("Ending game!")
                        gameEnd = True
                        
##                      #SAVING BROKEN... TO BE REMOVED
##                    elif event.key == K_k: #Save game and exit
##                        tempSave = []
##                        tempSave.append(self.map) #Map data saved in state 0
##                        tempSave.append(self.players) #Player data saved in state 1
##                        tempSave.append(self.Turn) #Turn data saved in state 2 ..etc
##                        tempSave.append(self.numTroops)
##                        tempSave.append(self.selectedTerritory)
####                        tempSave.append(self.interfaceDice) #surface obj cannot be saved
##                        tempSave.append(self.functions)
####                        tempSave.append(self.surfaces) #surface obj cannot be saved
####                        tempSave.append(self.tempTerritoryList) #surface obj cannot be saved
####                        tempSave.append(self.textList) #surface obj cannot be saved
##                        tempSave.append(self.topLevel)
##                        saveGame(tempSave)
##
##        
##                    elif event.key == K_l: #Restore saved game
##                        loadData = loadGame(tempSave)
##                        self.map = loadData[0]
##                        self.players = loadData[1]
##                        self.Turn = loadData[2]
##                        self.numTroops = loadData[3]
##                        self.selectedTerritory = loadData[4]
####                        self.interfaceDice = loadData[5]
##                        self.functions = loadData[5]
####                        self.surfaces = loadData[7]
####                        self.tempTerritoryList = loadData[8]
####                        self.textList = loadData[9]
##                        self.topLevel = loadData[6]
                        
                    elif event.key == K_n: #Proceed to next round
                        try:
                            self.Turn.next()
                        except ValueError as e:
                            print(e.args)

                        self.tempTerritoryList = [] #Resets selected territory for next player
                        selectFlag = False
                        selectedTerritory = 0

                    elif event.key == K_h: #Help screen
                        helpFlag = not helpFlag
                        
                # Handling mouse-clicks/scrolls                
                elif event.type == MOUSEBUTTONDOWN:
                    try:
                        if event.button == 3: #Right mouse-click to unselect (selected) territory
                            self.tempTerritoryList = []
                            selectFlag = False
                            selectedTerritory = 0
                            
                        elif event.button == 4: #Scroll mousewheel down to increase selected troops
                            self.troopCount += 1
                            
                        elif event.button == 5: #Scroll mousewheel down to decrease selected troops
                            if self.troopCount > 0:
                                self.troopCount -= 1
                                
                    except AttributeError as e:
                        print("You should select a country first ...")
                    except ValueError as e:
                        print(e.args)

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

            # Shows victory screen if player completes domination goal
            if self.Turn.players[self.Turn.turnCount - 1].obj.getGoalStatus() == True:
                self.topLevel = []
                
                topLayer = pygame.Surface(self.pygameWindow.get_size())
                topLayer = topLayer.convert()
                topLayer.fill(c.black)
                topLayer.set_alpha(180)
                
                self.topLevel.append([topLayer, (0,0)])
                display_win(self.topLevel,self.players)

            # Uses same top layer to contain help screen
            else:
                if helpFlag:
                    self.topLevel=[]
                    
                    topLayer = pygame.Surface(self.pygameWindow.get_size())
                    topLayer = topLayer.convert()
                    topLayer.fill(c.black)
                    topLayer.set_alpha(180)
                    
                    self.topLevel.append([topLayer, (0,0)])
                    display_help(self.topLevel)
                else:
                    self.topLevel=[]

            # Highlight territories as cursor moves over them
            mouse = pygame.mouse.get_pos()
            try:
                tempColorValue=self.surfaces[2][0].get_at((mouse[0], mouse[1]))
            except IndexError as e:
                pass
            
            # Setups user GUI layout and enables player functions
            try:
                if tempColorValue != (0,0,0,0) and tempColorValue != (0,0,0,255):
                    temptroopValID = tempColorValue[0] - 100
                    spriteLayer = next((territorySprite for territorySprite in highlightedTerritories if territorySprite.id == temptroopValID), None)

                    # Update selected territory visuals
                    if temptroopValID != selectedTerritory:
                        self.pygameWindow.blit(spriteLayer.layout, (0, 0))
                        pygame.display.update(spriteLayer.layout.get_rect())

                    # On click, check phase and territory function validity
                    click = pygame.mouse.get_pressed()

                    # Placing reinforcements on owned territories
                    if self.Turn.list_phase[self.Turn.phase] == "Placement":
                        if click[0] == 1:
                            playerTerritory = next((p for p in self.map.territories if p.id == temptroopValID), None) 
                            if playerTerritory.id_player == self.Turn.turnCount:
                                self.Turn.placeTroops(playerTerritory, self.troopCount)
                                pygame.time.wait(100)
                            else:
                                print("This territory does not belong to the player!")

                    # Attacking neighboring territories with n-1 troops
                    elif self.Turn.list_phase[self.Turn.phase] == "Attack":
                        if click[0] == 1 and not selectFlag:
                            startTerritory = next((p for p in self.map.territories if p.id == temptroopValID), None)
                            self.selectedTerritory = startTerritory
                            if startTerritory.id_player == self.Turn.turnCount and startTerritory.nb_troupes > 1:
                                self.troopCount = startTerritory.nb_troupes-1
                                self.tempTerritoryList.append(spriteLayer.layout)
                                selectFlag = True 
                                selectedTerritory = temptroopValID
                                
                        elif click[0] == 1: # Selecting territory to attack
                            endTerritory = next((p for p in self.map.territories if p.id == temptroopValID), None)
                            if attackFlag and endTerritory == targetTerritory and startTerritory.nb_troupes > 1:
                                self.Turn.troopMovement(startTerritory, endTerritory, self.troopCount)
                                selectFlag = False
                                self.tempTerritoryList = []
                                attackFlag = False
                                
                            elif attackFlag: 
                                selectFlag = False
                                self.tempTerritoryList = []
                                attackFlag  = False
                                
                            elif endTerritory.id_player != self.Turn.turnCount and endTerritory.id in startTerritory.voisins: #Attack with home troops
                                try:
                                    self.interfaceDice = []                           
                                    attackResult, diceResults = self.Turn.attack(startTerritory, endTerritory, self.troopCount)
                                    for i,res in enumerate(diceResults):
                                        diceRolls(self, res[0], res[2], 600, territorySprites[0].layout.get_height() + 10 + i * c.diceSize * 1.1)
                                        diceRolls(self, res[1], res[3], 800, territorySprites[0].layout.get_height() + 10 + i * c.diceSize * 1.1)
                                    pygame.time.wait(100)
                                except ValueError as e:
                                    print(e.args)
                                    attackResult = False
                                    selectFlag = False
                                    self.tempTerritoryList = []
                                if attackResult: #On successful attack, update visuals
                                    sprite = next((s for s in territorySprites if s.id == temptroopValID), None)
                                    setSurfaceColor(sprite, self.Turn.players[self.Turn.turnCount - 1].color, 255)
                                    finalLayout.blit(sprite.layout,(0,0))
                                    attackFlag = True
                                    targetTerritory = endTerritory
                                    self.troopCount = startTerritory.nb_troupes - 1
                                else:
                                    selectFlag = False
                                    self.tempTerritoryList = []

                    # Moving troops between territories
                    elif self.Turn.list_phase[self.Turn.phase] == "Movement":
                        if click[0] == 1 and not selectFlag: #On left click select territory
                            startTerritory = next((p for p in self.map.territories if p.id == temptroopValID), None)
                            self.selectedTerritory = startTerritory
                            if startTerritory.id_player == self.Turn.turnCount and startTerritory.nb_troupes > 1:
                                self.troopCount = startTerritory.nb_troupes - 1
                                self.tempTerritoryList.append(spriteLayer.layout)
                                selectFlag = True 
                                selectedTerritory = temptroopValID
                                
                        elif click[0] == 1: #On right click unselect territory
                            endTerritory = next((p for p in self.map.territories if p.id == temptroopValID), None)
                            path = self.map.checkPathValid(self.Turn.players[self.Turn.turnCount - 1].territories, startTerritory, endTerritory)
                            selectFlag = False
                            selectedTerritory = 0
                            self.tempTerritoryList = []
                            
                            if path and endTerritory.id != startTerritory.id:
                                self.Turn.troopMovement(startTerritory, endTerritory, self.troopCount)
                                self.Turn.next()
                                
                    # Update troop text overlay visuals
                    self.textList = []
                    troopDisplay(self.textList, territorySprites, self.map)
                    
            except ValueError as e:
                pass

            # Update HUD text visuals
            self.interfaceText = []
            display_hud(self.troopCount, self.interfaceText, self.Turn, (75, territorySprites[0].layout.get_height() + 10))
            pygame.display.flip()



# Returns information for text handling
def textArea(text, font, color = (0, 0, 0)):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


# Creates clickable area for mouse interactions and overlays with text
def button(txt, xPos, yPos, width, height, ic, ac, command = None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if xPos + width > mouse[0] > xPos and yPos + height > mouse[1] > yPos:
        pygame.draw.rect(pygameWindow, ac,(xPos, yPos, width, height))
        if click[0] == 1 and action != None:
            Win.functions.append(action)
    else:
        pygame.draw.rect(pygameWindow, ic,(xPos, yPos, width, height))

    smallText = pygame.font.Font(None, 20)
    textSurface, textBox = textArea(txt, smallText)
    textBox.center = ((xPos + (w/2)), (yPos + (height/2)))
    
    pygameWindow.blit(textSurface, textBox)


# Sets sprite overlay colors
def setSurfaceColor(sprite, color, alpha):
    for x in range(0, sprite.bounds.width):
        for y in range(0, sprite.bounds.height):
            if sprite.layout.get_at((sprite.bounds.x + x, sprite.bounds.y + y)) != (0, 0, 0):
                sprite.layout.set_at((sprite.bounds.x + x, sprite.bounds.y + y), color)
                sprite.layout.set_alpha(alpha)


# Update troop visual count
def troopDisplay(textList, sprites, Map):
    smallText = pygame.font.Font(None, 25)
    for sprite in sprites:
        territories = Map.territories[sprite.id-1]
        textSurface, textBox = textArea(str(territories.nb_troupes), smallText)
        textBox.center = sprite.bounds.center
        textList.append([textSurface, textBox])


# Player victory screen if a player completes goals
def display_win(topLevel, players):
    largeText = pygame.font.Font(None, 75)
    margin = 50
    textPosition = (200, 200)
    for p in players:
        if p.obj.getGoalStatus() == True:
            winnerPlayer = p
            textSurface, textBox = textArea(winnerPlayer.name + " wins!", largeText, winnerPlayer.color)
            textBox.topleft = textPosition
            textPosition = (textPosition[0], textPosition[1] + margin)
            topLevel.append([textSurface, textBox])


# Adds text to top layer for help screen
def display_help(topLevel):
    largeText = pygame.font.Font(None, 50)
    margin = 50
    textPosition = (200, 200)

    textSurface, textBox = textArea("'h' key: Help", largeText, c.white)
    textBox.topleft = textPosition
    topLevel.append([textSurface, textBox])
    textPosition = (textPosition[0],textPosition[1]+margin)
    
    textSurface, textBox = textArea("Left/Right Mouse-click : Select/Deselect Territory", largeText, c.white)
    textBox.topleft = textPosition
    topLevel.append([textSurface, textBox])
    textPosition = (textPosition[0], textPosition[1] + margin)

    textSurface, textBox = textArea("Scroll Wheel Up/Down : Increase/Decrease Troop Selection", largeText, c.white)
    textBox.topleft = textPosition
    topLevel.append([textSurface, textBox])
    textPosition = (textPosition[0], textPosition[1] + margin)
    
    textSurface, textBox = textArea("'n' key: Next phase", largeText, c.white)
    textBox.topleft = textPosition
    topLevel.append([textSurface, textBox])
    textPosition = (textPosition[0], textPosition[1] + margin)

##    textSurface, textBox = textArea("'k' key: Save game [TODO]", largeText, c.white)
##    textBox.topleft = textPosition
##    topLevel.append([textSurface, textBox])
##    textPosition = (textPosition[0], textPosition[1] + margin)
##
##    textSurface, textBox = textArea("'l' key: Load game [TODO]", largeText, c.white)
##    textBox.topleft = textPosition
##    topLevel.append([textSurface, textBox])
##    textPosition = (textPosition[0], textPosition[1] + margin)

    textSurface, textBox = textArea("'esc' key: quit", largeText, c.white)
    textBox.topleft = textPosition
    topLevel.append([textSurface, textBox])
    textPosition = (textPosition[0], textPosition[1] + margin)



# Player interface text updates
def display_hud(troopCount, interfaceText, Turn, textPosition):
    smallText = pygame.font.Font(None, 25)
    margin = 20
    col = [100, 400, 700, 1000]
    row = textPosition[1]


    # FIRTS COLUMN TEXT        ... position carries over to next
    textSurface, textBox = textArea("Round : " + str(Turn.num), smallText)
    textBox.topleft = (textPosition[0], textPosition[1])
    interfaceText.append([textSurface, textBox])

    textSurface, textBox = textArea("Phase : " + Turn.list_phase[Turn.phase], smallText)
    textPosition = (textPosition[0], textPosition[1] + margin + margin)
    textBox.topleft = textPosition
    interfaceText.append([textSurface, textBox])
    
    textSurface, textBox = textArea("Player : ",smallText)
    textPosition = (textPosition[0], textPosition[1] + margin + margin)
    textBox.topleft = textPosition
    interfaceText.append([textSurface, textBox])

    #name value
    textSurface, textBox = textArea(Turn.players[Turn.turnCount -1 ].name, smallText, Turn.players[Turn.turnCount - 1].color)
    textBox.topleft = (textPosition[0] + 70, textPosition[1])
    interfaceText.append([textSurface, textBox])
    

    # MIDDLE COLUMN TEXT    
    textSurface, textBox = textArea("Number of Selected Troops : " + str(troopCount), smallText)
    textPosition = (textPosition[0] + 200, textPosition[1])
    textBox.topleft = textPosition
    interfaceText.append([textSurface, textBox])
    
    textSurface, textBox = textArea("Available number of troops to deploy : " + str(Turn.players[Turn.turnCount - 1].nb_troupes), smallText)
    textPosition = (textPosition[0], textPosition[1] - margin - margin)
    textBox.topleft = textPosition
    interfaceText.append([textSurface, textBox])

    textSurface, textBox = textArea("Troops per turn : " + str(Turn.players[Turn.turnCount - 1].sbyturn), smallText)
    textPosition = (textPosition[0], textPosition[1] - margin - margin)
    textBox.topleft = textPosition
    interfaceText.append([textSurface, textBox])
    

# Updates dice visuals and shows respective losses as a column
def diceRolls(gameInstance, troopLosses, numDies, xPos, yPos):
    tempDiceLayer = []
    for i, j in enumerate(numDies): #Gets correct die sprite and resizes
        dieSprite = pygame.image.load(c.dicePath + str(j) + ".png").convert_alpha()
        resizeSprite = pygame.transform.scale(dieSprite, (c.diceSize, c.diceSize))
        tempDiceLayer.append([resizeSprite, gameInstance.pygameWindow.blit(resizeSprite, (i * c.diceSize * 1.1 + xPos, yPos))])

    for deaths in range(0, troopLosses): #Gets tombstome sprite to represent losses in a row
        tombstoneSprite = pygame.image.load(c.imagePath + c.deadImage).convert_alpha()
        resizeSprite = pygame.transform.scale(tombstoneSprite, (c.diceSize, c.diceSize))
        tempDiceLayer.append([resizeSprite, gameInstance.pygameWindow.blit(resizeSprite, (xPos - (deaths + 1) * c.diceSize * 1.1, yPos))])

    gameInstance.interfaceDice.extend(tempDiceLayer) 

#### CANNOT SAVE SURFACE...
### Save and restore game state using pickle
##def saveGame(save):
##    with open("saved_game", "wb") as l: #DOES NOT WORK
##        print("Game has been saved")
##        pickle.dump(save, l)
##
##
##def loadGame(save):
##    with open("saved_game","rb") as l:
##        print("Save has been loaded")
##        save = pickle.load(l)


# Secondary run, used for debugging
if __name__ == "__main__":
    from tkinter import *
    import random
    import copy
    
    from Map import Map
    from Player import Player
    from Card import Card
    from Turn import Turn

    import Constants as c

    # Run risk with set player params
    tempMap = Map()
    
    turn = Turn(3, tempMap) # Turn object created given number players and map object
    turn.initialTroops() # Sets starting troops, varies depending on number of players
    turn.distributeTerritories(tempMap.territories) # Distributes territories to players from map list

    Continents = tempMap.continents

    # Initialize players
    turn.players[0].color = c.riskRed #c.red
    turn.players[1].color = c.riskGreen #c.green
    turn.players[2].color = c.riskBlue #c.blue
##    turn.players[3].color = c.yellow
##    turn.players[4].color = c.purple
##    turn.players[5].color = c.teal
    
    turn.players[0].name = "Duncan"
    turn.players[1].name = "Isaac"
    turn.players[2].name = "Lily"
##    turn.players[3].name = "Finn"
##    turn.players[4].name = "Anna"
##    turn.players[5].name = "Brianna"

    # Setup and start pygame
    pygame.init()
    pygameWindow = pygame.display.set_mode((c.windowLength, c.windowWidth))


        




    # Create instance of Game to contain risk objects
    try:
        gameInstance = Game(pygameWindow, turn)
        
##        # User in game menu until button click
##        displayFlag = False
##        while (not displayFlag):
##            gameInstance.functions.append(gameInstance.menu)
##            gameInstance.display()
            
        gameInstance.functions.append(gameInstance.run)
        gameInstance.display()
    except UnboundLocalError:
        print("Colorization of map error, restart game and try again!")


        
