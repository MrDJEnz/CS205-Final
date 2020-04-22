import sys
import pygame #may need to install using (pip install pygame)
import glob
import  pickle
from pygame.locals import *
import time
#https://commons.wikimedia.org/wiki/File:Risk_board.svg
#paths to draw islands

pygame.init()
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


font = pygame.font.SysFont(None, 50)
game_height = 1080
game_width = 1920




def message_to_screen(msg,color, gameDisplay):
    screen_text = font.render(msg, True, color)
    gameDisplay.blit(screen_text, [game_width/2, game_height/2])

def menu(MENUSTAT, screen, clock, background1):
    while MENUSTAT == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    print("Moving to running game")
                    menu = False
                    running = True
                    game(running, screen, background1, clock)

        screen.fill((0, 0, 0))
        clock.tick(30)
        black = (0, 0, 0)
        menu = pygame.transform.scale(background1, (game_width, game_height))
        message_to_screen("Players: ", red, screen)
        screen.blit(menu, (0, 0))

        pygame.display.update()


def game(running, screen, background1, clock):
    # display.blit(background, (0,0)) #sets first green background element
    i = 0
    # loop continuously check and updates "event"
    screen = pygame.display.set_mode((game_width, game_height))
    while running:
        # screen.fill((0, 0, 0))
        #
        # # screen.blit(background1)

        for event in pygame.event.get():  # get and process events
            # if freshStart == True: #display map initialization animation
            # t1 = pygame.image.load("map/green.jpg").convert()
            # t1 = pygame.transform.scale(background, (720, 450))
            # i = 0
            ## for i in range(41):
            ##    territory = pygame.image.load("map/" + str(i) + ".png").convert()
            ##    territory = pygame.transform.scale(territory, (70, 40))
            ##    display.blit(territory, (70,40))
            ##     i += 1

            #   freshStart = False

            if event.type == pygame.MOUSEBUTTONDOWN:  # check of user pressed button
                print("mouse down, displaying country", str(i))
                i += 1
                # territory = pygame.image.load("map/" + str(i) + ".png").convert()
                # territory = pygame.transform.scale(territory, (70, 40))
                # i += 1
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    MENUSTAT = True
                    menu(MENUSTAT, screen, clock, background1)

            if event.type == QUIT:  # check if user wants to quit
                pygame.quit()
                sys.exit()
            ######
            territory = pygame.image.load("Map/" + str(i) + ".png").convert()
            territory = pygame.transform.scale(territory, (game_width, game_height))
            screen.blit(territory, (0, 0))
            #####
            pygame.display.update()

def start():

    freshStart = True  # for initializing map animation
    running = True
    MENUSTAT = True
    game = False

    # window display, size, caption
    screen = pygame.display.set_mode((game_width, game_height))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Risk (GAME WINDOW)")
    # Background Image
    background1 = pygame.image.load("Pictures/background/menuBackground.jpg")


    # background = pygame.image.load("Map/green.jpg").convert()
    # background = pygame.transform.scale(background, (720, 450)) #resize green image
    menu(MENUSTAT, screen, clock, background1)

if __name__ == "__main__":
    start()


        
