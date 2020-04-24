import sys
import pygame #may need to install using (pip install pygame)
import glob
import  pickle
from pygame.locals import *
import time
#https://commons.wikimedia.org/wiki/File:Risk_board.svg
#paths to draw islands
from Game import Game
import Constants as c


from tkinter import *
import random
import copy
    
from Map import Map
from Player import Player
from Card import Card
from Turn import Turn
    
pygame.init()

#can use constants file##
red=(255,0,0)
green=(0,255,0)
blue=(0,0,255)
white=(255,255,255)
black=(0,0,0)
grey = (100, 100, 100)
yellow = (255, 255, 0)
purple = (255, 0, 255)
cian = (0, 255, 255)
dark_purple = (127, 0, 255)
dark_green = (0, 170, 0)
dark_red = (170, 0, 0)
dark_blue = (0, 0, 170)
#####

font = pygame.font.SysFont(None, 50)

fpsClock = pygame.time.Clock()



def message_to_screen(msg,color, gameDisplay):
    screen_text = font.render(msg, True, color)
    gameDisplay.blit(screen_text, [c.windowLength/2, c.windowWidth/2])

def menu(MENUSTAT, screen, clock, background1):
    playButton = pygame.image.load(c.imagePath + c.playButton)
    helpButton = pygame.image.load(c.imagePath + c.helpButton)
    exitButton = pygame.image.load(c.imagePath + c.exitButton)

    mouse = pygame.mouse.get_pos() #get mouse position

    #add button images

    animateMenuX = 0 #start menu pos at x    
    while MENUSTAT == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:

                    #on mouse click check position
                    #if mouse == ((100, 200)):
                    print("Moving to running game")
                    menu = False
                    running = True

                    #prep load screen while game inits
                    loadScreen = pygame.image.load(c.imagePath + c.loadingImage)
                    formattedLoadScreen = pygame.transform.scale(loadScreen, (c.windowLength, c.windowWidth))
                    screen.blit(formattedLoadScreen, (0, 0))
                    pygame.display.update() #update visuals
                        
                    game(running, screen, background1, clock)

        screen.fill((0, 0, 0))
        clock.tick(30)
        black = (0, 0, 0)
        
        #menu animation
        menu = pygame.transform.scale(background1, (int(c.windowLength * 1.3), c.windowWidth)) #zoom in on bg

        formattedPlayButton = pygame.transform.scale(playButton, (100, 50)) #size change
        formattedHelpButton = pygame.transform.scale(helpButton, (100, 50)) #size change
        formattedExitButton = pygame.transform.scale(exitButton, (100, 50)) #size change

##        message_to_screen("Players: ", red, screen)


        #button stuff

##        # Creates clickable area for mouse interactions and overlays with text
##def button(txt, xPos, yPos, width, height, ic, ac, command = None):
##    mouse = pygame.mouse.get_pos()
##    click = pygame.mouse.get_pressed()
##    if xPos + width > mouse[0] > xPos and yPos + height > mouse[1] > yPos:
##        pygame.draw.rect(pygameWindow, ac,(xPos, yPos, width, height))
##        if click[0] == 1 and action != None:
##            Win.functions.append(action)
##    else:
##        pygame.draw.rect(pygameWindow, ic,(xPos, yPos, width, height))
##
##    smallText = pygame.font.Font(None, 20)
##    textSurface, textBox = textArea(txt, smallText)
##    textBox.center = ((xPos + (w/2)), (yPos + (height/2)))
##    
##    pygameWindow.blit(textSurface, textBox)


        
##               # Handling mouse-clicks/scrolls                
##                elif event.type == MOUSEBUTTONDOWN:
##                    try:
##                        if event.button == 3: #Right mouse-click to unselect (selected) territory
##                            self.tempTerritoryList = []
##                            selectFlag = False
##                            selectedTerritory = 0
##                            
##                        elif event.button == 4: #Scroll mousewheel down to increase selected troops
##                            self.troopCount += 1
##                            
##                        elif event.button == 5: #Scroll mousewheel down to decrease selected troops
##                            if self.troopCount > 0:
##                                self.troopCount -= 1
    
        
        screen.blit(menu, (animateMenuX, 0)) #add to layer starting left top corner position
        screen.blit(formattedPlayButton, (c.windowLength - int(c.windowLength/2) - 250, c.windowWidth - int(c.windowWidth/5)))
        screen.blit(formattedHelpButton, (c.windowLength - int(c.windowLength/2), c.windowWidth - int(c.windowWidth/5))) #middle
        screen.blit(formattedExitButton, (c.windowLength - int(c.windowLength/2) + 250, c.windowWidth - int(c.windowWidth/5)))

        pygame.display.update() #update visuals
        fpsClock.tick(30)
        
        animateMenuX -= 0.5
        if animateMenuX <= -400:
            animateMenuX = 0


def game(running, screen, background1, clock):


    # Run risk with set player params
    tempMap = Map()
    
    turn = Turn(3, tempMap) # Turn object created given number players and map object
    turn.initialTroops() # Sets starting troops, varies depending on number of players
    turn.distributeTerritories(tempMap.territories) # Distributes territories to players from map list

    Continents = tempMap.continents

    # Initialize players
    turn.players[0].color = c.red
    turn.players[1].color = c.green
    turn.players[2].color = c.blue
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


##    # display.blit(background, (0,0)) #sets first green background element
##    i = 0
##    # loop continuously check and updates "event"
##    screen = pygame.display.set_mode((c.windowLength, c.windowWidth))
##    while running:
##        # screen.fill((0, 0, 0))
##        #
##        # # screen.blit(background1)
##
##        for event in pygame.event.get():  # get and process events
##            # if freshStart == True: #display map initialization animation
##            # t1 = pygame.image.load("map/green.jpg").convert()
##            # t1 = pygame.transform.scale(background, (720, 450))
##            # i = 0
##            ## for i in range(41):
##            ##    territory = pygame.image.load("map/" + str(i) + ".png").convert()
##            ##    territory = pygame.transform.scale(territory, (70, 40))
##            ##    display.blit(territory, (70,40))
##            ##     i += 1
##
##            #   freshStart = False
##
##            if event.type == pygame.MOUSEBUTTONDOWN:  # check of user pressed button
##                print("mouse down, displaying country", str(i))
##                i += 1
##                # territory = pygame.image.load("map/" + str(i) + ".png").convert()
##                # territory = pygame.transform.scale(territory, (70, 40))
##                # i += 1
##            elif event.type == pygame.KEYDOWN:
##                if event.key == pygame.K_p:
##                    MENUSTAT = True
##                    menu(MENUSTAT, screen, clock, background1)
##
##            if event.type == QUIT:  # check if user wants to quit
##                pygame.quit()
##                sys.exit()
####            ######
####            territory = pygame.image.load("src/" + str(i) + ".png").convert()
####            territory = pygame.transform.scale(territory, (c.windowLength, c.windowWidth))
####            screen.blit(territory, (0, 0))
####            #####
##                
##            #INIT GAME*
##
##            pygame.display.update()

def start():

    freshStart = True  # for initializing map animation
    running = True
    MENUSTAT = True
    game = False

    # window display, size, caption
    screen = pygame.display.set_mode((c.windowLength, c.windowWidth))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Risk (GAME WINDOW)")
    # Background Image
##    background1 = pygame.image.load("Pictures/menu background.jpg")

    background1 = pygame.image.load(c.imagePath + c.menuBackgroundImage)

    # background = pygame.image.load("Map/green.jpg").convert()
    # background = pygame.transform.scale(background, (720, 450)) #resize green image
    menu(MENUSTAT, screen, clock, background1)

if __name__ == "__main__":
    start()


        
