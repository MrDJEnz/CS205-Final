import sys
import pygame #may need to install using (pip install pygame)
import glob
import  pickle
from pygame.locals import *
#https://commons.wikimedia.org/wiki/File:Risk_board.svg
#paths to draw islands

class Colors():
    def __init__(self):
        self.red=(255,0,0)
        self.green=(0,255,0)
        self.blue=(0,0,255)
        self.white=(255,255,255)
        self.black=(0,0,0)
        self.grey = (100, 100, 100)
        self.yellow = (255, 255, 0)
        self.purple = (255, 0, 255)
        self.cian = (0, 255, 255)
        self.dark_purple = (127, 0, 255)
        self.dark_green = (0, 170, 0)
        self.dark_red = (170, 0, 0)
        self.dark_blue = (0, 0, 170)
        
if __name__ == "__main__":
    pygame.init()
    freshStart = True #for initializing map animation
    
    #window display, size, caption
    display = pygame.display.set_mode((720,450))
    pygame.display.set_caption("Risk (GAME WINDOW)")
    
   # background = pygame.image.load("Map/green.jpg").convert()
   # background = pygame.transform.scale(background, (720, 450)) #resize green image 

   # display.blit(background, (0,0)) #sets first green background element
    i = 0
    #loop continuously check and updates "event"
    while True:
        for event in pygame.event.get(): #get and process events
           # if freshStart == True: #display map initialization animation
                #t1 = pygame.image.load("map/green.jpg").convert()
                #t1 = pygame.transform.scale(background, (720, 450))
               # i = 0
               ## for i in range(41):
                ##    territory = pygame.image.load("map/" + str(i) + ".png").convert()
                ##    territory = pygame.transform.scale(territory, (70, 40))
                ##    display.blit(territory, (70,40))
               ##     i += 1

             #   freshStart = False
            
            if event.type == pygame.MOUSEBUTTONDOWN: #check of user pressed button
                print("mouse down, displaying country", str(i))
                i+=1
                #territory = pygame.image.load("map/" + str(i) + ".png").convert()
                #territory = pygame.transform.scale(territory, (70, 40))
                #i += 1
                
            if event.type == QUIT: #check if user wants to quit
                pygame.quit()
                sys.exit()
######
        territory = pygame.image.load("Map/" + str(i) + ".png").convert()
        territory = pygame.transform.scale(territory, (720, 450))
        display.blit(territory, (0,0))
#####        
        pygame.display.update()
        
