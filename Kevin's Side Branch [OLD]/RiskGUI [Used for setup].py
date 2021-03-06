import sys
import os
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

# highlight surfaces making buttons interactive
def colorSurface(surface, r, g, b):
    arr = pygame.surfarray.pixels3d(surface)
    arr[:,:,0] = red
    arr[:,:,1] = green
    arr[:,:,2] = blue

# Returns information for text handling
def textArea(text, font, color = (0, 0, 0)):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def settings(SETTINGSTAT, screen, clock, exitButton):
    
    # flag true for options
    while SETTINGSTAT == True:
        mouse = pygame.mouse.get_pos()
        currentMouseX = mouse[0]
        currentMouseY = mouse[1]


        #button visual and function
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:

                #on right click on help (OPTIONS should rename latre)
                if (event.button == 1) and ((c.windowLength - int(c.windowLength/2)) < currentMouseX < (c.windowLength - int(c.windowLength/2) + 100)) and ((c.windowWidth - int(c.windowWidth/5)) < currentMouseY < (c.windowWidth - int(c.windowWidth/5) + 50)):
                    print("returning to menu")
                    SETTINGSTAT = False


        #load settings screen
        settingsScreen = pygame.image.load(c.imagePath + c.settingsImage)
        formattedSettingsScreen = pygame.transform.scale(settingsScreen, (c.windowLength, c.windowWidth))
        formattedExitButton = pygame.transform.scale(exitButton, (100, 50)) #size change


        screen.blit(formattedSettingsScreen, (0, 0))

        #create text
        margin = 100
        tempText = pygame.font.Font(None, 50)
        textPosition = (int(c.windowLength/5), margin)
        textSurface, textBox = textArea("In Risk you must conquer all the territories to win.", tempText, c.white)
        textBox.topleft = textPosition
        screen.blit(textSurface, textBox)

        textPosition = (int(c.windowLength/5), margin + 100)
        textSurface, textBox = textArea("Players will be given set troops and starting territories.", tempText, c.white)
        textBox.topleft = textPosition
        screen.blit(textSurface, textBox)
        
        textPosition = (int(c.windowLength/5), margin + 200)
        textSurface, textBox = textArea("Use the 'h' key ingame for control help ... Good Luck.", tempText, c.white)
        textBox.topleft = textPosition
        screen.blit(textSurface, textBox)


        
        if ((c.windowLength - int(c.windowLength/2)) < currentMouseX < (c.windowLength - int(c.windowLength/2) + 100)) and ((c.windowWidth - int(c.windowWidth/5)) < currentMouseY < (c.windowWidth - int(c.windowWidth/5) + 50)):
            screen.blit(formattedExitButton, (c.windowLength - int(c.windowLength/2), c.windowWidth - int(c.windowWidth/5)), special_flags = pygame.BLEND_RGBA_MULT) #middle
        else:
            screen.blit(formattedExitButton, (c.windowLength - int(c.windowLength/2), c.windowWidth - int(c.windowWidth/5))) #middle

             
        pygame.display.update() #update visuals
        fpsClock.tick(30)


        

def menu(MENUSTAT, screen, clock, background1):
    #origional
    playButton = pygame.image.load(c.imagePath + c.playButton)
##    playButton = playButton.convert_alpha()
##    playButtonAlt = pygame.Surface(playButton.get_rect().size, pygame.SRCALPHA)
##    playButtonAlt.fill((200, 200, 200, 100)) #r, g, b, alpha
    
    helpButton = pygame.image.load(c.imagePath + c.helpButton)
    exitButton = pygame.image.load(c.imagePath + c.exitButton)
    
    
##    #highlighted
##    playButtonAlt = playButton.copy()
##    colorSurface(playButtonAlt, 120, 78, 240)
##    
##    helpButtonAlt = helpButton.copy()
##    
##    exitButtonAlt = exitButton.copy()

    #maybe need origionalSurface.convert_alpha()
##coloredSurface = origSurface.copy()
##color_surface(coloredSurface, 120, 78, 240)
    animateMenuX = 0 #start menu pos at x    
    while MENUSTAT == True:
        mouse = pygame.mouse.get_pos() #get mouse position

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #on right click on play
                if (event.button == 1) and ((c.windowLength - int(c.windowLength/2) - 250) < currentMouseX < (c.windowLength - int(c.windowLength/2) - 150)) and ((c.windowWidth - int(c.windowWidth/5)) < currentMouseY < (c.windowWidth - int(c.windowWidth/5) + 50)):
                    print("Starting game ...")
                    menu = False
                    running = True

                    #prep load screen while game inits
                    loadScreen = pygame.image.load(c.imagePath + c.loadingImage)
                    formattedLoadScreen = pygame.transform.scale(loadScreen, (c.windowLength, c.windowWidth))
                    screen.blit(formattedLoadScreen, (0, 0))
                    pygame.display.update() #update visuals

                    game(running, screen, background1, clock)

                #on right click on help (OPTIONS should rename latre)
                elif (event.button == 1) and ((c.windowLength - int(c.windowLength/2)) < currentMouseX < (c.windowLength - int(c.windowLength/2) + 100)) and ((c.windowWidth - int(c.windowWidth/5)) < currentMouseY < (c.windowWidth - int(c.windowWidth/5) + 50)):
                    print("opening options ...")
                    settings(True, screen, clock, helpButton)

                #show help/setuup screen ? then go back to menu screen
                #on right click on exit
                elif (event.button == 1) and ((c.windowLength - int(c.windowLength/2) + 250) < currentMouseX < (c.windowLength - int(c.windowLength/2) + 350)) and ((c.windowWidth - int(c.windowWidth/5)) < currentMouseY < (c.windowWidth - int(c.windowWidth/5) + 50)):
                    print("Shutting down ...")
                    os._exit(0) #clean exit


        screen.fill((0, 0, 0))
        clock.tick(30)
        black = (0, 0, 0)

        #menu animation
        menu = pygame.transform.scale(background1, (int(c.windowLength * 1.3), c.windowWidth)) #zoom in on bg

        formattedPlayButton = pygame.transform.scale(playButton, (100, 50)) #size change
        formattedHelpButton = pygame.transform.scale(helpButton, (100, 50)) #size change
        formattedExitButton = pygame.transform.scale(exitButton, (100, 50)) #size change

##        message_to_screen("Players: ", red, screen)

        screen.blit(menu, (animateMenuX, 0)) #add to layer starting left top corner position
        screen.blit(formattedPlayButton, (c.windowLength - int(c.windowLength/2) - 250, c.windowWidth - int(c.windowWidth/5)))
        screen.blit(formattedHelpButton, (c.windowLength - int(c.windowLength/2), c.windowWidth - int(c.windowWidth/5))) #middle
        screen.blit(formattedExitButton, (c.windowLength - int(c.windowLength/2) + 250, c.windowWidth - int(c.windowWidth/5)))
        

        # check mouse pos and highlight button when mouse hovers above
        currentMouseX = mouse[0]
        currentMouseY = mouse[1]

        #if lowerbound < mousepos < higher bound and for y.. do button
        #difference is button size formatted
        if ((c.windowLength - int(c.windowLength/2) - 250) < currentMouseX < (c.windowLength - int(c.windowLength/2) - 150)) and ((c.windowWidth - int(c.windowWidth/5)) < currentMouseY < (c.windowWidth - int(c.windowWidth/5) + 50)):
            screen.blit(formattedPlayButton, (c.windowLength - int(c.windowLength/2) - 250, c.windowWidth - int(c.windowWidth/5)), special_flags = pygame.BLEND_RGBA_MULT)
        elif ((c.windowLength - int(c.windowLength/2)) < currentMouseX < (c.windowLength - int(c.windowLength/2) + 100)) and ((c.windowWidth - int(c.windowWidth/5)) < currentMouseY < (c.windowWidth - int(c.windowWidth/5) + 50)):
            screen.blit(formattedHelpButton, (c.windowLength - int(c.windowLength/2), c.windowWidth - int(c.windowWidth/5)), special_flags = pygame.BLEND_RGBA_MULT) #middle
        elif ((c.windowLength - int(c.windowLength/2) + 250) < currentMouseX < (c.windowLength - int(c.windowLength/2) + 350)) and ((c.windowWidth - int(c.windowWidth/5)) < currentMouseY < (c.windowWidth - int(c.windowWidth/5) + 50)):
            screen.blit(formattedExitButton, (c.windowLength - int(c.windowLength/2) + 250, c.windowWidth - int(c.windowWidth/5)), special_flags = pygame.BLEND_RGBA_MULT)


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
    turn.players[0].color = c.riskRed
    turn.players[1].color = c.riskGreen
    turn.players[2].color = c.riskBlue
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

    #fix for error?
    # Create instance of Game to contain risk objects
    try:
        gameInstance = Game(pygameWindow, turn)
            
        gameInstance.functions.append(gameInstance.run)
        gameInstance.display()
    except UnboundLocalError:
        print("Your troops are being trained, please wait...")
        print("Try moving the moving your mouse cursor onto the man's nose while you wait?")

        game(running, screen, background1, clock)


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


        
